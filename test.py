import cx_Oracle
dsn=cx_Oracle.makedsn("10.100.1.248",1521,"epps")
connect=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U",dsn)
c=connect.cursor()
sql="select round(SUM(C.LL)/1024) as TotalGib from NCUT_CSRDLLSJ  C where  C.YHM = '17152010921'"
res=c.execute(sql)
print (res.fetchone())
c.close()
connect.close()