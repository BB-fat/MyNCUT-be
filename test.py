import cx_Oracle
# dsn=cx_Oracle.makedsn("10.100.0.1",1521,"ORCL")
# connect=cx_Oracle.connect("MYNUCT","AQU1m0Lhp8",dsn)
dsn=cx_Oracle.makedsn("10.100.1.248",1521,"epps")
connect=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U",dsn)
c=connect.cursor()
sql='''
select DISTINCT KCMC,JSMC from DDXY_STU_FIRSTCOURSE   F1
where XH='15104050234' AND SKXQ=(select MIN(SKXQ) from DDXY_STU_FIRSTCOURSE where XH=F1.XH) 
AND SKDY=(select MIN(SKDY) from DDXY_STU_FIRSTCOURSE where XH=F1.XH and (SKXQ=(select MIN(SKXQ) from DDXY_STU_FIRSTCOURSE where XH=F1.XH) ))
'''
res=c.execute(sql)
print (res.fetchall())
c.close()
connect.close()