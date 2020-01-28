import requests
import json


class Push(object):

    def __init__(self, token):
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % token

    def push(self, title, text, at=None):
        msg = {}
        msg['msgtype'] = 'markdown'
        msg['markdown'] = {}
        msg['markdown']['title'] = title
        msg['markdown']['text'] = text
        msg['at'] = {}
        msg['at']['isAtAll'] = False
        if at is not None:
            msg['at']['atMobiles'] = []
            msg['at']['atMobiles'].append(at)
            msg['markdown']['text'] += "\r\n\r\n@%s"%at
        headers = {"Content-Type": "application/json"}
        res = requests.post(self.url, data=json.dumps(msg), headers=headers)
        return res.json()


if __name__ == '__main__':
    import config
    import time

    p = Push(config.DingTalkWebHookToken)
    p.push("title", "text.")
    time.sleep(1)
    p.push("title", "text.", config.DingTalkWebHookAtPhone)