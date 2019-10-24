# -*- coding: utf-8 -*-
import requests
import base64

def str2b64(s):
    return base64.b64encode((s).encode("utf-8")).decode()

def getNetInfo(uid):
    '''
    传入学号，得到校园网流量信息
    返回的列表中索引7对应的数值为本月已用流量，单位MB
    :param uid:
    :return:
    '''
    res = requests.get("http://10.0.12.3/DrcomSrv/DrcomServlet?business=" + str2b64("091"+uid)).text
    return res.split("\t")

def recharge(uid,amount,order):
    '''
    校网钱包充值
    uid：学号
    amount：充值金额（分）
    order：流水号
    '''
    parts=[
        "010"+uid,
        amount,
        '0',
        '6666',
        order
    ]
    print(" ".join(parts))
    res = requests.get("http://10.0.12.3/DrcomSrv/DrcomServlet?business=" + str2b64("\t".join(parts))).text
    return res.split("\t")

if __name__=="__main__":
    # parts=[
    #     "010001996",
    #     "100",
    #     '0',
    #     '6666',
    #     "200902190008"
    # ]
    # print(recharge("1520173431","100","00001"))
    # print(str2b64("\t".join(parts)))
    print(getNetInfo("17152010921"))