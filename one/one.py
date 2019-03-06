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
        signature=request.args.get("signature")
        print(signature)
        timestamp = request.args.get("timestamp")
        print(timestamp)
        nonce = request.args.get("nonce")
        print(nonce)
        echostr = request.args.get("echostr")
        print(echostr)

        token = "csxwxapp"

        list = [token, timestamp, nonce]
        list.sort()
        ts = ''.join(list)

        hashcode = hashlib.sha1(ts.encode('utf-8')).hexdigest()

        if hashcode == signature:
            return echostr




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)