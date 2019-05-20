import cx_Oracle
import os
import json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def takeIndex(items,index):
    return list(items)[index]
class SchoolLife():
    def __init__(self, userid):
        self.userid = userid
        self.c11 = cx_Oracle.connect("MYNUCT", "AQU1m0Lhp8",
                                     "10.100.0.1/orcl").cursor()
        self.c12 = cx_Oracle.connect(
            "C##MYNUCT", "c8SYjM05x7U", "10.100.1.248/orcl").cursor()

    def getData(self):
        '''
        获得数据
        '''
        return {
            **self.__consum(),
            **self.__dining_hall(),
            **self.__school_net_sum(),
            **self.__school_net_day(),
            **self.__birthday(),
        }

    def __consum(self):
        '''
        消费总次数、金额
        '''
        sql = '''
        select count(*) as totaltimes,sum(x.SMT_TRANSMONEY) as totalmoney from DBM.QYWX_YKTYHK Y
        join DBM.QYWX_YKTJYXX x on x.SMT_CARDID=y.SMT_CARDID
        where y.SMT_SALARYNO='{}'
        '''.format(self.userid)
        res = self.c11.execute(sql).fetchone()
        return {
            'sum_consum_times': res[0],
            'sum_consum_money': res[1]
        }

    def __dining_hall(self):
        '''
        食堂消费相关
        '''
        sql = '''
        select case 
        when s.NAME='学一食堂' then '毓秀餐厅一层(原学一食堂)' 
        when s.NAME='学二食堂' then '毓秀餐厅二层(原学二食堂)' 
        when s.NAME='学三食堂' then '尚德餐厅(原学三食堂)' 
        when s.NAME='学四风味食堂' then '聚贤阁(原学四食堂)' 
        when s.NAME='学五风味食堂' then '乐膳轩(原学五食堂)' 
        when s.NAME='学生餐厅' then '欣荣居(原学生餐厅)' 
        else s.NAME 
        end as NAME,
        count(*) as totaltimes,sum(x.SMT_TRANSMONEY) as totalmoney from DBM.QYWX_YKTYHK Y
        join DBM.QYWX_YKTJYXX x on x.SMT_CARDID=y.SMT_CARDID
        join DBM.QYWX_YKTSH s on s.CODE=substr(x.SMT_ORG_ID,0,10)
        where y.SMT_SALARYNO='{}'
        group by substr(x.SMT_ORG_ID,0,10),s.NAME
        ORDER BY sum(x.SMT_TRANSMONEY) desc
        '''.format(self.userid)
        res = self.c11.execute(sql).fetchall()
        res.sort(key=takeIndex(res,2))
        return {
            'dining_hall':res[:5]
        }

    def __school_net_sum(self):
        '''
        校园网使用总量
        '''
        sql='''
        select round(SUM(C.LL)/1024) as TotalGib from DBM.NCUT_CSRDLLSJ  C where  C.YHM = '{}'
        '''.format(self.userid)
        res=self.c11.execute(sql).fetchone()
        return {
            'school_net_sum':res[0]
        }

    def __school_net_day(self):
        '''
        校园网分小时使用情况
        '''
        sql='''
        select to_char(ZXSJ,'HH24') as HOUR,ROUND(SUM(C.LL)/1024) as G from DBM.NCUT_CSRDLLSJ C where  C.YHM='{}'  GROUP BY to_char(ZXSJ,'HH24')
        ORDER BY to_char(ZXSJ,'HH24') ASC
        '''.format(self.userid)
        res=self.c11.execute(sql).fetchall()
        return {
            'school_net_day':res
        }

    def __birthday(self):
        '''
        生日
        '''
        sql='''
        SELECT * from C##NCUTDATA.DDXY_STU_BASICINFO where XH='{}'
        '''.format(self.userid)
        res=self.c12.execute(sql).fetchone()
        return {
            "same_name":int(res[1])-1,
            "same_day_school":res[2]-1,
            "same_day_and_year":res[3]-1,
            "same_day_xueyuan":res[4]-1
        }


if __name__=="__main__":
    A=SchoolLife("17152010921")
    print(json.dumps(A.getData()))