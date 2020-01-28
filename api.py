from flask import Flask, request, jsonify
from message import Message
import config
import logging

log = logging.getLogger("api")
app = Flask(__name__, static_folder='', static_url_path='')
queue = Message(config.Redis, config.RedisKey)


@app.route('/add', methods=['POST'])
def add():
    try:
        msg = request.get_data().decode()
        queue.addMessage(msg)
        log.info("add: %s" % msg)
        return jsonify(success=True)
    except Exception as e:
        log.error("err: %s" % str(e))
        return jsonify(success=False, msg=str(e))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8060)
