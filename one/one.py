# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response
import hashlib
import time
import json
import requests

from lxml import etree
import datetime

import sys

reload(sys)

sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/weixin',methods=['GET','POST'])
def weixin():
    app.logger.info("0method:"+request.method)
    app.logger.info("0url:"+request.url)
    if request.method == 'GET':
        app.logger.info("url:" + request.url)
        signature=request.args.get("signature")

        app.logger.info("signature:"+str(signature))
        timestamp = request.args.get("timestamp")
        app.logger.info("signature:" + str(timestamp))
        nonce = request.args.get("nonce")
        app.logger.info("signature:" + str(nonce))
        echostr = request.args.get("echostr")
        app.logger.info("signature:" + str(echostr))

        token = "csxwxapp"

        list = [str(token), str(timestamp),str(nonce)]
        list.sort()
        ts = ''.join(list)

        hashcode = hashlib.sha1(ts.encode('utf-8')).hexdigest()
        app.logger.info("hashcode:" + hashcode)
        if hashcode == signature:
            return echostr
        else:
            return "error"
    else:
        str_xml = request.data
        xml = etree.fromstring(str_xml)
        content = xml.find("Content").text

        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        touserName = xml.find("ToUserName").text
        nowTime = str(time.time())

        app.logger.info("content:"+str(content))
        app.logger.info("touserName:"+str(touserName))
        app.logger.info("fromUser"+str(fromUser))

        now = datetime.datetime.now()
        now.strftime('%Y-%m-%d')
        start_data = datetime.datetime.strptime('2019-02-05', '%Y-%m-%d')
        run_days=(now-start_data).days


        if not str(content).startswith("/"):
            say_ai_data = {"reqType": 0, "perception": {"inputText": {"text": content}},
                           "userInfo": {"apiKey": "3b27ac8f81ee4853be53a4d22211533a", "userId": "rudy"}}

            api_url2 = "http://openapi.tuling123.com/openapi/api/v2"

            req = requests.post(api_url2, json.dumps(say_ai_data)).json()
            content=req['results'][0]['values']['text']

        if str(content)=="/help":
            content="您好！欢迎您！本号旨在探讨个人数据分析场景，并尝试使用简单、" \
                    "友好的方式帮助个人实现数据分析的需求。已累计运行"+\
                    str(run_days)+"天，实现AI聊天接入功能，后续会有更多分析功能上线，敬请期待！多谢关注！"

        res="<xml><ToUserName><![CDATA["+str(fromUser)+\
            "]]></ToUserName><FromUserName><![CDATA["+str(touserName)+\
            "]]></FromUserName><CreateTime>"+nowTime+"</CreateTime><MsgType><![CDATA["+msgType+\
            "]]></MsgType><Content><![CDATA["+str(content)+"]]></Content></xml>"

        return Response(str(res),  mimetype='application/xml')


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=80)