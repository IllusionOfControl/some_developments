from flask import Flask, request
import redis
import time

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


@app.route('/')
def index():
    cache = r.get('index')
    if not cache:
        time.sleep(3)
    payload = 'Hello <a href="/calc">click</a>'
    r.set('index', payload, ex=5)
    return payload


@app.route('/calc')
def calc():
    args = request.args
    a = args.get('a', None)
    b = args.get('b', None)
    value = ""
    if a is not None and b is not None:
        value = a + b
        cache = r.get(value)
        if not cache:
            time.sleep(3)
            r.set(value, value)
    return """
                Value: {}
                <form method="get">
                <input type="text" name="a">
                <input type="text" name="b">
                <button type="submit">Submit</button>
                </form>
            """.format(value)


app.run(debug=True)
