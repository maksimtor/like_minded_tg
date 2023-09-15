import redis


class RedisClient:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    