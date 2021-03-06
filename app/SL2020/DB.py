# -*- coding: utf-8 -*-
import cx_Oracle
import os
import json
import time
import hashlib
import requests
from lxml import etree
import datetime

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

"""
{'stu_id': '17159010325',
'name': '韩孟男',
'sex': '男',
'graduate_time': '2021', 
'entrance_time': '201709',
'province': '辽宁省', 
'institude': '计算机学院', 
'mayjor': '计算机科学与技术', 
'clazz': '计17-3', 
'highest_lesson_name': '高等代数与解析几何Ⅰ', 
'highest_lesson_score': 96, 
'lowest_lesson_name': '中国近现代史纲要', 
'lowest_lesson_score': 73, 
'first_lesson_name': '高等代数与解析几何Ⅰ', 
'first_lesson_loaction': '瀚学0110', 
'same_name_num': 0, 
'same_birthday_num': 6, 
'total_network': 378, 
'most_use_network_time': '01', 
'most_use_network_month': 53, 
'total_consume_times': 1211, 
'total_consume_money': 8043.66, 
'first_consume_times': datetime.datetime(2017, 9, 5, 20, 31, 6), 
'first_consume_money': 34, 
'first_consume_location': '后勤集团超市文具店', 
'most_consume_meal': '毓秀餐厅二层(原学二食堂)基本伙', 
'eat_consume': 7078.900000000001, 
'eletric_consume': 245.48, 
'shower_consume': 170, 
'most_consume_hour': '07', 
'most_consume_hour_2': '07', 
'most_consume_hour_3': '12'}
"""


