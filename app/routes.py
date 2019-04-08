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
    pass

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



@app.route('/courselist')
def getCourseList():
    """
    获取课程列表
    """
    openid=request.args.get('openid')
    data = {
         'sno':(mongoClient().getUserInfo(openid))['userInfo']['userid']
    }
    res= requests.get('http://v.ncut.edu.cn/course',params=data).text
    return res


@app.route('/homework')
def getDocument():
    """
    获取作业列表
    """
    #请求所有的课程信息
    openid = request.args.get('openid')
    data = {
        'sno':(mongoClient().getUserInfo(openid))['userInfo']['userid']
    }
    res = requests.get('http://v.ncut.edu.cn/course', params=data).text
    classlist=json.loads(res)
    # 获取所有的课程编号添加到course_codes字典
    course_codes = {}
    for i in classlist["data"]:
        data = {
            'code': i['course_code']
        }
        course_codes[i['course_name']] = json.loads(requests.get('http://v.ncut.edu.cn/work', params=data).text)['data']
    return json.dumps(course_codes)


@app.route('/coursewarelist')
def getWareList():
    """
    获取当前课程所有的课件
    """
    openid = request.args.get('openid')
    coursecode = request.args.get('coursecode')
    data = {
        'code' :coursecode
    }
    #请求到所有的课件字典
    res = requests.get('http://v.ncut.edu.cn/document', params=data).text
    #将课件字典其中的url的"&"取地址符换成"¥"符号
    coursewarelist = json.loads(res)
    for key in coursewarelist['data']:
        coursewarelist['data'][key]['url'] = coursewarelist['data'][key]['url'].replace('&', '¥')
    return json.dumps(coursewarelist)


@app.route('/courseware')
def readCourseware():
    """
    浏览单个课件
    """
    openid = request.args.get('openid')
    course = json.loads(request.args.get('course'))
    #将字典中的"¥"符号换成"&"取地址符，再返回课件的二进制数据
    url = course['url'].replace('¥', '&')
    print(url)
    res=requests.get(url).content
    return make_response(res)


@app.route('/favourite/courseware')
def markCourseware():
    """
    收藏单个课件
    """
    openid = request.args.get('openid')
    course = json.loads(request.args.get('course'))
    mode = request.args.get('mode')
    if mode == 'add':
        mongoClient.addCourseware(openid,course)


@app.route('/favourite/courseware')
def deleteCourseware():
    """
    删除收藏的课件
    """
    openid = request.args.get('openid')
    course = json.loads(request.args.get('course'))
    mode = request.args.get('mode')
    if mode == 'del':
        mongoClient.deleteCourseware(openid,course)
