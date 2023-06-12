from flask import Flask, request, make_response, Response
from connections import get_connection, get_redis_connection
import json
import hashlib
from flask_cors import CORS

redis_connection = get_redis_connection()
connection = get_connection()
app = Flask(__name__)
CORS(app)


@app.route("/get_data", methods=['POST'])
def get_data():
    cache_hit = True
    req = request.json
    user_id = req['user_id']

    sql = f"SELECT * FROM `users` where id={user_id}"
    hashed_sql = hashlib.md5(sql.encode('utf-8')).hexdigest()
    data = read_from_cache(hashed_sql)
    print(f"cache data--->>>", data)
    if data is None:
        cache_hit = False
        data = read_from_db(sql)
        print(f"sql--->>>", sql, flush=True)
        print(f"db data--->>>", data, flush=True)
        if data is not None:
            print(f"cache set--->>>", data)
            set_in_cache(
                hashed_sql=hashed_sql,
                value=json.dumps(data)
            )
    else:
        data = json.loads(data)
    return Response(
        response=json.dumps({
            "cache_hit": cache_hit,
            "data": data
        }),
        headers={
            'Access-Control-Allow-Origin': '*'
        },
        mimetype='application/json',
        content_type='application/json',
    )


@app.route("/save_data", methods=['POST'])
def save_data():
    redis_connection.publish(channel='insert_channel', message=json.dumps(request.json))
    return Response(
        response=json.dumps({
                "message": "Success"
            }),
        headers={
            'Access-Control-Allow-Origin': '*'
        },
        mimetype='application/json',
        content_type='application/json',
    )


def read_from_cache(hashed_sql):
    data = redis_connection.get(hashed_sql)
    return data


def set_in_cache(hashed_sql, value):
    data = redis_connection.set(name=hashed_sql, value=value, ex=30)
    return data


def read_from_db(sql):
    with connection.cursor() as cur:
        connection.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
    connection.commit()
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0')
