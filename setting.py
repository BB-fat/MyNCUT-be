
DEBUG=False

if DEBUG:
    DATABASEIP = '10.211.55.5'
else:
    DATABASEIP = '10.102.1.35'
    DB_USER = "myncut"
    DB_PASSWD = "myNCUT@wx315wdbf"

yxAPPID = '31b1e992583074382'

yxAPPSECRET = 'f5e030ee903dbc29c6e76375253d1ee6'

DATABASEPORT=27017

wxAPPID="wx12bef97a98001f0b"

wxAPPSECRET="dbd5ecc6424d1ce668c93e7f98120c53"

VALIDTIME=300

EMAIL_SERVER='smtp.qq.com'
EMAIL_PORT='465'
EMAIL_USERNAME='1056871944@qq.com'
EMAIL_PASSWD='snjpnnztwsnxbbbf'
EMAIL_TO_ADDRESS=['1056871944@qq.com']

FILE_TYPES = {
    'pdf': 'application/pdf',
    'ppt': 'application/x-ppt',
    'pptx': 'application/x-ppt',
    'doc': 'application/msword',
    'docx': 'application/msword',
    'zip': 'application/zip',
    'xls': 'application/x-xls',
    'xlsx': 'application/x-xls',
    'avi':'video/avi',
    'jpg':'image/jpeg',
    'mp4':'video/mpeg4',
    'rar':'application/octet-stream'
}