import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Yug@23042000",
    database="inventory"
)

# creating db cursor
cursor = db.cursor()

root = None

def set_root(top):
    global root
    root = top
    print(root)

def get_customer():
    cursor.execute("select * from customers;")
    customer = cursor.fetchall()
    return customer, cursor.description

def get_cashier():
    cursor.execute("select * from cashier;")
    cashier = cursor.fetchall()
    return cashier, cursor.description

def add_cashier_window():
    add_window = Tk()
    add_window.title("Add cashier details")
    cname_label = Label(add_window, text="Name of cashier")
    cname_label.grid(row=0, column=0, padx=10, pady=10)
    cname_entry = Entry(add_window)
    cname_entry.grid(row=0, column=1, padx=10, pady=10)

    address_label = Label(add_window, text="Address")
    address_label.grid(row=1, column=0, padx=10, pady=10)
    address_entry = Entry(add_window)
    address_entry.grid(row=1, column=1, padx=10, pady=10)

    phone_label = Label(add_window, text="Phone number")
    phone_label.grid(row=2, column=0, padx=10, pady=10)
    phone_entry = Entry(add_window)
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    salary_label = Label(add_window, text="Salary")
    salary_label.grid(row=3, column=0, padx=10, pady=10)
    salary_entry = Entry(add_window)
    salary_entry.grid(row=3, column=1, padx=10, pady=10)

    tip_label = Label(add_window, text="Tip")
    tip_label.grid(row=4, column=0, padx=10, pady=10)
    tip_entry = Entry(add_window)
    tip_entry.grid(row=4, column=1, padx=10, pady=10)
    
    add_button = Button(add_window, text="Add",
                        command=lambda: add_cashier_query(cname_entry.get(),  phone_entry.get(),address_entry.get(),
                                                          salary_entry.get(), tip_entry.get(), add_window))
    add_button.grid(row=5, columnspan=2, sticky='nsew')

def add_cashier_query(cname,phone,address,salary,tip, curr_window):
    curr_window.attributes("-topmost", True)
    try:
        salary = float(salary)
    except:
        messagebox.showerror("Error!", "Enter a number for salary please")
        print(cname,phone,address,salary,tip)
        return

    cursor.execute("select employee_id from cashier;")
    employee_id = cursor.fetchall()
    e_id = generate_id(employee_id)
    try:
        query = "INSERT INTO cashier VALUES('{}','{}',{},'{}',{},{});".format(e_id, cname, phone, address, salary, tip)
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "New cashier inserted!")
        global root
        # root.nametowidget("tree_table").destroy()
        print_result(get_cashier(), root.nametowidget("table_frame"))
        curr_window.destroy()
    except:
        messagebox.showerror("Error!", "Failed to insert record")

def generate_id(id_list):
    id_list = [x[0] for x in id_list]
    max_id = 0
    for x in id_list:
        x = list(x)
        for i in range(1, len(x)):
            if x[i] != '0':
                x = x[i:]
                break
        # print(str(x))
        if max_id < int(''.join(x)):
            max_id = int(''.join(x))
    new_id = id_list[0][0]
    print(new_id)
    new_id = new_id + '0' * (len(id_list[0]) - 1 - len(str(max_id)))
    print(new_id)
    new_id = new_id + str(max_id + 1)
    print(new_id)
    return new_id

