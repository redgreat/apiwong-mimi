# coding: utf-8
# from datetime import datetime
from app.utils.core import db


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户表'}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='自增主键')
    name = db.Column(db.String(20), nullable=False, comment='用户姓名')
    age = db.Column(db.Integer, nullable=False, comment='用户年龄')


class UserLoginMethod(db.Model):
    __tablename__ = 'user_login_method'
    __table_args__ = {'comment': '用户登陆验证表'}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='用户登陆方式主键ID')
    user_id = db.Column(db.Integer, nullable=False, comment='用户主键ID')
    login_method = db.Column(db.String(36), nullable=False, comment='用户登陆方式，WX微信，P手机')
    identification = db.Column(db.String(36), nullable=False, comment='用户登陆标识，微信ID或手机号')
    access_code = db.Column(db.String(36), nullable=True, comment='用户登陆通行码，密码或token')


class ChangeLogs(db.Model):
    __tablename__ = 'change_logs'
    __table_args__ = {'comment': '修改日志'}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='自增主键')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='作者')
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), comment='文章')
    modify_content = db.Column(db.String(255), nullable=False, comment='修改内容')
    create_time = db.Column(db.DateTime, nullable=False, comment='创建日期')

class Carlocdaily(db.Model):
    __tablename__ = 'carlocdaily'
    __table_args__ = {'comment': '车辆日常定位信息'}

    dev_upload = db.Column(db.DateTime, primary_key=True, comment='设备上传时间(主键)')
    device_id = db.Column(db.String(20), comment='设备Id(ICCID)')
    lat = db.Column(db.DECIMAL(9, 6), comment='经度')
    lng = db.Column(db.DECIMAL(9, 6), comment='纬度')
    dirct = db.Column(db.Integer, comment='方向角')
    speed = db.Column(db.Integer, comment='速度')
    mileage = db.Column(db.DECIMAL(18, 2), comment='里程')
    hight = db.Column(db.Integer, comment='海拔')
    gnss_num = db.Column(db.Integer, comment='GPS卫星数量')
    rssi = db.Column(db.Integer, comment='4G信号值')
    serv_receive = db.Column(db.DateTime, comment='GateWay处理时间')
    data_insert = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"), comment='数据写入时间')


class Watchdaily(db.Model):
    __tablename__ = 'watchdaily'
    __table_args__ = {'comment': '手表日常数据'}

    UtcTime = db.Column(db.DateTime, primary_key=True, comment='数据获取时间')
    Steps = db.Column(db.String(50), comment='步数')
    Heartbeat = db.Column(db.String(50), comment='心率')
    Roll = db.Column(db.String(50), comment='翻转数')
    BodyTemperature = db.Column(db.String(50), comment='体温')
    WristTemperature = db.Column(db.String(50), comment='腕温')
    BloodSugar = db.Column(db.String(50), comment='血糖')
    Diastolic = db.Column(db.String(50), comment='舒张压')
    Shrink = db.Column(db.String(50), comment='收缩压')
    BloodOxygen = db.Column(db.String(50), comment='血氧')
    SleepType = db.Column(db.String(50), comment='睡眠类型(1深度睡眠2浅度睡眠3醒来时长)')
    SleepStartTime = db.Column(db.String(50), comment='睡眠开始时间')
    SleepEndTime = db.Column(db.String(50), comment='睡眠结束时间')
    SleepMinute = db.Column(db.String(50), comment='睡眠时长(分钟)')
    Signal = db.Column(db.String(50), comment='信号值')
    Battery = db.Column(db.String(50), comment='电池电量')
    Lat = db.Column(db.String(50), comment='定位纬度(GPS)')
    Lng = db.Column(db.String(50), comment='定位经度(GPS)')
    Speed = db.Column(db.String(50), comment='速度')
    InsertTime = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='数据写入时间')