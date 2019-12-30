from app import app
from app.modules.Banner import Banner
from app.modules.Session import Session
from app.modules.User import User
from app.modules.Course import Course
from app.modules.Courseware import Courseware
from app.utils.MyResponse import *
from flask import request, render_template


@app.before_request
def authMidware():
    '''
    认证路由管理中间件
    如果请求的路由不在开放路由列表中需要经过认证
    openUrls:开放路由列表（不需要认证的路由）
    :return:
    '''
    openUrls = [
        "/v1/auth",
        "/v1/banner",
        "/v1/iclass/download",
        # "/test",
        "/"
    ]
    if request.path in openUrls:
        pass
    else:
        if not Session(request.headers.get("Token")).alive:
            return responseError(None, 401, "Unauthorized")


@app.route("/test")
def test():
    # Session.create()
    return "1234"
    pass
    # return make_response("Hello world")


@app.route("/v1/auth", methods=["POST"])
def auth():
    token = Session.create(request.form.get("code"))
    if token is None:
        return responseError(None, 401, "Unauthorized")
    else:
        return responseOK({"Token": token})


@app.route('/v1/banner', methods=["GET"])
def banner():
    """
    获取首页Banner新闻和notice通知条的信息
    """
    return responseOK(Banner.getAll())


@app.route("/v1/user", methods=["GET"])
def user():
    openid = Session(request.headers.get("Token")).openid
    return responseOK(User(openid).baseData)


@app.route("/v1/favorites/<type>", methods=["GET", "PUT", "DELETE"])
def favorites_type(type):
    if request.method == "GET":
        if type == "courseware":
            return responseOK(User(Session(request.headers.get("Token")).openid).getCourseware())
        elif type == "goods":
            pass
    elif request.method == "PUT":
        id = request.form.get("_id")
        if type == "courseware":
            cw = Courseware.getOne(id)
            if cw is None:
                return responseError(None, 404, "找不到这个文件")
            User(Session(request.headers.get("Token")
                         ).openid).addCourseware(str(cw["_id"]))
            return responseOK()
        elif type == "goods":
            pass
    elif request.method == "DELETE":
        id = request.args.get("_id")
        if type == "courseware":
            if User(Session(request.headers.get("Token")).openid).delCourseware(id):
                return responseOK()
            else:
                return responseError(None, 404, "该文件没有被收藏过")
        elif type == "goods":
            pass


@app.route("/v1/net", methods=["GET"])
def net():
    openid = Session(request.headers.get("Token")).openid
    return responseOK(User(openid).getNetInfo())


@app.route("/v1/iclass/course", methods=["GET"])
def iclass_course():
    """
    获取课程列表
    """
    openid = Session(request.headers.get("Token")).openid
    return responseOK(User(openid).getCourseList())


@app.route("/v1/iclass/homework", methods=["GET"])
def iclass_homework():
    course_codes = request.args.get("course_code").split(",")
    return responseOK(Course.getHomework(course_codes))


@app.route("/v1/iclass/courseware", methods=["GET"])
def iclass_course_code():
    return responseOK(Course.getCourseware(request.args.get("course_code")))


@app.route("/v1/iclass/courseware/download", methods=["GET", "POST"])
def iclass_courseCode_filename():
    if request.method == "GET":
        course_code = request.args.get("course_code")
        filename = request.args.get("filename")
        return responseFile(Courseware.privateDowmload(course_code, filename),
                            filename.encode("utf-8").decode("latin-1"))
    elif request.method == "POST":
        course_code = request.form.get("course_code")
        filename = request.form.get("filename")
        id = Courseware.makeUrl(course_code, filename)
        if id is not None:
            return responseOK({
                "id": id
            })
        else:
            return responseError(None, 404, "无法找到文件")


@app.route("/v1/iclass/download", methods=["GET"])
def iclass_download():
    id = request.args.get("id")
    filename, file = Courseware.publicDownload(id)
    if file is None:
        return render_template("failure.html")
    else:
        return responseFile(file, filename.encode("utf-8").decode("latin-1"))

# 以下是旧路由

