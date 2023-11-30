import asyncio
import logging
import typing as t
from dataclasses import dataclass

from gcp_pubsub_dao.async_pubsub_subscriber_dao import AsyncPubSubSubscriberDAO
from gcp_pubsub_dao.entities import Message

logger = logging.getLogger()


@dataclass
class HandlerResult:
    ack_id: str
    is_success: bool


@dataclass
class WorkerTask:
    subscriber_dao: AsyncPubSubSubscriberDAO
    handler: t.Callable[[Message], t.Awaitable[HandlerResult]]
    batch_size: int = 10
    return_immediately: bool = True


class WorkerPool:
    async def run(self, tasks: t.Iterable[WorkerTask]):
        async with asyncio.TaskGroup() as tg:
            for task in tasks:
                tg.create_task(self._run_worker(task=task))

    async def _run_worker(self, task: WorkerTask):
        while True:
            await self._job(task=task)

    async def _job(self, task: WorkerTask):
        messages = await task.subscriber_dao.get_messages(
            messages_count=task.batch_size,
            return_immediately=task.return_immediately,
        )

        ack_ids, nack_ids = [], []
        for coro in asyncio.as_completed([task.handler(message) for message in messages]):
            try:
                result: HandlerResult = await coro
            except Exception as ex:
                logger.error(f"Exception during task processing. Details: {ex}")
                continue

            if result.is_success:
                ack_ids.append(result.ack_id)
            else:
                nack_ids.append(result.ack_id)

        if ack_ids:
            await task.subscriber_dao.ack_messages(ack_ids=ack_ids)
        if nack_ids:
            await task.subscriber_dao.nack_messages(ack_ids=nack_ids)
