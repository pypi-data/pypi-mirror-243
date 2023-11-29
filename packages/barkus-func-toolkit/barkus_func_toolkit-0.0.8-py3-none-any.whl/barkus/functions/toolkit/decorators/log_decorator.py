from typing import Callable, Any

def log(depth: int = 0, *, name: str|None = None):
	prefix = "  "*depth + (" " if depth > 0 else "")
	input_name = name
	def decorator(func: Callable[..., Any]):
		def wrapper(*args, **kwargs):
			name = input_name or f"{prefix}{func.__name__}"
			print(f"{name} - start")
			try:
				result = func(*args, **kwargs)
				print(f"{name} - end")
				return result
			except Exception as e:
				print(f"-->{name} - error")
				raise e
		return wrapper
	return decorator