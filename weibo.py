from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from PIL import Image
import requests
import random
import logging

log = logging.getLogger("weibo")

class Weibo(object):

    def __init__(self, driverPath, callBack=None):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=options, executable_path=driverPath)
        self.browser.set_window_size(1366, 768)
        self.wait = WebDriverWait(self.browser, 30)
        self.callBack = callBack

    def isLogin(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[2]/textarea')
            log.info("检查是否登陆 已经登陆")
            return True
        except NoSuchElementException:
            log.info("检查是否登陆 没有登陆")
            return False

    def __login(self):
        log.info("开始登陆")
        if self.isLogin():
            return
        self.browser.get("https://weibo.com/login.php")
        qrcodeTab = self.browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[1]/div/a[2]')
        qrcodeTab.click()
        qrcodeImg = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pl_login_form"]/div/div[2]/img')))
        time.sleep(20)
        while True:
            if qrcodeImg.location['x'] > 0 and qrcodeImg.size['width'] > 0:
                break
            log.info("等待加载二维码图像")
            time.sleep(0.1)

        location = qrcodeImg.location
        size = qrcodeImg.size
        x, y, w, h = location['x'], location['y'], size['width'], size['height']
        rangle = (x, y, x + w, y + h)

        screenShotName = "screenShot.png"
        qrImgPath = "qr.png"

        self.browser.save_screenshot(screenShotName)

        img = Image.open(screenShotName)
        qr = img.crop(rangle)
        qr.save(qrImgPath)

        if self.callBack:
            self.callBack(qrImgPath)

    def login(self):
        while True:
            self.__login()

            success = False
            waitTimes = 0

            while True:
                waitTimes += 1
                if self.isLogin():
                    success = True
                    break
                else:
                    time.sleep(1)
                if waitTimes > 300:
                    log.info("扫码超时，重新获取二维码")
                    break
                log.info("等待扫码" + '.' * waitTimes + '\r')

            if success:
                break

    def postWeibo(self, text):
        if not self.isLogin():
            self.login()
        content = self.browser.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[2]/textarea')
        content.send_keys(text)
        send = self.browser.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[3]/div[1]/a')
        send.click()
        log.info("发送微博: " + text)

    def close(self):
        self.browser.quit()

    def __del__(self):
        self.browser.quit()


if __name__ == '__main__':
    def randomStr(l):
        r = ''
        for i in range(l):
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)
            val = f'{head:x}{body:x}'
            s = bytes.fromhex(val).decode('gb2312')
            r += s
        return r

    w = Weibo('./chromedriver')
    while True:
        w.postWeibo("认识几个字？" + randomStr(random.randrange(1, 6)))
        t = 1000 + random.randrange(100, 800)
        log.info("睡眠 %d s" % t)
        time.sleep(t)
