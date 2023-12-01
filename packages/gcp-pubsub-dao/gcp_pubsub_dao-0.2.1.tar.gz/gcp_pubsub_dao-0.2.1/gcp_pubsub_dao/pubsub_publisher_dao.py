from google.cloud.pubsub_v1 import PublisherClient


class PubSubPublisherDAO:
    def __init__(self, project_id: str):
        self.publisher = PublisherClient()
        self.project_id = project_id

    def publish_message(self, topic_name: str, payload: bytes, attributes: dict) -> None:
        self.publisher.publish(
            topic=self.publisher.topic_path(project=self.project_id, topic=topic_name),
            data=payload,
            **attributes,
        ).result()
