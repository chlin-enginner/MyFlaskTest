from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/weixin')
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




if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=80)