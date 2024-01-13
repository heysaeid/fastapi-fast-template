from fastapi_and_caching import RedisCache
from config import settings


cache = RedisCache(namespace=settings.redis_cache_namespace)