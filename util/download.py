import requests

def downloadCourseware(courseware):
    '''
    传入课件字典
    返回课件的二进制数据
    :param courseware:
    :return:
    '''
    data={
        'cidReset':True,
        'cidReq':courseware['coursecode']
    }
    res=requests.get('http://iclass.ncut.edu.cn/iclass/netclass/backends/download_api.php?url='+courseware['url'].replace("∫",'%'),params=data).content
    return res