import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Yug@23042000",
    database = "inventory"
)

print(db)
cursor = db.cursor()


cursor.execute("DROP TABLE IF EXISTS product_shipment;")
cursor.execute("DROP TABLE IF EXISTS shipments;")
cursor.execute("DROP TABLE IF EXISTS products;")

cursor.execute("CREATE Table products ( product_id varchar(10) check(substring(product_id,1,1) = 'P'),"
               "product_name varchar(100) not null,quantity int not null default 0,product_type varchar(15) not null, "
               "sell_price float not null check(sell_price>0), cost_price float not null check(cost_price>0),"
               " primary key(product_id));")
cursor.execute("insert into products values ('P00001', 'OnePlus 7T', 200, 'Phone', 34999, 20000);")
cursor.execute("insert into products values ('P00002', 'Samsung Galaxy Note 10', 100, 'Phone',75999, 50000);")
cursor.execute("insert into products values ('P00003', 'IPhone 11', 160, 'Phone', 64900, 45000);")
cursor.execute("insert into products values ('P00004', 'Google Pixel 4XL', 50, 'Phone', 82990, 60000);")
cursor.execute("insert into products values ('P00005', 'Sony Xperia One', 1, 'Phone', 73990, 55000);")
cursor.execute("insert into products values ('P00006', 'Asus Vivobook', 100, 'Laptop', 74999, 60000);")
cursor.execute("insert into products values ('P00007', 'MacBook Pro', 75, 'Laptop', 119900 , 80000);")
cursor.execute("insert into products values ('P00008', 'Dell XPS13', 50, 'Laptop', 83990 , 61000);")
cursor.execute("insert into products values ('P00009', 'IPad Pro', 50, 'Tablet', 62900, 47000);")
cursor.execute("insert into products values ('P00010', 'Samsung Galaxy Tab A', 20, 'Tablet', 19999, 9000);")

cursor.execute("CREATE Table shipments(shipment_id varchar(10) "
               "check(substring(shipment_id,1,1) = 'S'), "
               "payment_type varchar(6) not null check( payment_type = 'cash' or payment_type = 'cheque'"
               " or payment_type = 'card'), order_date date not null, delivery_date date not null,"
               " total_cost float not null check(total_cost>0), primary key(shipment_id), "
               "check(order_date <= delivery_date));")
cursor.execute("insert into shipments values('S00001', 'Cheque', '2019-07-24' , '2019-08-01' , 5000000); ")
cursor.execute("insert into shipments values('S00002', 'Cash', '2019-09-07' , '2019-09-15', 3940000);")
cursor.execute("insert into shipments values('S00003', 'Card', '2019-10-29' , '2019-11-03', 3620000);")
cursor.execute("insert into shipments values('S00004', 'Card', '2019-11-23', '2019-11-30', 560000); ")
cursor.execute("insert into shipments values('S00005', 'Cheque','2019-02-12' ,'2019-12-11',5655000); ")
cursor.execute("insert into shipments values('S00006', 'Cash', '2019-12-15' , '2019-12-24', 2160000); ")
cursor.execute("insert into shipments values('S00007', 'Cheque', '2020-01-05' , '2020-01-15', 1600000);")
cursor.execute("insert into shipments values('S00008', 'Cheque', '2020-01-27', '2020-02-05', 6600000);")
cursor.execute("insert into shipments values('S00009', 'Cash', '2020-03-10', '2020-03-15', 5090000);")
cursor.execute("insert into shipments values('S00010', 'Card', '2020-04-01', '2020-04-19', 2610000);")

cursor.execute("CREATE Table product_shipment( shipment_id varchar(10), product_id varchar(10),"
               " cost_price float not null check(cost_price>0), quantity int not null check(quantity>0),"
               " foreign key (shipment_id) references shipments(shipment_id) on delete cascade on update cascade,"
               " foreign key (product_id) references products(product_id) on delete no action on update cascade);")
cursor.execute("insert into product_shipment values('S00001', 'P00001', 20000, 100);")
cursor.execute("insert into product_shipment values('S00001', 'P00006', 60000, 50);")
cursor.execute("insert into product_shipment values('S00002', 'P00006', 60000, 50);")
cursor.execute("insert into product_shipment values('S00002', 'P00009', 47000, 20);")
cursor.execute("insert into product_shipment values('S00003', 'P00007', 80000, 30);")
cursor.execute("insert into product_shipment values('S00003', 'P00008', 61000, 20);")
cursor.execute("insert into product_shipment values('S00004', 'P00009', 47000, 10);")
cursor.execute("insert into product_shipment values('S00004', 'P00010', 9000, 10);")
cursor.execute("insert into product_shipment values('S00005', 'P00001', 20000, 100);")
cursor.execute("insert into product_shipment values('S00005', 'P00005', 55000, 1);")
cursor.execute("insert into product_shipment values('S00005', 'P00003', 45000, 80);")
cursor.execute("insert into product_shipment values('S00006', 'P00009', 47000, 20);")
cursor.execute("insert into product_shipment values('S00006', 'P00008', 61000, 20);")
cursor.execute("insert into product_shipment values('S00007', 'P00007', 80000, 20);")
cursor.execute("insert into product_shipment values('S00008', 'P00003', 45000, 80);")
cursor.execute("insert into product_shipment values('S00008', 'P00004', 60000, 50);")
cursor.execute("insert into product_shipment values('S00009', 'P00002', 50000, 100);")
cursor.execute("insert into product_shipment values('S00009', 'P00010', 9000, 10);")
cursor.execute("insert into product_shipment values('S00010', 'P00007', 80000, 25);")
cursor.execute("insert into product_shipment values('S00010', 'P00008', 61000, 10);")

db.commit()

cursor.execute("select * from product_shipment;")

result = cursor.fetchall()

for x in result:
    print(x)