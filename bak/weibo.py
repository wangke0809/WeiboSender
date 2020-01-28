import requests
import time
import re
import urllib
import json
from http import cookiejar


def callbackdemo(image_name, raw_data):
    print("callback")
    with open(image_name, 'wb') as f:
        f.write(raw_data)
        f.close()
    print("callback end")


class Weibo(object):

    def __init__(self):
        index_url = "https://weibo.com/"
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar('weibo_cookies.txt')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        self.session.get(index_url, headers=self.headers)

    def getQrcode(self):
        qrcode_before = "https://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_" + str(
            time.time() * 10000)
        qrcode_before_page = self.session.get(qrcode_before, headers=self.headers)
        if qrcode_before_page.status_code != 200:
            return
        qrcode_before_data = qrcode_before_page.text
        qrcode_image = re.search(r'"image":"(?P<image>.*?)"', qrcode_before_data).group("image").replace("\/", "/")
        qrcode_qrid = re.findall(r'"qrid":"(.*?)"', qrcode_before_data)[0]
        cha_page = self.session.get("https:" + qrcode_image, headers=self.headers)
        image_name = u"cha." + cha_page.headers['content-type'].split("/")[1]
        return image_name, cha_page.content, qrcode_qrid

    def scanQrcode(self, qrcode_qrid, times):
        params = {
            "entry": "weibo",
            "qrid": qrcode_qrid,
            "callback": "STK_" + times
        }
        qrcode_check = "https://login.sina.com.cn/sso/qrcode/check"
        return self.session.get(qrcode_check, params=params, headers=self.headers).text

    def login(self, callback):

        if self.isLogin():
            return True

        image_name, raw_data, qrcode_qrid = self.getQrcode()
        callback(image_name, raw_data)

        # 下面判断是否已经扫描了二维码
        statu = 0
        while not statu:
            qrcode_check_page = self.scanQrcode(qrcode_qrid, str(time.time() * 10000))
            if "50114002" in qrcode_check_page:
                statu = 1
                print("已经扫描")
            time.sleep(2)

        # 下面判断是否已经点击登录,并获取alt的内容
        while statu:
            qrcode_click_page = self.scanQrcode(qrcode_qrid, str(time.time() * 100000))
            if "succ" in qrcode_click_page:
                print("登陆")
                # 登录成功后显示的是如下内容,需要获取到alt的内容
                # {"retcode":20000000,"msg":"succ","data":{"alt":"ALT-MTgxODQ3MTYyMQ==-sdfsfsdfsdfsfsdf-39A12129240435A0D"}}
                statu = 0
                alt = re.search(r'"alt":"(?P<alt>[\w\-\=]*)"', qrcode_click_page).group("alt")
            time.sleep(2)

        # 下面是登录请求获取登录的跨域请求
        params = {
            "entry": "weibo",
            "returntype": "TEXT",
            "crossdomain": 1,
            "cdult": 3,
            "domain": "weibo.com",
            "alt": alt,
            "savestate": 30,
            "callback": "STK_" + str(time.time() * 100000)
        }
        login_url_list = "https://login.sina.com.cn/sso/login.php"
        login_list_page = self.session.get(login_url_list, params=params, headers=self.headers)
        # 返回的数据如下所示，需要提取出4个url
        # STK_145809336258600({"retcode":"0","uid":"1111111","nick":"*****@sina.cn","crossDomainUrlList":
        # ["http:***************","http:\/\***************","http:\/\/***************","http:\/\/***************"]});
        url_list = [i.replace("\/", "/") for i in login_list_page.text.split('"') if "http" in i]
        print(url_list)
        for i in url_list:
            self.session.get(i, headers=self.headers)
            time.sleep(0.5)
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)

        return True

    def isLogin(self):
        try:
            self.session.cookies.load(ignore_discard=True, ignore_expires=True)
        except:
            return False
        url = "https://weibo.com/"
        my_page = self.session.get(url, headers=self.headers)
        if "我的首页" in my_page.text:
            return True
        else:
            return False

    def postWeibo(self, text):
        ts = int(time.time() * 1000)
        post_str = f'location=page_100505_manage&text={urllib.parse.quote(text)}&style_type=1&pdetail=1005052216356441&isReEdit=false&rank=0&pub_type=dialog&_t=0'
        url = f'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd={ts}'

        res = self.session.post(url, data=post_str, headers=self.headers).text
        print(res)
        j = json.loads(res)
        if j['code'] == '100000':
            return True
        else:
            return False

if __name__ == '__main__':
    w = Weibo()
    if w.isLogin():
        print("已经登陆")
        w.postWeibo("yes1")
    else:
        w.login(callbackdemo)
        w.postWeibo("yes2")
