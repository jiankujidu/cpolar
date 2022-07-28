# -*- coding: UTF-8 -*-
# Version: v1.1
# Created by lstcml on 2022/07/21
# 建议定时10分钟：*/10 * * * *

'''
使用说明：
1、https://i.cpolar.com/m/4LUd/注册登录后获取authtoken；
2、新增变量qlnwct_authtoken，值为你账户的authtoken，运行脚本

更新记录：
V1.1
1、开放推送，仅支持PushPlus推送，每次触发启动穿透会推送一次地址
'''
'''
cron： */10 * * * * *
new Env（'cpolar内网穿透'）;
'''

import os
import re
import sys
import json
import requests
from time import sleep
path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(path, "nwct_cpolar_log")
log_name = os.path.join(log_path, "cpolar")
log_file = os.path.join(log_path, "cpolar.master.log") 
app_path = os.path.join(path, "cpolar")
commond = "python3 " + os.path.join(path, "cpolar.py") + " &"

def update():
    print("当前运行的脚本版本：" + str(version))
    try:
        r1 = requests.get("https://gitee.com/lstcml/qinglongscripts/raw/master/nwct_cpolar.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("killall cpolar")
            os.system("ql raw https://gitee.com/lstcml/qinglongscripts/raw/master/nwct_cpolar.py &")
    except:
        pass


# 下载主程序
def download_cpolar():
    if not os.path.exists("cpolar.py"):
        res = requests.get("https://gitee.com/lstcml/qinglongscripts/raw/master/cpolar.py")
        with open("cpolar.py", "wb") as f:
            f.write(res.content)
    if not os.path.exists("cpolar"):
        res = requests.get("https://static.cpolar.com/downloads/releases/3.2.88.2/cpolar-stable-linux-arm.zip")
        with open("cpolar.zip", "wb") as f:
            f.write(res.content)
        os.system("unzip cpolar.zip >/dev/null 2>&1&&rm -f cpolar.zip&&chmod +x cpolar&&" + app_path + " authtoken  " + authtoken + ">/dev/null 2>&1")
    start_nwct()        

# 获取穿透url
def get_url():
    try:
        with open(log_file, encoding='utf-8') as f:
            log_content = f.read()
        reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        for i in re.findall(reg, log_content):
            if 'cpolar' in i:
                print("获取穿透链接成功...")
                return i.replace('\\', '')
                break
    except:
        return "https://gitee.com/lstcml/qinglongscripts"

# 进程守护
def process_daemon():
    print("公众号：一起瞎折腾\nQQ交流群:641307462\n正在检测穿透状态...")
    global qlurl
    qlurl = get_url()
    try:
        res = requests.get(qlurl + "/login").text
        if "/images/g5.ico" in res:
            return True
        else:
            return False
    except:
        return False


# 执行程序
def start_nwct():
    if not process_daemon():
        os.system("rm -rf " + log_path)
        os.system("mkdir -p " + log_path)
        os.system("killall cpolar >/dev/null 2>&1")
        print("正在启动内网穿透...")
        os.system(commond)
        sleep(10)
        if process_daemon():
            if load_send():
                print("启动内网穿透成功！\n青龙面板：%s" % qlurl)
                send("内网穿透通知", "青龙面板访问地址：" + qlurl)
        else:
            print("启动内网穿透失败...")
    else:
        print("穿透程序已在运行...\n青龙面板：%s" % qlurl)


# 推送
def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    sendNotifPath = cur_path + "/sendNotify.py"
    if not os.path.exists(sendNotifPath):
        res = requests.get("https://gitee.com/lstcml/qinglongscripts/raw/master/sendNotify.py")
        with open(sendNotifPath, "wb") as f:
            f.write(res.content)

    try:
        from sendNotify import send
        return True
    except:
        print("加载通知服务失败！")
        return False


if __name__ == '__main__':
    version = 1.1
    try:
        authtoken = os.environ['qlnwct_authtoken']
    except:
        authtoken = ""
    try:
        token = os.environ['PUSH_PLUS_TOKEN']
    except:
        token = ""
    try:
        check_update = os.environ['qlnwctupdate']
    except:
        check_update = ""

    if check_update == "true":
        update()
    else:
        print("变量qlnwctupdate未设置，脚本自动更新未开启！")
    if len(authtoken ) < 1:
        print("请新增变量qlnwct_authtoken！")
    else:
        download_cpolar()
