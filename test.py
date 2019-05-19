import cx_Oracle
dsn=cx_Oracle.makedsn("10.100.1.248",1521,"epps")
connect=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U",dsn)
c=connect.cursor()
sql='''
select XH,XM,XB,SYD,CC,XY,ZY,BJ from DDXY_STU_COURSE
'''
res=c.execute(sql)
print (res.fetchone())
c.close()
connect.close()