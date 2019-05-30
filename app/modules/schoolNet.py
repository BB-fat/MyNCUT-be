import requests
import base64

def getNetInfo(uid):
    '''
    传入学号，得到校园网流量信息
    返回的列表中索引7对应的数值为本月已用流量，单位MB
    :param uid:
    :return:
    '''
    b = base64.b64encode(("091"+uid).encode("utf-8")).decode()
    res = requests.get("http://10.0.12.3/DrcomSrv/DrcomServlet?business=" + b).text
    return res.split("\t")