from typing import Any, Collection, Literal, Sequence, MutableSequence

collection_like = Collection|object

def read_collection(source: collection_like, key: str|int):
	if isinstance(source, dict):
		return source.get(key)
	
	if isinstance(source, Sequence):
		try:
			return source.__getitem__(int(key))
		except:
			return None
	try:
		source = getattr(source, str(key))
	except:
		return None
	
def write_collection(source: collection_like, key: str|int, value):
	if isinstance(source, dict):
		source[key] = value
		return True
	if isinstance(source, Sequence):
		try:
			s: Any = source
			s[key] = value
			return True
		except:
			return False
	try:
		setattr(source, str(key), value)
		source = getattr(source, str(key))
		return True
	except:
		return False

def path(source: collection_like, pathStr: str) -> Any:
	out = source
	parts = pathStr.split(".")
	for part in parts:
		try:
			out = read_collection(out, part)
		except:
			return None			
	return out
