# WeiboSender

## 安装依赖

Ubuntu：

```bash
# 中文
apt-get update && apt-get install language-pack-zh-hans 
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb # Might show "errors", fixed by next line
sudo apt-get install -f
# 查看版本
google-chrome --version
# ttf 字体放入 /usr/share/fonts/
fc-cache -fv
fc-list :lang=zh
```

下载 Driver

https://sites.google.com/a/chromium.org/chromedriver/downloads

