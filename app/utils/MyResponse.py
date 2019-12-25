import json
from flask import make_response


def responseOK(data):
    '''
    请求成功的响应
    :param data: data字段携带的数据
    :return:
    '''
    return json.dumps({
        "code": 200,
        "m": "",
        "data": data
    })


def responseError(data, code: int, m: str):
    '''
    请求失败的响应
    :param data: 携带的数据
    :param code: 响应代码
    :param m: 错误信息
    :return:
    '''
    return json.dumps({
        "code": code,
        "m": m,
        "data": data
    })


def responseFile(file, filename):
    res = make_response(file)
    res.headers['Content-Disposition'] = "attachment;filename=" + filename
    return res
