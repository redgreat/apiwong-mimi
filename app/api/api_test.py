import logging
from flask import Blueprint, jsonify, session, request, current_app
from datetime import datetime, timedelta
from decimal import Decimal

from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.util import route, Redis
from app.utils.auth import Auth, login_required
from app.api.wx_login_or_register import get_access_code, get_wx_user_info, wx_login_or_register

bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


# -----------------原生蓝图路由---------------#


@bp.route('/logs', methods=["GET"])
def test_logger():
    """
    测试自定义logger
    :return:
    """
    logger.info("this is info")
    logger.debug("this is debug")
    logger.warning("this is warning")
    logger.error("this is error")
    logger.critical("this is critical")
    return "ok"


@bp.route("/unifiedResponse", methods=["GET"])
def test_unified_response():
    """
    测试统一返回消息
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    res.update(code=ResponseCode.Success, data=test_dict)
    return jsonify(res.data)


# --------------使用自定义封装蓝图路由--------------------#


@route(bp, '/packedResponse', methods=["GET"])
def test_packed_response():
    """
    测试响应封装
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    # 此处不再需要用jsonify，如果需要定制返回头或者http响应如下所示
    # return res.data,200,{"token":"111"}
    return res.data


@route(bp, '/typeResponse', methods=["GET"])
def test_type_response():
    """
    测试返回不同的类型
    :return:
    """
    res = ResMsg()
    now = datetime.now()
    date = datetime.now().date()
    num = Decimal(11.11)
    test_dict = dict(now=now, date=date, num=num)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    # 此处不再需要用jsonify，如果需要定制返回头或者http响应如下所示
    # return res.data,200,{"token":"111"}
    return res.data


# --------------Redis测试封装--------------------#

@route(bp, '/testRedisWrite', methods=['GET'])
def test_redis_write():
    """
    测试redis写入
    """
    # 写入
    Redis.write("test_key", "test_value", 60)
    return "ok"


@route(bp, '/testRedisRead', methods=['GET'])
def test_redis_read():
    """
    测试redis获取
    """
    data = Redis.read("test_key")
    return data


# --------------------JWT测试-----------------------------------------#

@route(bp, '/testLogin', methods=["POST"])
def test_login():
    """
    登陆成功获取到数据获取token和刷新token
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)
    user_name = obj.get("name")
    # 未获取到参数或参数不存在
    if not obj or not user_name:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    if user_name == "qin":
        # 生成数据获取token和刷新token
        access_token, refresh_token = Auth.encode_auth_token(user_id=user_name)

        data = {"access_token": access_token.decode("utf-8"),
                "refresh_token": refresh_token.decode("utf-8")
                }
        res.update(data=data)
        return res.data
    else:
        res.update(code=ResponseCode.AccountOrPassWordErr)
        return res.data


@route(bp, '/testGetData', methods=["GET"])
@login_required
def test_get_data():
    """
    测试登陆保护下获取数据
    :return:
    """
    res = ResMsg()
    name = session.get("user_name")
    data = "{}，你好！！".format(name)
    res.update(data=data)
    return res.data


@route(bp, '/testRefreshToken', methods=["GET"])
def test_refresh_token():
    """
    刷新token，获取新的数据获取token
    :return:
    """
    res = ResMsg()
    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    payload = Auth.decode_auth_token(refresh_token)
    # token被串改或过期
    if not payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data

    # 判断token正确性
    if "user_id" not in payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data
    # 获取新的token
    access_token = Auth.generate_access_token(user_id=payload["user_id"])
    data = {"access_token": access_token.decode("utf-8"), "refresh_token": refresh_token}
    res.update(data=data)
    return res.data


# --------------------测试微信登陆注册-------------------------------#

@route(bp, '/testWXLoginOrRegister', methods=["GET"])
def test_wx_login_or_register():
    """
    测试微信登陆注册
    :return:
    """
    res = ResMsg()
    code = request.args.get("code")
    flag = request.args.get("flag")
    # 参数错误
    if code is None or flag is None:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    # 获取微信用户授权码
    access_code = get_access_code(code=code, flag=flag)
    if access_code is None:
        res.update(code=ResponseCode.WeChatAuthorizationFailure)
        return res.data
    # 获取微信用户信息
    wx_user_info = get_wx_user_info(access_data=access_code)
    if wx_user_info is None:
        res.update(code=ResponseCode.WeChatAuthorizationFailure)
        return res.data

    # 验证微信用户信息本平台是否有，
    data = wx_login_or_register(wx_user_info=wx_user_info)
    if data is None:
        res.update(code=ResponseCode.Fail)
        return res.data
    res.update(data=data)
    return res.data