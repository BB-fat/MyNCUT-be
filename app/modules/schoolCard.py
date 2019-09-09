import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def getBalance(userid):
    c11 = cx_Oracle.connect("MYNUCT", "AQU1m0Lhp8","10.100.0.1/orcl").cursor()
    sql='''
    select "YHBH","YE" from DBM.V_YKT_YHYEXX WHERE YHBH='{}'
    '''.format(userid)
    res=c11.execute(sql).fetchone()
    return res