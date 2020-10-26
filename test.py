import mysql.connector
mydb=mysql.connector.connect(host='localhost',database='inventory',user='root',password='Yug@23042000')
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE manager(employee_id varchar(10) check(substring(employee_id,1,1) == 'E'),manager_name varchar(100) not null,number int(10) not null,salary float not null check(salary>0),address varchar(100) not null,bonus float() not null default 0,primary key(employee_id)")
	# CREATE TABLE cashier(
	# 	employee_id varchar(10) check(substring(employee_id,1,1)== 'E'),
	# 	cashier_name varchar(100) not null,
	# 	number int(10) not null,
	# 	salary float not null check(salary>0),s
	# 	address varchar(100) not null,
	# 	tip float() not null default 0,
	# 	primary key(employee_id)
	# )
