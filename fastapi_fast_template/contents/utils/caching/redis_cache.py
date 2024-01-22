from config import settings
from fastapi_and_caching import RedisCache

cache = RedisCache(namespace=settings.redis_cache_namespace)
