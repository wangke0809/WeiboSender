# 模拟发送微博

基于 selenium 模拟发送微博，在 [2019-nCoV-Push](https://github.com/wangke0809/2019-nCoV-Push) 项目中使用，经过数次迭代，已经稳定运行一个月。

微博登陆态在每天都发送微博的情况下实测是可以维持一个月左右。

本项目中 `weibo.py` 可单独使用。

整体项目提供了一个 `/add` 接口，POST 提交要发送的微博内容。使用 Redis List 作为消息队列，定时检测待发送内容并发送。微博需要扫码登陆，通过钉钉群机器人下发二维码实现登陆。

## 安装依赖

目前测试了 Ubuntu 和 macos，下面给出 Ubuntu 下依赖安装方法

Ubuntu：

安装 Chrome:

```bash
# 服务器中文支持
apt-get update && apt-get install language-pack-zh-hans 

sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb # Might show "errors", fixed by next line
sudo apt-get install -f
# 查看版本
google-chrome --version
# 中文 ttf 字体放入 /usr/share/fonts/
fc-cache -fv
fc-list :lang=zh
```

下载 Driver: https://sites.google.com/a/chromium.org/chromedriver/downloads

安装 Python 依赖:

```bash
pip install -r requirements.txt
```

请使用 Python 3.5+，推荐 conda 管理 Python 运行环境。

## 配置

```bash
cp config.py.example config.py
```

按需求填写配置项。

## 启动

```bash
python main.py
```
