from django.core.cache import cache
import json

class RedisCacheHelper:
    def _build_key(self, prefix: str, identifier: str) -> str:
        return f"{prefix}:{identifier}"

    def get(self, prefix: str, identifier: str):
        key = self._build_key(prefix, identifier)
        return cache.get(key)

    def set(self, prefix: str, identifier: str, value, ttl=3600):
        key = self._build_key(prefix, identifier)
        return cache.set(key, value, timeout=ttl)

    def delete(self, prefix: str, identifier: str):
        key = self._build_key(prefix, identifier)
        return cache.delete(key)

    def bulk_delete(self, items: list[tuple[str, str]]):
        """Accepts a list of (prefix, identifier) to delete multiple keys."""
        for prefix, identifier in items:
            self.delete(prefix, identifier)
