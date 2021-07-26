import os
import re
import time

import feedparser
import requests

requests.packages.urllib3.disable_warnings()


def getSubscribeUrl():
    dirs = './subscribe'
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
    summary = rss["entries"][0]["summary"]

    # 获取普通订阅链接
    v2rayList = re.findall(
        r"v2ray\(若无法更新请开启代理后再拉取\)：(.+?)</div>", summary)
    if v2rayList:
        v2rayTxt = requests.request(
            "GET", v2rayList[-1].replace('amp;', ''), verify=False)
        with open(dirs + '/v2ray.txt', 'wb') as f:
            f.write(v2rayTxt.text.encode("utf-8"))

    # 获取clash订阅链接
    clashList = re.findall(
        r"clash\(若无法更新请开启代理后再拉取\)：(.+?)</div>", summary)
    if clashList:
        clashTxt = requests.request(
            "GET", clashList[-1].replace('amp;', ''), verify=False)
        day = time.strftime('%m%d%H%M', time.localtime(time.time()))
        with open(dirs + '/clash.yml', 'wb') as f:
            clash_content = clashTxt.text.replace('https://www.mattkaydiary.com', day)
            f.write(clash_content.encode("utf-8"))


def main():
    getSubscribeUrl()


# 主函数入口
if __name__ == '__main__':
    main()
