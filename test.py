import cx_Oracle
dsn=cx_Oracle.makedsn("10.100.0.1",1521,"ORCL")
connect=cx_Oracle.connect("MYNUCT","AQU1m0Lhp8",dsn)
c=connect.cursor()
sql="select round(SUM(C.LL)/1024) as TotalGib from NCUT_CSRDLLSJ  C where  C.YHM = '17152010921'"
res=c.execute(sql)
print (res.fetchone())
c.close()
connect.close()