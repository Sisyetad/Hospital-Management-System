from functools import wraps
from .redis_cache_helper import RedisCacheHelper

cache_helper = RedisCacheHelper()

def cache_get(prefix: str, id_arg_name: str, ttl: int = 3600):
    """
    Decorator to cache the result of a method using object prefix and an identifier.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            identifier = kwargs.get(id_arg_name)
            if identifier is None:
                raise ValueError(f"Missing expected keyword arg: {id_arg_name}")

            cached_data = cache_helper.get(prefix, str(identifier))
            if cached_data:
                return cached_data

            result = func(self, *args, **kwargs)
            cache_helper.set(prefix, str(identifier), result, ttl)
            return result
        return wrapper
    return decorator

def cache_invalidate(items_to_clear: list[tuple[str, str]]):
    """
    Decorator to invalidate specific cache keys after a write method.
    Each item: (prefix, id_arg_name)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            to_invalidate = []
            for prefix, id_arg_name in items_to_clear:
                identifier = kwargs.get(id_arg_name, 'all')
                to_invalidate.append((prefix, str(identifier)))

            cache_helper.bulk_delete(to_invalidate)
            return result
        return wrapper
    return decorator


def no_cache(func):
    """
    Decorator that bypasses any caching and always executes the method.
    Useful for endpoints or services where fresh data is required.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
