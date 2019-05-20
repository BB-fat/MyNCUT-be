# -*- coding: utf-8 -*-
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

conn = cx_Oracle.connect("MYNUCT", "AQU1m0Lhp8", "10.100.0.1/orcl")

# conn = cx_Oracle.connect("C##MYNUCT", "c8SYjM05x7U", "10.100.1.248/orcl")

# sql = """
# SELECT * from C##NCUTDATA.DDXY_STU_BASICINFO where XH='17152010921'
# """
sql='''
select round(SUM(C.LL)/1024) as TotalGib from MYNCUTDATA.NCUT_CSRDLLSJ  C where  C.YHM = '000120'
'''

#sql = "select * from C##NCUTDATA.DDXY_STU_FIRSTCOURSE where rownum <=5"

cursor = conn.cursor()

# for each in cursor.execute(sql):
#   print(each[0])
#   print(each[1])
print(cursor.execute(sql).fetchall())