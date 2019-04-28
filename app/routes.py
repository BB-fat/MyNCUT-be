from flask import request,render_template,Response,make_response
from util.login import *
from util.mongoClient import *
import json
from util.parseurl import parseUrl
import uuid

# 登陆成功的网页路由函数
from app.templates.loginsuccess.routes import *

# 首页轮播图图片路由函数
from static.publicinfo.routes import *

# 下载超时页面图片路由函数
from static.failure.routes import *

@app.route('/')
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
    print(userInfo)
    app.DB.newUser(openid,userInfo)
    return render_template("loginsuccess/redirect.html",name=userInfo['name'])

@app.route('/login/code')
def getUserInfoByCode():
    '''
    服务器返回openid和用户基本信息
    '''
    code=request.args.get('code')
    openid=getOpenid(code)
    userInfo=app.DB.getUserInfo(openid)
    userInfoTemp={
        'openid':openid,
        'userInfo':userInfo
    }
    return json.dumps(userInfoTemp)

@app.route("/login/openid")
def getUserInfoByOpenid():
    '''
    通过openid获取用户基本信息
    '''
    openid=request.args.get('openid')
    return json.dumps(app.DB.getUserInfo(openid))

@app.route('/publicinfo')
def getBannerAndNotice():
    """
    获取首页Banner新闻和notice滚动条的信息
    """
    return json.dumps(app.DB.getPublicInfo())



@app.route('/courselist')
def getCourseList():
    """
    获取课程列表
    """
    openid=request.args.get('openid')
    data = {
         'sno':app.DB.getUserInfo(openid)['userInfo']['userid']
    }
    courselist = json.loads(requests.get('http://v.ncut.edu.cn/course',params=data).text)['data']
    for course in courselist:
        course['course_name'],course['course_class']=course['course_name'].split('：')
    return json.dumps(courselist)




@app.route('/homework')
def getDocument():
    """
    获取作业列表
    """
    #请求所有的课程信息
    openid = request.args.get('openid')
    data = {
        'sno':(app.DB.getUserInfo(openid))['userInfo']['userid']
    }
    res = requests.get('http://v.ncut.edu.cn/course', params=data).text
    classlist=json.loads(res)
    # 获取所有的课程编号添加到course_codes字典
    course_codes = {}
    for i in classlist["data"]:
        data = {
            'code': i['course_code']
        }
        assignment  = json.loads(requests.get('http://v.ncut.edu.cn/work', params=data).text)['data']
        if assignment !=[]:
            course_codes[i['course_name']] = assignment
    return json.dumps(course_codes)



@app.route('/coursewarelist')
def getWareList():
    """
    获取当前课程所有的课件
    """
    openid = request.args.get('openid')
    mode=request.args.get('mode')
    if mode=='all':
        coursecode = request.args.get('coursecode')
        data = {
            'code' :coursecode
        }
        #请求到所有的课件字典
        res = json.loads(requests.get('http://v.ncut.edu.cn/document', params=data).text)
    elif mode=='dir':
        courseware=json.loads(request.args.get('courseware'))
        data={
            'code':courseware['coursecode'],
            'item':courseware['sign']
        }
        res = json.loads(requests.get('http://v.ncut.edu.cn/document', params=data).text)
    if res['data']==[]:
        return json.dumps(None)
    wareList=[]
    favourite=app.DB.getFavorite(openid)['courseware']
    favList=[]
    for item in favourite:
        favList.append(item['url'])
    for key,value in res['data'].items():
        tempDict=value
        quote=parseUrl(tempDict['url'].replace('%','∫'))
        tempDict['url']=quote['url']
        tempDict['coursecode']=quote['cidReq']
        tempDict['file_name'] = key.split('/')[-1]
        if tempDict['type']!='dir':
            tempDict['type'] = key.split('.')[-1]
        if tempDict['url'] in favList:
            tempDict['favourite']=True
        else:
            tempDict['favourite']=False
        wareList.append(tempDict)
    return json.dumps(wareList)


@app.route('/courseware')
def readCourseware():
    """
    浏览单个课件
    """
    openid = request.args.get('openid')
    courseware = json.loads(request.args.get('courseware'))
    data={
        'cidReset':True,
        'cidReq':courseware['coursecode']
    }
    res=requests.get('http://iclass.ncut.edu.cn/iclass/netclass/backends/download_api.php?url='+courseware['url'].replace("∫",'%'),params=data).content
    return make_response(res)


@app.route('/favourite/courseware')
def markCourseware():
    """
    收藏单个课件
    """
    openid = request.args.get('openid')
    mode = request.args.get('mode')
    if mode == 'add':
        courseware = json.loads(request.args.get('courseware'))
        app.DB.addCourseware(openid,courseware)
    elif mode=='del':
        index=request.args.get('index')
        app.DB.deleteCourseware(openid,index)
    return "success"

@app.route('/favourite/get')
def getFavorite():
    """
    获取收藏夹
    """
    openid = request.args.get('openid')
    return json.dumps(app.DB.getCourseware(openid))

@app.route('/feedback')
def submitFeedback():
    """
    提交反馈
    """
    data = {
        'type' : request.args.get('type'),
        'openid' :request.args.get('openid'),
        'time' :request.args.get('time'),
        'text':request.args.get('text')
    }
    app.DB.saveFeedback(data)
    return "success"

@app.route('/reqdownload')
def requestDownload():
    """
    请求下载课件
    params:openid,courseware(json)
    :return id
    """
    openid = request.args.get('openid')
    courseware = request.args.get('courseware')
    id = uuid.uuid1()
    app.DB.newfile(id, courseware)
    return id

@app.route('/download')
def downloadfile():
    """
    下载课件
    :return:file(json)
    """
    id = request.args.get('id')
    #不确定的地方3.1  返回的是json字符串是吗？ 是的话，我就需要把json变成列表，然后再将积分符号换回来。
    file = json.loads(app.DB.getfile(id))
    data = {
        'cidReset': True,
        'cidReq': file['coursecode']
    }
    #不确定的地方3.2 文件的格式用在哪里呢？
    type = file['type']
    # 不确定的地方3.3 如何返回给前端一个文件
    url = requests.get('http://iclass.ncut.edu.cn/iclass/netclass/backends/download_api.php?url=' + file['url'].replace("∫", '%'),params=data).content
    return url




