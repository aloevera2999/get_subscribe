import os
import re
import time

import feedparser
import requests

requests.packages.urllib3.disable_warnings()


def write_log(content, level="INFO"):

    date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    update_log = f"[{date_str}] [{level}] {content}\n"
    with open('./log/update.log', 'a') as f:
        f.write(update_log)


def get_subscribe_url():
    dirs = './subscribe'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    log_dir = "./log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
    entries = rss.get("entries")
    if not entries:
        write_log("更新失败！无法拉取原网站内容", "ERROR")
        return
    summary = entries[0]["summary"]

    update_list = []
    # 获取普通订阅链接
    v2ray_list = re.findall(
        r"v2ray\(若无法更新请开启代理后再拉取\)：(.+?)</div>", summary)
    if v2ray_list:
        v2ray_req = requests.request(
            "GET", v2ray_list[-1].replace('amp;', ''), verify=False)
        v2ray_code = v2ray_req.status_code
        update_list.append(f"v2ray: {v2ray_code}")
        with open(dirs + '/v2ray.txt', 'wb') as f:
            f.write(v2ray_req.text.encode("utf-8"))

    # 获取clash订阅链接
    clash_list = re.findall(
        r"clash\(若无法更新请开启代理后再拉取\)：(.+?)</div>", summary)
    if clash_list:
        clash_req = requests.request(
            "GET", clash_list[-1].replace('amp;', ''), verify=False)
        clash_code = clash_req.status_code
        update_list.append(f"clash: {clash_code}")
        with open(dirs + '/clash.yml', 'wb') as f:
            clash_content = clash_req.text.replace('https://www.mattkaydiary.com', "日本瞎眼裁判")
            f.write(clash_content.encode("utf-8"))

    if update_list:
        write_log(f"更新成功：{update_list}", "INFO")
    else:
        write_log(f"未能获取新的更新内容", "WARN")

def main():
    get_subscribe_url()


# 主函数入口
if __name__ == '__main__':
    main()
