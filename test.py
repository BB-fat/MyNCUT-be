import cx_Oracle
dsn=cx_Oracle.makedsn("10.100.1.248",1521,"epps")
connect=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U",dsn)
c=connect.cursor()
sql='''
select case 
	when s.NAME='学一食堂' then '毓秀餐厅一层(原学一食堂)' 
	when s.NAME='学二食堂' then '毓秀餐厅二层(原学二食堂)' 
	when s.NAME='学三食堂' then '尚德餐厅(原学三食堂)' 
	when s.NAME='学四风味食堂' then '聚贤阁(原学四食堂)' 
	when s.NAME='学五风味食堂' then '乐膳轩(原学五食堂)' 
	when s.NAME='学生餐厅' then '欣荣居(原学生餐厅)' 
	else s.NAME 
end as NAME,
count(*) as totaltimes,sum(x.SMT_TRANSMONEY) as totalmoney from DBM.QYWX_YKTYHK Y
join DBM.QYWX_YKTJYXX x on x.SMT_CARDID=y.SMT_CARDID
join DBM.QYWX_YKTSH s on s.CODE=substr(x.SMT_ORG_ID,0,10)
where y.SMT_SALARYNO='17152010921'
group by substr(x.SMT_ORG_ID,0,10),s.NAME
ORDER BY sum(x.SMT_TRANSMONEY) desc
'''
res=c.execute(sql)
print (res.fetchone())
c.close()
conn.close()  