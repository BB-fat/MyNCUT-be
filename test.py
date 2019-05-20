# -*- coding: utf-8 -*-
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

print (cx_Oracle.clientversion())
conn = cx_Oracle.connect("C##MYNUCT", "c8SYjM05x7U", "10.100.1.248/orcl")
print (conn.version)

sql = """
select XH,KCS,ZXF,ZGFKC,ZGF,ZDFKC,ZDF from DDXY_STU_COURSE  where XH='17152010921'
"""

#sql = "select * from C##NCUTDATA.DDXY_STU_FIRSTCOURSE where rownum <=5"

cursor = conn.cursor()

for each in cursor.execute(sql):
  print(each[0])
  print(each[1])