def update_cashier_window():
    update_window = Tk()
    update_window.title("Update cashier details")
   
    cname_label = Label(update_window, text="Select name of cashier")
    cname_label.grid(row=0, column=0, padx=10, pady=10)

    cursor.execute("SELECT cashier_name from cashier;")
    c_names = cursor.fetchall()
    c_names = [x[0] for x in c_names]
    default_cashier = StringVar(update_window, name='selected')
    default_cashier.set(c_names[0])

    address_label = Label(update_window, text="Address")
    address_label.grid(row=1, column=0, padx=10, pady=10)
    address_entry = Entry(update_window, name='address_entry')
    address_entry.grid(row=1, column=1, padx=10, pady=10)

    phone_label = Label(update_window, text="Phone Number")
    phone_label.grid(row=2, column=0, padx=10, pady=10)
    phone_entry = Entry(update_window, name='phone_entry')
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    salary_label = Label(update_window, text="Salary")
    salary_label.grid(row=3, column=0, padx=10, pady=10)
    salary_entry = Entry(update_window, name='salary_entry')
    salary_entry.grid(row=3, column=1, padx=10, pady=10)

    tip_label = Label(update_window, text="Tip")
    tip_label.grid(row=4, column=0, padx=10, pady=10)
    tip_entry = Entry(update_window, name='tip_entry')
    tip_entry.grid(row=4, column=1, padx=10, pady=10)

    dropdown = OptionMenu(update_window, default_cashier, *c_names)
    dropdown.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    default_cashier.trace('w', lambda *args, b=phone_entry, c=address_entry, d=salary_entry,
                                      e=tip_entry: set_values_cashier(default_cashier, b, c, d, e, *args))

    update_button = Button(update_window, text="Update",
                           command=lambda: update_cashier_query(default_cashier.get(),phone_entry.get(),address_entry.get(), 
                                                                salary_entry.get(), tip_entry.get(), update_window))
    update_button.grid(row=5, columnspan=2, sticky='nsew')

def set_values_cashier(selected, phone_entry, address_entry, salary_entry, tip_entry, *args):
    print("SELECT * FROM cashier where cashier_name = '{}'".format(selected.get()))
    cursor.execute("SELECT * FROM cashier where cashier_name = '{}'".format(selected.get()))
    record=cursor.fetchall()
    record = record[0]
    print(record)
    print(record[2])
    print(record[3])
    print(record[4])
    print(record[5])
    print(phone_entry, address_entry, salary_entry, tip_entry)

    phone_entry.delete(0, 'end')
    phone_entry.insert(0, record[2])
    address_entry.delete(0, 'end')
    address_entry.insert(0, record[3])
    salary_entry.delete(0, 'end')
    salary_entry.insert(0, record[4])
    tip_entry.delete(0, 'end')
    tip_entry.insert(0, record[5])

def update_cashier_query(cname,  phone,address, salary, tip, curr_window):
    print(cname,  phone,address, salary, tip, curr_window)
    curr_window.attributes("-topmost", True)
    try:
        salary = float(salary)
    except:
        messagebox.showerror("Error!", "Enter a number for salary please")
        print(cname,  phone,address, salary, tip)
        return

    # try:
    #     number = float(number)
    # except:
    #     messagebox.showwarning("Error!", "Enter a number please")
    #     print(cname, phone,address, salary, tip)
    #     return

    # try:
    #     tip = float(tip)
    # except:
    #     messagebox.showwarning("Error!", "Enter a number for tip please")
    #     print(cname, phone,address, salary, tip)
    #     return

    try:
        query = "UPDATE cashier SET cashier_phone={}, cashier_address='{}', salary={}, tip={} Where " \
                "cashier_name='{}';".format(phone, address, salary, tip, cname)
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "Details updated!")
        print_result(get_cashier(), root.nametowidget("table_frame"))
        curr_window.destroy()
    except Exception as e:
        messagebox.showerror("Error!", "Failed to update record")
        print(e)

def delete_cashier_window():
    deletecashier_window = Tk()

    cursor.execute("SELECT * from cashier;")
    cashier = cursor.fetchall()
    cashier = [x[0] for x in cashier]

    selected_cashier = StringVar(deletecashier_window)
    selected_cashier.set(cashier[0])

    select_cashier_label = Label(deletecashier_window, text="Select Cashier ID")
    select_cashier_label.grid(row=1, column=0)
    cashier_menu = OptionMenu(deletecashier_window, selected_cashier, *cashier)
    cashier_menu.grid(row=1, column=1, sticky='ew')

    delete_button = Button(deletecashier_window, text='Delete',
                           command=lambda: delete_cashier_query(selected_cashier, deletecashier_window))
    delete_button.grid(row=2, column=0, columnspan=2, sticky='ew')

    cashier_table = get_cashier()
    print(cashier_table)
    print_result(cashier_table, deletecashier_window)


