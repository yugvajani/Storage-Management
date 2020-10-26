import mysql.connector
con=mysql.connector.connect(host='localhost',database='mysql',user='root',password='Yug@23042000')
cur=con.cursor()
cur.execute('Create DATABASE INVENTORY')
# cur.execute("CREATE TABLE manager((employee_id varchar(10) check(substring(employee_id,1,1)== 'E')),manager_name varchar(100) not null,number int(10) not null,salary float() not null check(salary>0),address varchar(100) not null,bonus float() ,primary key(employee_id))")
print('Database created Successfully')