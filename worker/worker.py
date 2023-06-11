import time

from connections import get_connection, get_redis_connection
import json
import pymysql

connection = None

while connection is None:
    try:
        print("trying to connect")
        connection = get_connection()
        print('success')
    except pymysql.err.OperationalError as e:
        print(e)
        time.sleep(1)

redis_connection = get_redis_connection()


p = redis_connection.pubsub()

p.subscribe('insert_channel')
# redis_connection.publish(channel='insert_channel', message=json.dumps({'name': "niloy"}))
while True:
    try:
        # print("worker start")
        message = json.loads(p.get_message()['data'])
        print(message)
        if message is not None:
            print("new message: ", message)
            # save to db
            with connection.cursor() as cur:
                sql = f"INSERT INTO users (`name`) VALUES ('{message['name']}')"
                connection.ping(reconnect=True)
                cur.execute(sql)
            connection.commit()
    except TypeError as e:
        pass

    except pymysql.err.ProgrammingError as e:
        print(e)
    except pymysql.err.OperationalError as e:
        print(e)
        time.sleep(5)
