"""
Redis client configuration
"""
import redis
from app.config import settings

# Create Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)

# Test connection
try:
    redis_client.ping()
    print("✓ Redis connection successful")
except redis.ConnectionError as e:
    print(f"✗ Redis connection failed: {e}")
    print("  Make sure Redis is running on", settings.REDIS_URL)

def get_redis():
    """Dependency to get Redis client"""
    return redis_client

