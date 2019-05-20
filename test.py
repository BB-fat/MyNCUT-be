# -*- coding: utf-8 -*-
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

# print (cx_Oracle.clientversion())
conn = cx_Oracle.connect("C##MYNUCT", "c8SYjM05x7U", "10.100.1.248/orcl")
# print (conn.version)

sql = """
select DISTINCT KCMC,JSMC from C##MYNUCT.DDXY_STU_FIRSTCOURSE   F1
where XH='15104050234' AND SKXQ=(select MIN(SKXQ) from DDXY_STU_FIRSTCOURSE where XH=F1.XH) 
AND SKDY=(select MIN(SKDY) from DDXY_STU_FIRSTCOURSE where XH=F1.XH and (SKXQ=(select MIN(SKXQ) from DDXY_STU_FIRSTCOURSE where XH=F1.XH) ))
"""

#sql = "select * from C##NCUTDATA.DDXY_STU_FIRSTCOURSE where rownum <=5"

cursor = conn.cursor()

for each in cursor.execute(sql):
  print(each[0])
  print(each[1])