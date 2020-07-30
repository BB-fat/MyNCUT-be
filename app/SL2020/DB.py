import cx_Oracle
import os
import json
import time
import hashlib
import requests
from lxml import etree

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class SL2020_DB():
    data = {}

    def __init__(self , userid):
        self.userid = userid
        self.c11 = cx_Oracle.connect("MYNUCT" , "AQU1m0Lhp8" ,
                                     "10.100.0.1/orcl").cursor()
        self.c12 = cx_Oracle.connect("C##MYNUCT" , "c8SYjM05x7U" ,
                                     "10.100.1.248/orcl").cursor()

    def getBasicData(self):
        """
        课程是列表
        :return:
        """

        sql = "select XH,XM,XB,BYNF,RXSJ,SYD,XY,ZY,BJ,ZGFKC,ZGF,ZDFKC,ZDF from DDXY_STU_COURSE where XH={}".format(
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
        self.data["lowest_lesson_name"] = res[9]
        self.data["lowest_lesson_score"] = res[10]

    def getSameBirthdayNum(self):
        sql = "SELECT * from DDXY_STU_BASICINFO where XH={}".format(self.userid)
        res = self.c12.execute(sql).fetchone()
        self.data["same_name_num"] = res[1] - 1
        # self.data["name"] = res[1]
        # self.data["sex"] = res[2]
        # self.data["graduate_time"] = res[3]
        # self.data["entrance_time"] = res[4]

    def getFirstLesson(self):
        sql = "select KCMC,SKDD from C##NCUTDATA.DDXY_STU_FIRSTCOURSE where XH={}".format(self.userid)
        res = self.c12.execute(sql).fetchone()
        self.data["first_lesson_name"] = res[0]
        self.data["first_lesson_loaction"] = res[1]

    def getConsumingData(self):
        sql = """select count(*) as totaltimes,sum(x.SMT_TRANSMONEY) as totalmoney 
                from DBM.QYWX_YKTYHK y join DBM.QYWX_YKTJYXX x 
                on x.SMT_CARDID=y.SMT_CARDID
                where y.SMT_SALARYNO={}
                """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["total_consume_times"] = res[0]
        self.data["total_consume_money"] = res[1]

        sql = """
        select SMT_DEALDATETIME,SMT_TRANSMONEY,s.NAME from DBM.QYWX_YKTYHK Y
        join DBM.QYWX_YKTJYXX x on x.SMT_CARDID=y.SMT_CARDID
        join DBM.QYWX_YKTSH s on s.CODE=substr(x.SMT_ORG_ID,0,10)
        where y.SMT_SALARYNO={} and SMT_DEALDATETIME=(select MIN(SMT_DEALDATETIME) from DBM.QYWX_YKTYHK y1
        join DBM.QYWX_YKTJYXX x1 on x1.SMT_CARDID=y1.SMT_CARDID
        where y1.SMT_SALARYNO={})
        """.format(self.userid)

        res = self.c11.execute(sql).fetchone()
        self.data["first_meal_times"] = res[0]
        self.data["first_meal_money"] = res[1]
        self.data["first_meal_location"] = res[2]

        sql = """
            select s.name,
               count(*)              as totaltimes,
               sum(x.SMT_TRANSMONEY) as totalmoney
            from DBM.QYWX_YKTYHK Y
                 join DBM.QYWX_YKTJYXX x on x.SMT_CARDID = y.SMT_CARDID
                 join DBM.QYWX_YKTSH s on s.CODE = x.SMT_ORG_ID
            where y.SMT_SALARYNO = {}
            and s.code > 10000000000
            group by x.SMT_ORG_ID, s.NAME
            ORDER BY sum(x.SMT_TRANSMONEY) desc)
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
        where y.SMT_SALARYNO = {}
        
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
                      where y.SMT_SALARYNO = {})
                group by hour
                order by times desc 
                """.format(self.userid)

        res = self.c11.execute(sql).fetchone()
        self.data["most_consume_hour"] = res[0]

    def getNetworkData(self):
        sql = "select round(SUM(C.LL)/1024) as TotalGib from NCUT_CSRDLLSJ  C where  C.YHM = {}".format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["total_network"] = res[0]

        sql = """
        select to_char(ZXSJ,'HH24') as HOUR,MAX(ROUND(SUM(C.LL)/1024)) as G from NCUT_CSRDLLSJ C where  C.YHM={}  GROUP BY to_char(ZXSJ,'HH24')
        ORDER BY G DESC
        """.format(self.userid)

        res = self.c11.execute(sql).fetchone()
        self.data["most_use_network_time"] = res[0]

        sql = """
        select to_char(DLSJ,'YYYYMM') as MONTH,ROUND(SUM(C.LL)/1024) as MONTHGIB from NCUT_CSRDLLSJ C where  C.YHM={} GROUP BY to_char(DLSJ,'YYYYMM')
        ORDER BY MONTHGIB DESC
        """.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        self.data["most_use_network_month"] = res[1]
