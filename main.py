import threading
import logging, logging.config
import json
import config
from message import Message
from push import Push
from weibo import Weibo
import traceback
import random
import time
from api import app

conf = json.loads(config.LoggerJsonConfig)
logging.config.dictConfig(conf)

log = logging.getLogger('main')
push = Push(config.DingTalkWebHookToken)


def callback(path):
    url = config.Url + path + '?rand=%d' % random.randrange(10000)
    title = '微博登陆提醒'
    text = '![.](%s)' % url
    push.push(title, text, config.DingTalkWebHookAtPhone)


def main():
    queue = Message(config.Redis, config.RedisKey)
    weibo = Weibo(config.ChromeDriver, callback)
    while True:
        try:
            msg = queue.getMessage()
            if msg is not None:
                log.info("检测到消息，准备发送")
                msg = msg.decode()
                weibo.postWeibo(msg)
        except Exception:
            queue.reAddMessage(msg)
            log.error("error: %s", traceback.format_exc())
        time.sleep(10)


if __name__ == '__main__':
    t = threading.Thread(target=main, args=(), name="main")
    t.start()
    app.run(host="127.0.0.1", port=8060)
