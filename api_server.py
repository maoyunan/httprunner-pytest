import hashlib
import hmac
import json
import random
import string
from functools import wraps

from flask import Flask, request, make_response

# 用户调用 get_token（需要检查签名，用户需要根据签名算法 get_sign 算出sign）
app = Flask(__name__)

FLASK_APP_PORT = 5000
FLASK_APP_HOST = '127.0.0.1'
SECRET_KEY = "DebugTalk"

token_dict = {}
users_dict = {}


def get_sign(*args):
    # 签名算法
    content = ''.join(args).encode('ascii')
    sign_key = SECRET_KEY.encode('ascii')
    sign = hmac.new(sign_key, content, hashlib.sha1).hexdigest()
    return sign


def gen_md5(*args):
    # 计算md5
    return hashlib.md5("".join(args).encode('utf-8')).hexdigest()


def gen_random_string(str_len):
    """ generate random string with specified length
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


@app.route('/')
def index():
    # 欢迎页面
    return 'Hello World!'


# 检查登录状态的装饰器
def validate_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        device_sn = request.headers.get('device_sn', '')
        token = request.headers.get('token', '')

        if not device_sn or not token:
            result = {
                'success': False,
                'msg': 'device_sn or token is null'
            }
            response = make_response(json.dumps(result), 401)
            response.headers['"Content-Type"'] = "application/json"
            return response

        if token_dict[device_sn] != token:
            result = {
                'success': False,
                'msg': "Authorization failed!"
            }
            response = make_response(json.dumps(result), 403)
            response.headers["Content-Type"] = "application/json"
            return response
        return func(*args, **kwargs)

    return wrapper


@app.route('/api/get_token', methods=['POST'])
def get_token():
    device_sn = request.headers.get('device_sn', '')
    os_platform = request.headers.get('os_platform', '')
    app_version = request.headers.get('app_version', '')
    data = request.get_json()
    sign = data.get('sign', '')

    expected_sign = get_sign(device_sn, os_platform, app_version)
    if expected_sign != sign:
        result = {
            'success': False,
            'msg': "Authorization failed!"
        }
        response = make_response(json.dumps(result), 403)
    else:
        token = gen_random_string(16)
        token_dict[device_sn] = token

        result = {
            'success': True,
            'token': token
        }
        response = make_response(json.dumps(result))

    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/get_all_user')
@validate_request
def get_all_user():
    users_list = [user for uid, user in users_dict.items()]
    users = {
        'success': True,
        'count': len(users_list),
        'items': users_list
    }
    response = make_response(json.dumps(users))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/<int:uid>')
@validate_request
def get_user(uid):
    user = users_dict.get(uid, {})
    if user:
        result = {
            'success': True,
            'data': user
        }
        status_code = 200
    else:
        result = {
            'success': False,
            'data': user
        }
        status_code = 404

    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/reset_all_users')
@validate_request
def clear_users():
    users_dict.clear()
    result = {
        'success': True
    }
    response = make_response(json.dumps(result))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/user/<int:uid>', methods=['POST'])
@validate_request
def create_user(uid):
    user = request.get_json()
    if uid not in users_dict:
        result = {
            'success': True,
            'msg': "user created successfully."
        }
        status_code = 201
        users_dict[uid] = user
    else:
        result = {
            'success': False,
            'msg': "user already existed."
        }
        status_code = 500

    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/<int:uid>', methods=['DELETE'])
@validate_request
def delete_user(uid):
    user = users_dict.pop(uid, {})
    if user:
        success = True
        status_code = 200
    else:
        success = False
        status_code = 404

    result = {
        'success': success,
        'data': user
    }
    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/<int:uid>', methods=['PUT'])
@validate_request
def update_user(uid):
    user = users_dict.get(uid, {})
    if user:
        user = request.get_json()
        success = True
        status_code = 200
        users_dict[uid] = user
    else:
        success = False
        status_code = 404

    result = {
        'success': success,
        'data': user
    }
    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

# if __name__ == '__main__':
#     app.run(FLASK_APP_HOST, FLASK_APP_PORT)
