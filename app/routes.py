from flask import request,render_template
from util.login import *
from util.mongoClient import *
import json

# 登陆成功的网页路由函数
from app.templates.loginsuccess.routes import *

# 首页轮播图图片路由函数
from static.publicinfo.routes import *

@app.route('/login/')
def test():
    return render_template("loginsuccess/redirect.html",name='bbfat')

@app.route('/login/oauth')
def oauth():
    '''
    身份认证函数
    '''
    access_token=getAccess_token()
    openid=request.args.get('state')
    code=request.args.get('code')
    userInfo=getUserInfo(code,access_token)
    mongoClient().newUser(openid,userInfo)
    return render_template("loginsuccess/redirect.html",name=userInfo['name'])

@app.route('/login/code')
def getUserInfoByCode():
    '''
    服务器返回openid和用户基本信息
    '''
    code=request.args.get('code')
    openid=getOpenid(code)
    userInfo=mongoClient().getUserInfo(openid)
    userInfoTemp={
        'openid':openid,
        'userInfo':userInfo,
    }
    return json.dumps(userInfoTemp)

@app.route("/login/openid")
def getUserInfoByOpenid():
    '''
    通过openid获取用户基本信息
    '''
    openid=request.args.get('openid')
    return json.dumps(mongoClient().getUserInfo(openid))

@app.route('/publicinfo')
def getBannerAndNotice():
    """
    获取首页Banner新闻和notice滚动条的信息
    """
    return json.dumps(mongoClient().getPublicInfo())




@app.route('/course')
def getCourseList():
    """
    Parameters：openid
    获取课程列表
    """
    openid=request.args.get('openid')
    sno=(mongoClient().getUserInfo(openid))['userInfo']['uid']
    res= request.get('http://v.ncut.edu.cn/course',params=sno).text
    return json.dumps(res)


@app.route('/homework')
def getDocument():
    """
    获取作业列表
    """
    #请求所有的课程信息
    openid = request.args.get('openid')
    sno = (mongoClient().getUserInfo(openid))['userInfo']['uid']
    res = request.get('http://v.ncut.edu.cn/course', params=sno)
    classlist=json.loads(res)
    # 获取所有的课程编号到course_codes列表
    index = 0
    course_codes = []
    for i in classlist["data"]:
        course_codes.append(classlist["data"][index]["course_code"])
        index = index + 1
    #从服务器获取课程作业-----------为了json.dumps把assignment做成字典了，key是1，2，3...------
    assignment = {}
    for i in  course_codes:
        code =  course_codes[i]
        assignment[i] = request.get('http://v.ncut.edu.cn/course',params=code).text
    return json.dumps(assignment)


@app.route('/coursewarelist')
def getWareList():
    """
    Parameters：openid、coursecode
    获取当前课程所有的课件
    """
    #接受前端的参数
    openid = request.args.get('openid')
    coursecode = request.args.get('coursecode')
    #从服务器获取当前的课程列表
    #---------------看到我们这里的接口文档接受的参数是coursecode，但是多模式的接口是code，
    #所以不然换成同一个名字好让我用params直接传进去，还是我对params有什么误解。。？
    code = coursecode
    res = request.get('http://v.ncut.edu.cn/document', params=code)
    return json.dumps(res.text)


@app.route('/courseware')
def readCourseware():
    """
    Parameters：openid、course（课件字典）
    浏览单个课件
    """
    # 接受前端的参数
    openid = request.args.get('openid')
    course = request.args.get('course')
    #返回课件的二进制数据------------怎么写二进制--为什么还给openid----------？？？？？？？--------------------------
    res=request.get(course["url"]).text
    return json.dumps(res)


@app.route('/favourite/courseware')
def collectCourseware():
    """
    Parameters：openid、mode=add、course（课件字典）
    收藏单个课件
    """
    # 接受前端的参数
    openid = request.args.get('openid')
    course = request.args.get('course')
    mode = request.args.get('mode')
    #调用数据库存储文件
    if mode == 'add':
        mongoClient.saveCourseware(openid,course)


@app.route('/favourite/courseware')
def deleteCourseware():
    """
    Parameters：openid、mode=del、course（课件字典）
    删除收藏的课件
    """
    # 接受前端的参数
    openid = request.args.get('openid')
    course = request.args.get('course')
    mode = request.args.get('mode')















