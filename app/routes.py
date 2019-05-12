from flask import request,render_template,make_response
from util.login import *
from util.mongoClient import *
import json
import uuid

from util.download import *
from util.parseurl import parseUrl
from setting import *
from util.schoolNet import *

# 首页轮播图图片路由函数
from static.publicinfo.routes import *


@app.route("/download/")
def test():
    return send_file("../static/failure/failure.html")


@app.route('/kSyoZqkJwk.txt')
def wxAuth():
    '''
    微信业务域名认证文件
    :return:
    '''
    return send_file('kSyoZqkJwk.txt')
    pass

@app.route('/login/oauth')
def auth():
    '''
    身份认证函数
    '''
    access_token=getAccess_token()
    openid=request.args.get('state')
    code=request.args.get('code')
    userInfo=getUserInfo(code,access_token)
    app.DB.setUserInfo(openid,userInfo)
    return render_template("loginsuccess/redirect.html",name=userInfo['name'])

@app.route('/login/<path:subpath>')
def show_loginsuccess(subpath):
    '''
    辅助加载认证成功页面
    :param subpath:
    :return:
    '''
    return send_file("templates/loginsuccess/"+subpath)

@app.route('/login/code')
def getUserInfoByCode():
    '''
    服务器返回用户基本信息openid
    '''
    code=request.args.get('code')
    openid=getOpenid(code)
    app.DB.newUser(openid)
    userData=app.DB.getUserInfo(openid)
    return json.dumps(userData)

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
        tmpList=course['course_name'].split('：')
        course['course_name']='：'.join(tmpList[:-1])
        course['course_class'] =tmpList[-1]
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
            course_codes[i['course_name'].split('：')[0]] = assignment
    return json.dumps(course_codes)



@app.route('/coursewarelist')
def getWareList():
    """
    获取当前课程所有的课件
    """
    openid = request.args.get('openid')
    mode=request.args.get('mode')
    if mode=='all':
        coursecode = request.args.get('course_code')
        data = {
            'code' :coursecode
        }
        #请求到所有的课件字典
        res = json.loads(requests.get('http://v.ncut.edu.cn/document', params=data).text)
    elif mode=='dir':
        courseware=json.loads(request.args.get('courseware'))
        data={
            'code':courseware['course_code'],
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
        tempDict['course_code']=quote['cidReq']
        tempDict['file_name'] = key.split('/')[-1]
        # 格式化文件大小
        if tempDict['size']<1000000:
            tempDict['size'] = '%.1fKB' % (tempDict['size'] / 1000)
        else:
            tempDict['size']='%.1fMB'%(tempDict['size']/1000000)
        if tempDict['type']!='dir':
            tempDict['type'] = key.split('.')[-1].lower()
        if tempDict['url'] in favList:
            tempDict['favourite']=True
        else:
            tempDict['favourite']=False
        wareList.append(tempDict)
    # 按照课件发布时间进行排序
    wareList.sort(key=lambda k: (k.get('date', 0)),reverse=True)
    # 格式化时间
    for i in range(len(wareList)):
        wareList[i]['date'] = time.strftime("%Y-%m-%d", time.localtime(wareList[i]['date']))
    return json.dumps(wareList)


@app.route('/courseware')
def readCourseware():
    """
    浏览单个课件
    """
    openid = request.args.get('openid')
    courseware = json.loads(request.args.get('courseware'))
    res=downloadCourseware(courseware)
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
        courseware=json.loads(request.args.get('courseware'))
        app.DB.deleteCourseware(openid,courseware)
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
    courseware = json.loads(request.args.get('courseware'))
    id = uuid.uuid1().hex
    app.DB.newFile(id, courseware)
    return id

@app.route('/download')
def downloadfile():
    """
    下载课件
    :return:file(json)
    """
    id = request.args.get('id')
    downloadItem = app.DB.getFile(id)
    if downloadItem is None:
        return send_file("../static/failure/failure.html")
    nowTime=time.time()
    if nowTime-downloadItem['time']<=VALIDTIME:
        res=make_response(downloadCourseware(downloadItem['courseware']))
        res.headers['Content-Disposition']="attachment;filename="+downloadItem['courseware']['file_name'].encode("utf-8").decode("latin-1")
        try:
            res.headers['Content-type']=FILE_TYPES[downloadItem['courseware']['type']]
        except:
            pass
        return res
    else:
        return send_file("../static/failure/failure.html")

@app.route('/download/<path:subpath>')
def show_failure(subpath):
    '''
    辅助加载下载失败页面
    :param subpath:
    :return:
    '''
    return send_file("../static/failure/"+subpath)


@app.route("/wifi")
def getWifi():
    openid=request.args.get("openid")
    uid=app.DB.getUserInfo(openid)['userInfo']['userid']
    return getNetInfo(uid)[7]

@app.route("/getauth")
def getAuth():
    return app.DB.getPasswd()

@app.route("/storedata",methods=['POST'])
def storeData():
    tempInfo =request.form
    if tempInfo['type']== 'banner':
        print("ok_1")
        app.DB.saveIndexBanner(tempInfo)
    else:
        print("ok_2")
        app.DB.saveIndexNotice(tempInfo)
    return "scucess"


