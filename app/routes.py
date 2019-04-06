from flask import request,render_template,Response,make_response
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
    data = {
         'sno':(mongoClient().getUserInfo(openid))['userInfo']['uid']
    }
    res= requests.get('http://v.ncut.edu.cn/course',params=data).text
    return json.dumps(res)


@app.route('/homework')
def getDocument():
    """
    获取作业列表
    """
    #请求所有的课程信息
    openid = request.args.get('openid')
    data = {
        'sno':mongoClient().getUserInfo(openid)['userInfo']['uid']
    }
    res = requests.get('http://v.ncut.edu.cn/course', params=data).text
    classlist=json.loads(res)
    # 获取所有的课程编号到course_codes列表
    course_codes = {}
    for i in classlist["data"]:
        data = {
            'code': i['course_code']
        }
        course_codes[i['course_name']] = (i['course_code'])
        course_codes[i['course_code']] = requests.get('http://v.ncut.edu.cn/work',params=data).text
    #从服务器获取课程作业
    return json.dumps(course_codes)


@app.route('/coursewarelist')
def getWareList():
    """
    获取当前课程所有的课件
    """
    openid = request.args.get('openid')
    coursecode = request.args.get('coursecode').text
    data = {
        'code' :coursecode
    }
    res = requests.get('http://v.ncut.edu.cn/document', params=data)
    return json.dumps(res.text)


@app.route('/courseware')
def readCourseware():
    """
    Parameters：openid、course（课件字典）
    浏览单个课件
    """
    openid = request.args.get('openid')
    course = json.loads(request.args.get('course'))
    #返回课件的二进制数据
    url = course['url']
    res=requests.get(url).content
    return make_response(res)



@app.route('/favourite/courseware')
def BookmarkCourseware():
    """
    Parameters：openid、mode=add、course（课件字典）
    收藏单个课件
    """
    openid = request.args.get('openid')
    course = json.loads(request.args.get('course'))
    mode = request.args.get('mode')
    if mode == 'add':
        mongoClient.saveCourseware(openid,course)


@app.route('/favourite/courseware')
def deleteCourseware():
    """
    Parameters：openid、mode=del、course（课件字典）
    删除收藏的课件
    """
    openid = request.args.get('openid')
    course = json.loads(request.args.get('course'))
    mode = request.args.get('mode')
    if mode == 'delete':
        mongoClient.deleteCourseware(openid,course)
