# @app.route('/login/oauth')
# def auth():
#     '''
#     身份认证函数
#     '''
#     access_token = getYxAccess_token()
#     openid = request.args.get('state')
#     code = request.args.get('code')
#     userInfo = getUserInfo(code, access_token)
#     app.DB.setUserInfo(openid, userInfo)
#     return render_template("redirect.html", name=userInfo['name'])
#
#
# @app.route('/login/code')
# def getUserInfoByCode():
#     '''
#     服务器返回用户基本信息openid
#     '''
#     code = request.args.get('code')
#     openid = getOpenid(code)
#     app.DB.newUser(openid)
#     userData = app.DB.getUserInfo(openid)
#     return json.dumps(userData)
#
#
# @app.route("/login/openid")
# def getUserInfoByOpenid():
#     '''
#     通过openid获取用户基本信息
#     '''
#     openid = request.args.get('openid')
#     return json.dumps(app.DB.getUserInfo(openid))
#
#
# @app.route('/publicinfo')
# def getBannerAndNotice():
#     """
#     获取首页Banner新闻和notice滚动条的信息
#     """
#     return json.dumps(app.DB.getPublicInfo())
#
#
# @app.route('/courselist')
# def getCourseList():
#     """
#     获取课程列表
#     """
#     openid = request.args.get('openid')
#     data = {'sno': app.DB.getUserInfo(openid)['userid']}
#     courselist = json.loads(
#         requests.get('http://v.ncut.edu.cn/course', params=data).text)['data']
#     for course in courselist:
#         tmpList = course['course_name'].split('：')
#         course['course_name'] = '：'.join(tmpList[:-1])
#         course['course_class'] = tmpList[-1]
#     return json.dumps(courselist[::-1])
#
#
# @app.route('/homework')
# def getDocument():
#     """
#     获取作业列表
#     """
#     #请求所有的课程信息
#     openid = request.args.get('openid')
#     data = {'sno': (app.DB.getUserInfo(openid))['userid']}
#     res = requests.get('http://v.ncut.edu.cn/course', params=data).text
#     classlist = json.loads(res)
#     # 获取所有的课程编号添加到course_codes字典
#     course_codes = {}
#     for i in classlist["data"]:
#         data = {'code': i['course_code']}
#         assignment = json.loads(
#             requests.get('http://v.ncut.edu.cn/work',
#                          params=data).text)['data']
#         if assignment != []:
#             course_codes[i['course_name'].split('：')[0]] = assignment
#     return json.dumps(course_codes)
#
#
# @app.route('/coursewarelist')
# def getWareList():
#     """
#     获取当前课程所有的课件
#     """
#     openid = request.args.get('openid')
#     mode = request.args.get('mode')
#     if mode == 'all':
#         coursecode = request.args.get('course_code')
#         data = {'code': coursecode}
#         #请求到所有的课件字典
#         res = json.loads(
#             requests.get('http://v.ncut.edu.cn/document', params=data).text)
#     elif mode == 'dir':
#         courseware = json.loads(request.args.get('courseware'))
#         data = {'code': courseware['course_code'], 'item': courseware['sign']}
#         res = json.loads(
#             requests.get('http://v.ncut.edu.cn/document', params=data).text)
#     if res['data'] == []:
#         return json.dumps(None)
#     wareList = []
#     favourite = app.DB.getFavorite(openid)
#     favList = []
#     for item in favourite:
#         favList.append(item['url'])
#     for key, value in res['data'].items():
#         tempDict = value
#         quote = parseUrl(tempDict['url'].replace('%', '∫'))
#         tempDict['url'] = quote['url']
#         tempDict['course_code'] = quote['cidReq']
#         tempDict['file_name'] = key.split('/')[-1]
#         # 格式化文件大小
#         if tempDict['size'] < 1000000:
#             tempDict['size'] = '%.1fKB' % (tempDict['size'] / 1000)
#         else:
#             tempDict['size'] = '%.1fMB' % (tempDict['size'] / 1000000)
#         if tempDict['type'] != 'dir':
#             tempDict['type'] = key.split('.')[-1].lower()
#         if tempDict['url'] in favList:
#             tempDict['favourite'] = True
#         else:
#             tempDict['favourite'] = False
#         wareList.append(tempDict)
#     # 按照课件发布时间进行排序
#     wareList.sort(key=lambda k: (k.get('date', 0)), reverse=True)
#     # 格式化时间
#     for i in range(len(wareList)):
#         wareList[i]['date'] = time.strftime(
#             "%Y-%m-%d", time.localtime(wareList[i]['date']))
#     return json.dumps(wareList)
#
#
# @app.route('/courseware')
# def readCourseware():
#     """
#     浏览单个课件
#     """
#     openid = request.args.get('openid')
#     courseware = json.loads(request.args.get('courseware'))
#     res = document.downloadCourseware(courseware)
#     return make_response(res)
#
#
# @app.route('/favourite/courseware')
# def markCourseware():
#     """
#     收藏单个课件
#     """
#     openid = request.args.get('openid')
#     mode = request.args.get('mode')
#     if mode == 'add':
#         courseware = json.loads(request.args.get('courseware'))
#         app.DB.addCourseware(openid, courseware)
#     elif mode == 'del':
#         courseware = json.loads(request.args.get('courseware'))
#         app.DB.deleteCourseware(openid, courseware)
#     return "success"
#
#
# @app.route('/favourite/get')
# def getFavorite():
#     """
#     获取收藏夹
#     """
#     openid = request.args.get('openid')
#     return json.dumps(app.DB.getFavorite(openid))
#
#
# @app.route('/reqdownload')
# def reqDownload():
#     """
#     请求下载课件
#     params:openid,courseware(json)
#     :return id
#     """
#     openid = request.args.get('openid')
#     courseware = json.loads(request.args.get('courseware'))
#     id = uuid.uuid1().hex
#     app.DB.newFile(id, courseware)
#     return id
#
#
# @app.route('/download')
# def downloadFile():
#     """
#     下载课件
#     :return:file(json)
#     """
#     id = request.args.get('id')
#     downloadItem = app.DB.getFile(id)
#     if downloadItem is None:
#         return render_template("failure.html")
#     nowTime = time.time()
#     if nowTime - downloadItem['time'] <= VALIDTIME:
#         res = make_response(
#             document.downloadCourseware(downloadItem['courseware']))
#         res.headers[
#             'Content-Disposition'] = "attachment;filename=" + downloadItem[
#                 'courseware']['file_name'].encode("utf-8").decode("latin-1")
#         try:
#             res.headers['Content-type'] = FILE_TYPES[downloadItem['courseware']
#                                                      ['type']]
#         except:
#             pass
#         return res
#     else:
#         return render_template("failure.html")
#
#
# @app.route("/wifi")
# def getWifi():
#     '''
#     balance：钱包余额
#     expend：本月使用量
#     '''
#     openid = request.args.get("openid")
#     uid = app.DB.getUserInfo(openid)['userid']
#     # TODO 调成wifi返回数据
#     # return json.dumps({
#     #     "balance": schoolNet.getNetInfo(uid)[4],
#     #     "expend": schoolNet.getNetInfo(uid)[7]
#     # })
#     return schoolNet.getNetInfo(uid)[7]
#
#
# @app.route("/pay/reqpay/wifi", methods=['POST'])
# def payWifi():
#     '''
#     生成校网充值预支付订单
#     '''
#     openid = request.form["openid"]
#     pay_money = request.form["pay_money"]
#     sign = request.form["sign"]
#     if sign != pay.sign({"openid": openid, "pay_money": pay_money}):
#         return json.dumps({"e": 401, "m": "签名校验失败", "url": ""})
#     td = {
#         "pay_money":
#         pay_money,
#         "expire_time":
#         "10",
#         "notify_url":
#         "http://test.com",
#         "return_url":
#         "http://test.com",
#         "intro":
#         "wifi充值",
#         "out_trade_no":
#         pay.createTradeNo("01",
#                           app.DB.getUserInfo(openid=openid)["userid"]),
#         "attach":
#         openid
#     }
#     res = pay.reqPay(**td)
#     if res is None:
#         return json.dumps({"e": 403, "m": "订单创建失败", "url": ""})
#     app.DB.createTrade(openid, pay_money, td["out_trade_no"], res)
#     return json.dumps({"e": 0, "m": "", "url": res})
#
#
# @app.route("/pay/history/wifi")
# def wifiTradeHistory():
#     '''
#     查询wifi充值交易历史信息
#     '''
#     openid = request.args.get("openid")
#     return json.dumps(app.DB.getTradeHistory(openid, "01"))
