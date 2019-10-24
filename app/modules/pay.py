#!/usr/bin/env python

import requests
from setting import *
import hashlib
import random
import time
import json


def sign(params):
    '''
    对队列参数进行签名
    '''
    l = sorted(params)
    s = ""
    for k in l:
        s += k + "=" + params[k] + "&"
    s += "key=" + payAPPSECRET
    res = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()
    return res.upper()


def reqPay(pay_money, expire_time, notify_url, return_url, intro, out_trade_no,
           attach):
    '''
    生成预支付订单
    文档详见http://doc.campusapp.com.cn/index.php?s=/3&page_id=280
    '''
    data = {
        "appid": payAPPID,
        "pay_money": pay_money,
        "expire_time": expire_time,
        "notify_url": notify_url,
        "return_url": return_url,
        "intro": intro,
        "out_trade_no": out_trade_no,
        "attach": attach
    }
    data['signature'] = sign(data)
    res = json.loads(
        requests.post("https://ucpay.ncut.edu.cn/pay/api/index/preorder",
                      data=data).text)
    if res["e"] != 0:
        return None
    return "https://ucpay.ncut.edu.cn/pay/wap/order/index?appid=%s&preorder=%s&signature=%s" % (
        payAPPID, res["d"], sign({
            "appid": payAPPID,
            "preorder": str(res['d'])
        }))


def createTradeNo(type, userid):
    '''
    生成订单号，订单号格式如下：
    2位交易类型+Unix时间戳后六位+学号后5位+3位随机数
    '''
    return type + str(int(time.time()))[-6:] + userid[-5:] + str(
        random.randint(100, 999))


if __name__ == "__main__":
    td = {
        "pay_money": "1",
        "expire_time": "10",
        "notify_url": "http://test.com",
        "return_url": "http://test.com",
        "intro": "wifi充值",
        "out_trade_no": "1715201092120190613232123",
        "attach": r"{}"
    }
    # print(reqPay(**td))
    # print(sign({
    #     "foo": "value1",
    #     "bar": "value2",
    #     "baz": "value3"
    # }, "12345678"))
    print(sign({"openid": "o1Glo5BZgdDoVqkuXgKzSw_r4T_M", "pay_money": "100"}))
    # print(hashlib.md5("".encode(encoding='UTF-8')).hexdigest().upper())
    # print(createTradeNo("01","17152010921"))