from redis import StrictRedis, ConnectionPool
import config.server_config as server_config

redis_instance = None
pool = None


def redis_server_init():
    global redis_instance, pool
    pool = ConnectionPool(host=server_config.REDIS_ARGS["host"], port=server_config.REDIS_ARGS["port"], )
    redis_instance = StrictRedis(connection_pool=pool)


def get_redis_instance():
    return redis_instance
