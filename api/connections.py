from pymysql import connections, cursors
import os
import redis


def get_connection():
    return connections.Connection(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASS', 'my-secret-pass'),
        database=os.environ.get('DB_DATABASE', 'my-db'),
        port=int(os.environ.get('DB_PORT', 3306)),
        connect_timeout=5,
        cursorclass=cursors.DictCursor
    )


def get_redis_connection():
    pool = redis.Redis(
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        password=os.environ.get('REDIS_PASSWORD', ''),
        decode_responses=True
        # db=os.environ.get('REDIS_DB', 0),

    )
    return pool
    # return redis.Redis(connection_pool=pool)

