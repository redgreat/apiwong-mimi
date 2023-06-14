#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw 
# @generate at 2023/6/1 15:40

import logging
from flask import Blueprint, jsonify, session, request, current_app
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import select, text

from app.utils.core import db
from app.models.model import Carlocdaily
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.util import route
from app.celery import add, flask_app_context

bp = Blueprint("product", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


@route(bp, '/locapi/v1/<imei>/<start_time>&<end_time>', methods=["GET"])
def getloc(imei, start_time, end_time):
    res = ResMsg()
    locs = db.session.execute(select(Carlocdaily.lng,Carlocdaily.lat,Carlocdaily.speed,Carlocdaily.dev_upload).where(Carlocdaily.device_id == imei).where(Carlocdaily.dev_upload >= start_time).where(Carlocdaily.dev_upload < end_time).order_by(Carlocdaily.dev_upload))
    result = []
    for loc in locs:
        #dict = {'lng': loc.lng, 'lat': loc.lat, 'speed': loc.speed, 'loctime': loc.dev_upload}
        list = [float(loc.lng), float(loc.lat)]
        result.append(list)
    res.update(code=ResponseCode.Success, data=result)
    return res.data

@route(bp, '/testCeleryAdd', methods=["GET"])
def test_add():
    """
    测试相加
    :return:
    """
    result = add.delay(1, 2)
    return result.get(timeout=1)

@route(bp, '/testCeleryFlaskAppContext', methods=["GET"])
def test_flask_app_context():
    """
    测试获取flask上下文
    :return:
    """
    result = flask_app_context.delay()
    return result.get(timeout=1)

@route(bp, '/locapi/v2/<imei>/<start_time>&<end_time>&<page>', methods=["GET"])
def getlocate(imei, start_time, end_time, page):
    res = ResMsg()
    page_size = current_app.config['DEFAULT_PAGE_SIZE']
    sql_text = text('SELECT lng, lat \
    FROM carlocdaily \
    WHERE device_id = :imei \
    AND dev_upload >= :start_time \
        AND dev_upload < :end_time \
    ORDER BY dev_upload \
    LIMIT :page, :page_size;')
    locs = db.session.execute(sql_text.params(imei=imei, start_time=start_time, end_time=end_time, page=int(page), page_size=page_size))
    result=[]
    for loc in locs:
        list = [float(loc.lng), float(loc.lat)]
        result.append(list)
    res.update(code=ResponseCode.Success, data=result)
    return res.data

@route(bp, '/testconfig', methods=["GET"])
def test_config():
    """
    测试配置文件读取
    """
    res = ResMsg()
    result = current_app.config['DEFAULT_PAGE_SIZE']
    res.update(code=ResponseCode.Success, data=result)
    return res.data
