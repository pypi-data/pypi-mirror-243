from typing import Callable, TypeVar

InstanceType = TypeVar("InstanceType")

class ClientCache:
	clients: dict = {}

	def __init__(self):
		self.clients = {}

	@classmethod
	def load(cls, property: str, callback: Callable[..., InstanceType], *args, **kwargs) -> InstanceType:
		if not (property in cls.clients):
			instance = callback(*args, **kwargs)
			cls.clients[property] = instance
		return cls.clients[property]
	
	@classmethod
	def failed_import(cls, excpt: ModuleNotFoundError, name: str):
		instructions = f"Run ( pip install barkus-func-toolkit[{name}] ) to fix it"
		print(f"\n{excpt.msg}")
		print(">> " + instructions + "\n")
		raise ModuleNotFoundError(f"{excpt.msg}\n{instructions}")
	
class CloudClientManager:

	@classmethod
	@property
	def firestore(cls):
		try:
			from google.cloud.firestore import Client
		except ModuleNotFoundError as err:
			return ClientCache.failed_import(err, "firestore")
		return ClientCache.load("firestore", Client)
	
	@classmethod
	@property
	def bigquery(cls):
		try:
			from google.cloud.bigquery import Client
		except ModuleNotFoundError as err:
			return ClientCache.failed_import(err, "bigquery")
		return ClientCache.load("bigquery", Client)
	
	@classmethod
	@property
	def pubsub(cls):
		try:
			from google.cloud.pubsub import PublisherClient
		except ModuleNotFoundError as err:
			return ClientCache.failed_import(err, "pubsub")
		return ClientCache.load("pubsub", PublisherClient)
