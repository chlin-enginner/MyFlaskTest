from flask import Flask
from flask import request
from flask import Response
import hashlib
import time

from lxml import etree

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

        app.logger.info("content:"+str(content))
        app.logger.info("touserName:"+str(touserName))
        app.logger.info("fromUser"+str(fromUser))

        nowTime=str(time.time())



        res="<xml><ToUserName><![CDATA["+str(fromUser)+"]]></ToUserName><FromUserName><![CDATA["+str(touserName)+"]]></FromUserName><CreateTime>"+nowTime+"</CreateTime><MsgType><![CDATA["+msgType+"]]></MsgType><Content><![CDATA["+str(content)+"]]></Content></xml>"

        return Response(str(res),  mimetype='application/xml')




if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=80)