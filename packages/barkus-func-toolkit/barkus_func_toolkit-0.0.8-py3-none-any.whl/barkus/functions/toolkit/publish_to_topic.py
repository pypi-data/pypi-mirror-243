import json
from .cloud_client_manager import CloudClientManager

def publish_to_topic(project: str, topic: str, attributes: dict) -> None:
	topic_name = f'projects/{project}/topics/{topic}'

	print(f"Publishing to [{topic_name=}] with", attributes)

	message_data_bytes = json.dumps(attributes).encode()

	CloudClientManager.pubsub.publish(topic_name, data=message_data_bytes)