class SL2020_DB():
    data = {}

    def __init__(self , userid):
        self.userid = userid
        self.c11 = cx_Oracle.connect("MYNUCT" , "AQU1m0Lhp8" ,
                                     "10.100.0.1/orcl").cursor()
        self.c12 = cx_Oracle.connect("C##MYNUCT" , "c8SYjM05x7U" ,
                                     "10.100.1.248/orcl").cursor()

    def getBasicData(self):

        sql = "select XH,XM,XB,BYNF,RXSJ,SYD,XY,ZY,BJ,ZGFKC,ZGF,ZDFKC,ZDF from C##NCUTDATA.DDXY_STU_COURSE where XH={}".format(
            self.userid)
        res = self.c12.execute(sql).fetchone()

        self.data["stu_id"] = res[0]
        self.data["name"] = res[1]
        self.data["sex"] = res[2]
        self.data["graduate_time"] = res[3]
        self.data["entrance_time"] = res[4]
        self.data["province"] = res[5]
        self.data["institude"] = res[6]
        self.data["mayjor"] = res[7]
        self.data["clazz"] = res[8]
        self.data["highest_lesson_name"] = res[9]
        self.data["highest_lesson_score"] = res[10]
        self.data["lowest_lesson_name"] = res[11]
        self.data["lowest_lesson_score"] = res[12]

    def getSameBirthdayNum(self):
        sql = "SELECT * from C##NCUTDATA.DDXY_STU_BASICINFO where XH={}".format(
            self.userid)
        res = self.c12.execute(sql).fetchone()
        self.data["same_name_num"] = int(res[1]) - 1
        self.data["same_birthday_num"] = int(res[4]) - 1

    def getFirstLesson(self):
        sql = "select KCMC,SKDD from C##NCUTDATA.DDXY_STU_FIRSTCOURSE where XH={}".format(
            self.userid)
        res = self.c12.execute(sql).fetchone()
        self.data["first_lesson_name"] = res[0]
        self.data["first_lesson_loaction"] = res[1]

    def getConsumingData(self):
        sql = """select count(*) as totaltimes,sum(x.SMT_TRANSMONEY) as totalmoney 
                from DBM.QYWX_YKTYHK y join DBM.QYWX_YKTJYXX x 
                on x.SMT_CARDID=y.SMT_CARDID
                where y.SMT_SALARYNO='{}'
                """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["total_consume_times"] = res[0]
        self.data["total_consume_money"] = res[1]

        sql = """
        select SMT_DEALDATETIME,SMT_TRANSMONEY,s.NAME from DBM.QYWX_YKTYHK Y
        join DBM.QYWX_YKTJYXX x on x.SMT_CARDID=y.SMT_CARDID
        join DBM.QYWX_YKTSH s on s.CODE=substr(x.SMT_ORG_ID,0,10)
        where y.SMT_SALARYNO='{}' and SMT_DEALDATETIME=(select MIN(SMT_DEALDATETIME) from DBM.QYWX_YKTYHK y1
        join DBM.QYWX_YKTJYXX x1 on x1.SMT_CARDID=y1.SMT_CARDID
        where y1.SMT_SALARYNO='{}')
        """.format(self.userid , self.userid)

        res = self.c11.execute(sql).fetchone()
        self.data["first_consume_times"] = res[0].strftime('%Y-%m-%d')
        self.data["first_consume_money"] = res[1]
        self.data["first_consume_location"] = res[2]

        sql = """
            select s.name,
               count(*)              as totaltimes,
               sum(x.SMT_TRANSMONEY) as totalmoney
            from DBM.QYWX_YKTYHK Y
                 join DBM.QYWX_YKTJYXX x on x.SMT_CARDID = y.SMT_CARDID
                 join DBM.QYWX_YKTSH s on s.CODE = x.SMT_ORG_ID
            where y.SMT_SALARYNO = '{}'
            and s.code > 10000000000
            group by x.SMT_ORG_ID, s.NAME
            ORDER BY sum(x.SMT_TRANSMONEY) desc
        """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["most_consume_meal"] = res[0]

        sql = """
        select s.name,
       count(*)              as totaltimes,
       sum(x.SMT_TRANSMONEY) as totalmoney
        from DBM.QYWX_YKTYHK Y
                 join DBM.QYWX_YKTJYXX x on x.SMT_CARDID = y.SMT_CARDID
                 join DBM.QYWX_YKTSH s on s.CODE = x.SMT_ORG_ID
        where y.SMT_SALARYNO = '{}'

        group by x.SMT_ORG_ID, s.name
            """.format(self.userid)

        res = self.c11.execute(sql).fetchall()
        el_sum = 0
        eat_sum = 0
        shower_sum = 0

        for i in res:
            if "餐" in str(i[0]) or "食" in str(i[0]):
                eat_sum += i[2]
            elif "浴" in str(i[0]):
                shower_sum += i[2]
            elif "电" in str(i[0]):
                el_sum += i[2]

        self.data["eat_consume"] = eat_sum
        self.data["eletric_consume"] = el_sum
        self.data["shower_consume"] = shower_sum

        sql = """
                select hour, count(*) as times
                from (select smt_name, to_char(smt_dealdatetime, 'HH24') as hour
                      from DBM.QYWX_YKTYHK Y
                               join DBM.QYWX_YKTJYXX x on x.SMT_CARDID = y.SMT_CARDID
                      where y.SMT_SALARYNO = '{}')
                group by hour
                order by times desc 
                """.format(self.userid)

        res = self.c11.execute(sql).fetchone()
        self.data["most_consume_hour"] = res[0]

        sql = """
        select hour, count(*) as times
        from (
         select to_char(smt_dealdatetime, 'HH24') as hour
         from DBM.QYWX_YKTYHK Y
                  join DBM.QYWX_YKTJYXX x on x.SMT_CARDID = y.SMT_CARDID
         where y.SMT_SALARYNO = '{}'
           and to_char(smt_dealdatetime, 'yyyy-mm-dd') between '2017-09-01' and '2018-07-15'
        )
        group by hour
        order by times desc
        """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["most_consume_hour_2"] = res[0]

        sql = """
        select hour, count(*) as times
        from (
                 select to_char(smt_dealdatetime, 'HH24') as hour
                 from DBM.QYWX_YKTYHK Y
                          join DBM.QYWX_YKTJYXX x on x.SMT_CARDID = y.SMT_CARDID
                 where y.SMT_SALARYNO = '{}'
                   and to_char(smt_dealdatetime, 'yyyy-mm-dd') between '2018-09-01' and '2019-07-15'
             )
        group by hour
        order by times desc
        """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["most_consume_hour_3"] = res[0]

    def getNetworkData(self):
        sql = "select round(SUM(C.LL)/1024) as TotalGib from DBM.NCUT_CSRDLLSJ  C where  C.YHM = '{}'".format(
            self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["total_network"] = res[0]

        sql = """
        select to_char(ZXSJ,'HH24') as HOUR,ROUND(SUM(C.LL)/1024) as G from DBM.NCUT_CSRDLLSJ C where  C.YHM='{}'  GROUP BY to_char(ZXSJ,'HH24')
        ORDER BY  G DESC 
        """.format(self.userid)

        res = self.c11.execute(sql).fetchone()

        self.data["most_use_network_time"] = res[0]

        sql = """
        select substr(to_char(DLSJ,'YYYYMM') ,5,6) as MONTH,ROUND(SUM(C.LL)/1024) as MONTHGIB from DBM.NCUT_CSRDLLSJ C where  C.YHM='17159010325' GROUP BY substr(to_char(DLSJ,'YYYYMM') ,5,6)
        ORDER BY MONTHGIB DESC
        """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["most_use_network_month"] = res[0]


if __name__ == "__main__":
    t = SL2020_DB("17159010325")
    t.getBasicData()
    t.getFirstLesson()
    t.getSameBirthdayNum()
    t.getNetworkData()
    t.getConsumingData()
    print(t.data)