def delete_cashier_query(selected_cashier, curr_window=None):
    try:
        query = "DELETE from cashier where employee_id= '{}'".format(selected_cashier.get())
        print(query)
        cursor.execute(query)
        db.commit()
        if curr_window:
            messagebox.showinfo("Success", "Success!")
            print_result(get_cashier(), root.nametowidget("table_frame"))
            curr_window.destroy()
            delete_cashier_window()
    except:
        messagebox.showerror("Error!", "Failed to delete cashier")

def add_customer_window():
    add_window = Tk()
    add_window.title("Add customer details")
    name_label = Label(add_window, text="Name of customer")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = Entry(add_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    address_label = Label(add_window, text="Address")
    address_label.grid(row=1, column=0, padx=10, pady=10)
    address_entry = Entry(add_window)
    address_entry.grid(row=1, column=1, padx=10, pady=10)

    phone_label = Label(add_window, text="Phone number")
    phone_label.grid(row=2, column=0, padx=10, pady=10)
    phone_entry = Entry(add_window)
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    points_label = Label(add_window, text="Points")
    points_label.grid(row=4, column=0, padx=10, pady=10)
    points_entry = Entry(add_window)
    points_entry.grid(row=4, column=1, padx=10, pady=10)
    
    add_button = Button(add_window, text="Add",
                        command=lambda: add_customer_query(name_entry.get(),  phone_entry.get(),address_entry.get(),
                                                          points_entry.get(), add_window))
    add_button.grid(row=5, columnspan=2, sticky='nsew')

def add_customer_query(name,phone,address,points, curr_window):
    curr_window.attributes("-topmost", True)
    try:
        points = int(points)
    except:
        messagebox.showerror("Error!", "Enter a number for points please")
        print(cname,phone,address,points)
        return

    cursor.execute("select customer_id from customers;")
    customer_id = cursor.fetchall()
    c_id = generate_id(customer_id)
    try:
        query = "INSERT INTO customers VALUES('{}','{}',{},'{}',{});".format(c_id, name, phone, address, points)
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "New customer inserted!")
        global root
        # root.nametowidget("tree_table").destroy()
        print_result(get_customer(), root.nametowidget("table_frame"))
        curr_window.destroy()
    except:
        messagebox.showerror("Error!", "Failed to insert record")

def update_customer_window():
    update_window = Tk()
    update_window.title("Update customer details")
   
    name_label = Label(update_window, text="Select name of customer")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    cursor.execute("SELECT customer_name from customers;")
    cus_names = cursor.fetchall()
    cus_names = [x[0] for x in cus_names]
    default_customer = StringVar(update_window, name='selected')
    default_customer.set(cus_names[0])

    address_label = Label(update_window, text="Address")
    address_label.grid(row=1, column=0, padx=10, pady=10)
    address_entry = Entry(update_window, name='address_entry')
    address_entry.grid(row=1, column=1, padx=10, pady=10)

    phone_label = Label(update_window, text="Phone Number")
    phone_label.grid(row=2, column=0, padx=10, pady=10)
    phone_entry = Entry(update_window, name='phone_entry')
    phone_entry.grid(row=2, column=1, padx=10, pady=10)

    points_label = Label(update_window, text="Points")
    points_label.grid(row=4, column=0, padx=10, pady=10)
    points_entry = Entry(update_window, name='tip_entry')
    points_entry.grid(row=4, column=1, padx=10, pady=10)

    dropdown = OptionMenu(update_window, default_customer, *cus_names)
    dropdown.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    default_customer.trace('w', lambda *args, b=phone_entry, c=address_entry, 
    						d=points_entry: set_values_customer(default_customer, b, c, d, *args))

    update_button = Button(update_window, text="Update",
                           command=lambda: update_cashier_query(default_customer.get(),phone_entry.get(),address_entry.get(), 
                                                                points_entry.get(), update_window))
    update_button.grid(row=5, columnspan=2, sticky='nsew')

