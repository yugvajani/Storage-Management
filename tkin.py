from tkinter import *
import tkinter.messagebox as Messagebox
import mysql.connector as mysql
root=Tk()
root.geometry("600x300")
root.title("Add Customer")

def insert():
	cid=e_id.get();
	name=e_name.get();
	phone=e_phone.get();
	address=e_address.get(); 
	points=e_points.get();

	if(cid=="" or name=="" or phone=="" or address=="" or points==""):
		Messagebox.showinfo("All the fields must be Inserted")
	else:
		mydb=mysql.connect(host="localhost",user="root",password="Yug@23042000",database="inventory")
		mycursor=mydb.cursor()
		mycursor.execute("insert into customers values('"+ cid +"','"+ phone +"','"+ address +"','"+ name +"','"+ points +"')")
		mycursor.execute("commit");
		e_id.delete(0,'end')
		e_name.delete(0,'end')
		e_phone.delete(0,'end')
		e_address.delete(0,'end')
		e_points.delete(0,'end')
		Messagebox.showinfo("Inserted Successfully");
		mydb.close(); 

def delete():
	if(e_id.get()=="" and e_name.get()==""):
		Messagebox.showinfo("Id or Name is compulsory for delete")
	else:
		mydb=mysql.connect(host="localhost",user="root",password="Yug@23042000",database="inventory")
		mycursor=mydb.cursor()
		mycursor.execute("delete from customers where cid='"+e_id.get()+"' or name='"+e_name.get()+"'")
		mycursor.execute("commit");
		e_id.delete(0,'end')
		e_name.delete(0,'end')
		e_phone.delete(0,'end')
		e_address.delete(0,'end')
		e_points.delete(0,'end')
		Messagebox.showinfo("Deleted Successfully");
		mydb.close(); 

def update():
	cid=e_id.get();
	name=e_name.get();
	phone=e_phone.get();
	address=e_address.get(); 
	points=e_points.get();

	if(cid=="" or name=="" or phone=="" or address==""):
		Messagebox.showinfo("All the fields must be Inserted")
	else:
		mydb=mysql.connect(host="localhost",user="root",password="Yug@23042000",database="inventory")
		mycursor=mydb.cursor()
		mycursor.execute("update customers set cid='"+ cid +"',number='"+ phone +"',address='"+ address +"',name='"+ name +"',points='"+ points +"' where cid='"+cid+"'")
		mycursor.execute("commit");
		e_id.delete(0,'end')
		e_name.delete(0,'end')
		e_phone.delete(0,'end')
		e_address.delete(0,'end')
		e_points.delete(0,'end')
		Messagebox.showinfo("Updated Successfully");
		mydb.close();

def get():
	if(e_id.get()==""):
		Messagebox.showinfo("Id is compulsory for Get status")
	else:
		mydb=mysql.connect(host="localhost",user="root",password="Yug@23042000",database="inventory")
		mycursor=mydb.cursor()
		mycursor.execute("select * from customers where cid='"+e_id.get()+"'")
		rows=mycursor.fetchall()

		for row in rows:
			e_name.insert(0,row[3])
			e_phone.insert(0,row[1])
			e_address.insert(0,row[2])
			e_points.insert(0,row[4])

		mydb.close();

cid=Label(root,text='Enter Customer Id',font=('bold',10))
cid.place(x=20,y=30);
name=Label(root,text='Enter Customer Name',font=('bold',10))
name.place(x=20,y=60);
phone=Label(root,text='Enter Customer PhoneNo.',font=('bold',10))
phone.place(x=20,y=90);
address=Label(root,text='Enter Customer Address',font=('bold',10))
address.place(x=20,y=120);
points=Label(root,text='Enter Customer Points',font=('bold',10))
points.place(x=20,y=150);

e_id=Entry()
e_id.place(x=190,y=30)
e_name=Entry()
e_name.place(x=190,y=60)
e_phone=Entry()
e_phone.place(x=190,y=90)
e_address=Entry()
e_address.place(x=190,y=120)
e_points=Entry()
e_points.place(x=190,y=150)

insert=Button(root,text="Add Customer",font=("Italic",10),bg="white",command=insert)
insert.place(x=20,y=180)
delete=Button(root,text="Delete Customer",font=("Italic",10),bg="white",command=delete)
delete.place(x=130,y=180)
get=Button(root,text="Get Customer Details",font=("Italic",10),bg="white",command=get)
get.place(x=250,y=180)
update=Button(root,text="Update Customer",font=("Italic",10),bg="white",command=update)
update.place(x=420,y=180)
root.mainloop()
