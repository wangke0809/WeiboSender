import redis


class Message(object):

    def __init__(self, url, redisKey='WEIBOMESSAGEQUENE'):
        self.rds = redis.Redis.from_url(url)
        self.key = redisKey

    def addMessage(self, text):
        self.rds.lpush(self.key, text)

    def getMessage(self):
        msg = self.rds.rpop(self.key)
        return msg

    def reAddMessage(self, text):
        self.rds.rpush(self.key, text)


if __name__ == '__main__':
    import config

    m = Message(config.Redis)
    print(m.getMessage())
    print(m.getMessage())
    print(m.addMessage("aaa"))
    print(m.addMessage("bbb"))
    print(m.getMessage())
    print(m.getMessage())
