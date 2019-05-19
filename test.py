import cx_Oracle
dsn=cx_Oracle.makedsn("10.100.0.1",1521,"ORCL")
connect=cx_Oracle.connect("MYNUCT","AQU1m0Lhp8",dsn)
c=connect.cursor()
sql='''
select to_char(ZXSJ,'HH24') as HOUR,ROUND(SUM(C.LL)/1024) as G from NCUT_CSRDLLSJ C where  C.YHM='17152010921'  GROUP BY to_char(ZXSJ,'HH24')
ORDER BY to_char(ZXSJ,'HH24') ASC
'''
res=c.execute(sql)
print (res.fetchone())
c.close()
connect.close()