def set_values_customer(selected, phone_entry, address_entry, points_entry, *args):
    print("SELECT * FROM customers where customer_name = '{}'".format(selected.get()))
    cursor.execute("SELECT * FROM customers where customer_name = '{}'".format(selected.get()))
    record=cursor.fetchall()
    record = record[0]
    print(record)
    print(record[2])
    print(record[3])
    print(record[4])
    print(phone_entry, address_entry, points_entry)

    phone_entry.delete(0, 'end')
    phone_entry.insert(0, record[2])
    address_entry.delete(0, 'end')
    address_entry.insert(0, record[3])
    points_entry.delete(0, 'end')
    points_entry.insert(0, record[4])
  
def update_customer_query(name,  phone,address, points, curr_window):
    print(name,  phone,address, points, curr_window)
    curr_window.attributes("-topmost", True)
    try:
        points = int(points)
    except:
        messagebox.showerror("Error!", "Enter a number for points please")
        print(name,  phone,address, points)
        return

    # try:
    #     number = float(number)
    # except:
    #     messagebox.showwarning("Error!", "Enter a number please")
    #     print(cname, phone,address, salary, tip)
    #     return

    # try:
    #     tip = float(tip)
    # except:
    #     messagebox.showwarning("Error!", "Enter a number for tip please")
    #     print(cname, phone,address, salary, tip)
    #     return

    try:
        query = "UPDATE customers SET customer_phone={}, customer_address='{}', points={} Where " \
                "customer_name='{}';".format(phone, address, points, name)
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "Details updated!")
        print_result(get_customer(), root.nametowidget("table_frame"))
        curr_window.destroy()
    except Exception as e:
        messagebox.showerror("Error!", "Failed to update record")
        print(e)

def delete_customer_window():
    deletecustomer_window = Tk()

    cursor.execute("SELECT * from customers;")
    customer = cursor.fetchall()
    customer = [x[0] for x in customer]

    selected_customer = StringVar(deletecustomer_window)
    selected_customer.set(customer[0])

    select_customer_label = Label(deletecustomer_window, text="Select customer ID")
    select_customer_label.grid(row=1, column=0)
    customer_menu = OptionMenu(deletecustomer_window, selected_customer, *customer)
    customer_menu.grid(row=1, column=1, sticky='ew')

    delete_button = Button(deletecustomer_window, text='Delete',
                           command=lambda: delete_customer_query(selected_customer, deletecustomer_window))
    delete_button.grid(row=2, column=0, columnspan=2, sticky='ew')

    customer_table = get_customer()
    print(customer_table)
    print_result(customer_table, deletecustomer_window)


def delete_customer_query(selected_customer, curr_window=None):
    try:
        query = "DELETE from customers where customer_id= '{}'".format(selected_customer.get())
        print(query)
        cursor.execute(query)
        db.commit()
        if curr_window:
            messagebox.showinfo("Success", "Success!")
            print_result(get_customer(), root.nametowidget("table_frame"))
            curr_window.destroy()
            delete_customer_window()
    except:
        messagebox.showerror("Error!", "Failed to delete cashier")



# creating tree view to display query results as a table
def print_result(result, top):
    rows = result[0]
    cols = [x[0] for x in result[1]]
    tree = ttk.Treeview(top, columns=cols, show='headings', name='tree_table')

    for x in cols:
        tree.heading(x, text=x)
    tree.grid(row=0, column=0, columnspan=len(cols))
    # tree.pack(side=LEFT, padx=5, pady=5)
    # top.grid_columnconfigure(0, weight=1)

    # for i in range(len(cols)):
    #     top.grid_columnconfigure(i, weight=1, uniform='column')

    vsb = ttk.Scrollbar(top, orient="vertical", command=tree.yview, name='scroll')
    vsb.grid(row=0, column=len(cols) + 1, rowspan=len(rows), sticky='NS')
    # vsb.pack(side=RIGHT, fill= Y)
    tree.configure(yscrollcommand=vsb.set)
    for x in rows:
        tree.insert("", "end", values=x)
        # print(x)
