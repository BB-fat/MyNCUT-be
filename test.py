import cx_Oracle
# dsn=cx_Oracle.makedsn("10.100.0.1",1521,"ORCL")
# connect=cx_Oracle.connect("MYNUCT","AQU1m0Lhp8",dsn)
dsn=cx_Oracle.makedsn("10.100.1.248",1521,"epps")
connect=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U",dsn)
c=connect.cursor()
sql='''
SELECT owner FROM all_tables WHERE table_name = 'DDXY_STU_BASICINFO';
'''
res=c.execute(sql)
print (res.fetchone())
c.close()
connect.close()