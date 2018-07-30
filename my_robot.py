#!/usr/bin/python
#coding:utf-8 

import time
import requests
import itchat
from itchat.content import *

KEY = 'f8daa2e8b916479998ed606bb08e0d85'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(TEXT, isGroupChat=True)
def tuling_reply(msg):
    group  = itchat.get_chatrooms(update=True)
    for g in group:
       if g['NickName'] == '测试':#从群中找到指定的群聊
           print(g['NickName'])
           print(g['UserName'])
           from_group = g['UserName']
           break

    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    #time.sleep(3)

    if msg['FromUserName'] == from_gruop:
        return reply or defaultReply
    return
    
# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    time.sleep(3)

    return reply or defaultReply

# @itchat.msg_register(PICTURE)
# def download_files(msg):
#     # msg['Text']是一个文件下载函数
#     # 传入文件名，将文件下载下来
#     msg['Text'](msg['FileName'])
#     # 把下载好的文件再发回给发送者
#     return '@%s@%s' % ({'PICTURE': 'img', 'VIDEO': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

itchat.auto_login(hotReload=True)
itchat.run()
