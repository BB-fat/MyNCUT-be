import cx_Oracle
# dsn=cx_Oracle.makedsn("10.100.0.1",1521,"ORCL")
# connect=cx_Oracle.connect("MYNUCT","AQU1m0Lhp8",dsn)
dsn=cx_Oracle.makedsn("10.100.1.248",1521,"epps")
connect=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U",dsn)
c=connect.cursor()
sql='''
select XH,KCS,ZXF,ZGFKC,ZGF,ZDFKC,ZDF from DDXY_STU_COURSE  where XH='xuehao'
'''
res=c.execute(sql)
print (res.fetchall())
c.close()
connect.close()