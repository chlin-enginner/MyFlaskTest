from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        app.logger.info("url:" + request.url)
        signature=request.args.get("signature")
        app.logger.info("signature:"+signature)
        timestamp = request.args.get("timestamp")
        app.logger.info("signature:" + signature)
        nonce = request.args.get("nonce")
        app.logger.info("signature:" + signature)
        echostr = request.args.get("echostr")
        app.logger.info("signature:" + signature)

        token = "csxwxapp"

        list = [token, timestamp, nonce]
        list.sort()
        ts = ''.join(list)

        hashcode = hashlib.sha1(ts.encode('utf-8')).hexdigest()
        app.logger.info("hashcode:" + hashcode)
        if hashcode == signature:
            return echostr




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)