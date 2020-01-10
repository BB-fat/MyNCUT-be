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
    if request.path in openUrls or "static" in request.path:
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


@app.route("/v1/auth", methods=["GET", "POST"])
def auth():
    if request.method == "GET":
        openid = Session.getOpenid(request.args.get("state"))
        if openid is None:
            return responseError(None, 401, "Unauthorized")
        u = User.OAuth(openid, request.args.get("code"))
        return render_template("redirect.html", name=u.name)
    elif request.method == "POST":
        token = Session.create(request.form.get("code"))
        if token is None:
            return responseError(None, 401, "Unauthorized")
        elif User(Session(token).openid).avatarUrl is None:
            return responseError({"Token": token}, 402, "需要授权信息")
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
        id = request.form.get("_id")
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
        cw = Courseware.getOne(request.args.get("id"))
        if cw is None:
            return responseError(None, 404, "无法找到文件")
        return responseFile(Courseware.fileStream(cw), cw["filename"].encode("utf-8").decode("latin-1"), cw["size"])
    elif request.method == "POST":
        id1 = request.args.get("id")
        id2 = Courseware.makeUrl(id1)
        if id2 is not None:
            return responseOK({
                "id": id2
            })
        else:
            return responseError(None, 404, "无法找到文件")


@app.route("/v1/iclass/download", methods=["GET"])
def iclass_download():
    realId = Courseware.publicDownload(request.args.get("id"))
    if realId is None:
        return render_template("failure.html")
    else:
        cw = Courseware.getOne(realId)
        return responseFile(Courseware.fileStream(cw), cw["filename"].encode("utf-8").decode("latin-1"), cw["size"])
