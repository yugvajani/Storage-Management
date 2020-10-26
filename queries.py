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
#   print_result(get_products(), root)


def get_products():
    cursor.execute("select * from products;")
    products = cursor.fetchall()
    return products, cursor.description


def get_shipments():
    cursor.execute("select * from shipments;")
    shipments = cursor.fetchall()
    return shipments, cursor.description


def get_product_shipment():
    cursor.execute("select * from product_shipment;")
    product_shipment = cursor.fetchall()
    return product_shipment, cursor.description

def add_product_window():
    add_window = Tk()
    add_window.title("Add product")
    name_label = Label(add_window, text="Name of product-")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = Entry(add_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    type_label = Label(add_window, text="Product type-")
    type_label.grid(row=1, column=0, padx=10, pady=10)
    type_entry = Entry(add_window)
    type_entry.grid(row=1, column=1, padx=10, pady=10)

    sp_label = Label(add_window, text="Sell price-")
    sp_label.grid(row=2, column=0, padx=10, pady=10)
    sp_entry = Entry(add_window)
    sp_entry.grid(row=2, column=1, padx=10, pady=10)

    cp_label = Label(add_window, text="Cost Price-")
    cp_label.grid(row=3, column=0, padx=10, pady=10)
    cp_entry = Entry(add_window)
    cp_entry.grid(row=3, column=1, padx=10, pady=10)

    quantity_label = Label(add_window, text="Quantity")
    quantity_label.grid(row=4, column=0, padx=10, pady=10)
    qty = 0
    quantity_entry = Scale(add_window, variable=qty, from_=0, to=300, orient=HORIZONTAL)
    quantity_entry.grid(row=4, column=1, padx=10, pady=10)

    add_button = Button(add_window, text="Add",
                        command=lambda: add_product_query(name_entry.get(), type_entry.get(), sp_entry.get(),
                                                          cp_entry.get(), quantity_entry.get(), add_window))
    add_button.grid(row=5, columnspan=2, sticky='nsew')


def add_product_query(name, type_prod, sp, cp, qty, curr_window):
    curr_window.attributes("-topmost", True)
    try:
        cp = float(cp)
    except:
        messagebox.showerror("Error!", "Enter a number for cost price please")
        print(name, type_prod, sp, cp, qty)
        return

    try:
        sp = float(sp)
    except:
        messagebox.showwarning("Error!", "Enter a number for sell price please")
        print(name, type_prod, sp, cp, qty)
        return

    cursor.execute("select product_id from products;")
    product_id = cursor.fetchall()
    p_id = generate_id(product_id)
    try:
        query = "INSERT INTO products VALUES('{}','{}',{},'{}',{},{});".format(p_id, name, qty, type_prod, sp, cp)
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "New product inserted!")
        global root
        # root.nametowidget("tree_table").destroy()
        print_result(get_products(), root.nametowidget("table_frame"))
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


def update_product_window():
    update_window = Tk()
    update_window.title("Update product")
    # update_window.protocol("WM_DELETE_WINDOW", update_window.destroy())

    # update_window.geometry("500x500")

    name_label = Label(update_window, text="Select product-")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    cursor.execute("SELECT product_name from products;")
    p_names = cursor.fetchall()
    p_names = [x[0] for x in p_names]
    default_product = StringVar(update_window, name='selected')
    default_product.set(p_names[0])

    type_label = Label(update_window, text="Product type-")
    type_label.grid(row=1, column=0, padx=10, pady=10)
    type_entry = Entry(update_window, name='type_entry')
    type_entry.grid(row=1, column=1, padx=10, pady=10)

    sp_label = Label(update_window, text="Sell price-")
    sp_label.grid(row=2, column=0, padx=10, pady=10)
    sp_entry = Entry(update_window, name='sp_entry')
    sp_entry.grid(row=2, column=1, padx=10, pady=10)

    cp_label = Label(update_window, text="Cost Price-")
    cp_label.grid(row=3, column=0, padx=10, pady=10)
    cp_entry = Entry(update_window, name='cp_entry')
    cp_entry.grid(row=3, column=1, padx=10, pady=10)

    quantity_label = Label(update_window, text="Quantity")
    quantity_label.grid(row=4, column=0, padx=10, pady=10)
    quantity_entry = Entry(update_window, name='quantity_entry')
    quantity_entry.grid(row=4, column=1, padx=10, pady=10)

    dropdown = OptionMenu(update_window, default_product, *p_names)
    dropdown.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    default_product.trace('w', lambda *args, b=type_entry, c=sp_entry, d=cp_entry,
                                      e=quantity_entry: set_values_product(default_product, b, c, d, e, *args))

    update_button = Button(update_window, text="Update",
                           command=lambda: update_product_query(default_product.get(), type_entry.get(), sp_entry.get(),
                                                                cp_entry.get(), quantity_entry.get(), update_window))
    update_button.grid(row=5, columnspan=2, sticky='nsew')


def set_values_product(selected, type_entry, sp_entry, cp_entry, quantity_entry, *args):
    print("SELECT * FROM products where product_name = '{}'".format(selected.get()))
    cursor.execute("SELECT * FROM products where product_name = '{}'".format(selected.get()))
    record = cursor.fetchall()
    record = record[0]
    print(record)
    print(record[3])
    print(record[4])
    print(record[5])
    print(record[2])
    print(type_entry, sp_entry, cp_entry, quantity_entry)

    type_entry.delete(0, 'end')
    type_entry.insert(0, record[3])
    sp_entry.delete(0, 'end')
    sp_entry.insert(0, record[4])
    cp_entry.delete(0, 'end')
    cp_entry.insert(0, record[5])
    quantity_entry.delete(0, 'end')
    quantity_entry.insert(0, record[2])


def update_product_query(name, type_prod, sp, cp, qty, curr_window):
    print(name, type_prod, sp, cp, qty, curr_window)
    curr_window.attributes("-topmost", True)
    try:
        cp = float(cp)
    except:
        messagebox.showerror("Error!", "Enter a number for cost price please")
        print(name, type_prod, sp, cp, qty)
        return

    try:
        sp = float(sp)
    except:
        messagebox.showwarning("Error!", "Enter a number for sell price please")
        print(name, type_prod, sp, cp, qty)
        return

    try:
        qty = int(qty)
    except:
        messagebox.showwarning("Error!", "Enter a number for quantity please")
        print(name, type_prod, sp, cp, qty)
        return

    try:
        query = "UPDATE products SET product_type='{}', quantity={}, cost_price={}, sell_price={} Where " \
                "product_name='{}';".format(type_prod, qty, cp, sp, name)
        cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "Product updated!")
        print_result(get_products(), root.nametowidget("table_frame"))
        curr_window.destroy()
    except Exception as e:
        messagebox.showerror("Error!", "Failed to update record")
        print(e)

def delete_product_window():
    delete_window = Toplevel()
    delete_window.title("Delete product")
    delete_window.geometry("400x300")
    name_label = Label(delete_window, text="Select product-")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    cursor.execute("SELECT product_name from products;")
    p_names = cursor.fetchall()
    p_names = [x[0] for x in p_names]
    default_product = StringVar(delete_window, name='selected')
    default_product.set(p_names[0])

    dropdown = OptionMenu(delete_window, default_product, *p_names)
    dropdown.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    update_button = Button(delete_window, text="Delete",
                           command=lambda: delete_product_query(default_product.get(), delete_window))
    update_button.grid(row=5, columnspan=2, sticky='nsew')


def delete_product_query(product_name, curr_window):
    try:
        cursor.execute("DELETE from products where product_name='{}';".format(product_name))
        db.commit()
        messagebox.showinfo("Success", "Product deleted!")
        print_result(get_products(), root.nametowidget("table_frame"))
        curr_window.destroy()
    except Exception as e:
        messagebox.showerror("Error!", "Failed to delete record")
        print(e)


def shipment_window(action):
    addshipment_window = Tk()
    product_label = Label(addshipment_window, text='Product')
    product_label.grid(row=1, column=0)

    quantity_label = Label(addshipment_window, text='Quantity')
    quantity_label.grid(row=1, column=1)

    cursor.execute("SELECT product_name, product_id, cost_price from products;")
    products = cursor.fetchall()
    product_id_list = [x[1] for x in products]
    product_name_list = [x[0] for x in products]
    cost_price_list = [x[2] for x in products]
    checkbutton_list = []
    quantity_entry_list = []
    checkbutton_values = []

    for i in range(len(product_name_list)):
        checkbutton_values.append(IntVar(addshipment_window))

    for i, x in enumerate(product_name_list, 0):
        checkbutton_list.append(
            Checkbutton(addshipment_window, text=x, variable=checkbutton_values[i], onvalue=1, offvalue=0))
        checkbutton_list[i].grid(row=i + 2, column=0, sticky='w')
        quantity_entry_list.append(Entry(addshipment_window))
        quantity_entry_list[i].grid(row=i + 2, column=1)

    print(checkbutton_values)

    mode = StringVar(addshipment_window)
    mode.set('Cash')
    pay_mode_label = Label(addshipment_window, text='Payment Mode-')
    pay_mode_label.grid(row=len(product_name_list) + 2, column=0, sticky='w', pady=10)
    pay_mode_dropdown = OptionMenu(addshipment_window, mode, 'Cash', 'Cheque', 'Card')
    pay_mode_dropdown.grid(row=len(product_name_list) + 2, column=1, sticky='ew', pady=10)

    order_date_label = Label(addshipment_window, text='Order Date (YYYY/MM/DD)-')
    order_date_label.grid(row=len(product_name_list) + 3, column=0, sticky='w', pady=10)
    order_date_entry = Entry(addshipment_window)
    order_date_entry.grid(row=len(product_name_list) + 3, column=1, sticky='w', pady=10)

    delivery_date_label = Label(addshipment_window, text='Delivery Date (YYYY/MM/DD)-')
    delivery_date_label.grid(row=len(product_name_list) + 4, column=0, sticky='w')
    delivery_date_entry = Entry(addshipment_window)
    delivery_date_entry.grid(row=len(product_name_list) + 4, column=1, sticky='w')

    if action == 'add':
        add_shipment_window(addshipment_window, checkbutton_values, product_name_list, product_id_list,
                            quantity_entry_list, cost_price_list, mode, order_date_entry, delivery_date_entry)
    elif action == 'update':
        update_shipment_window(addshipment_window, checkbutton_values, product_name_list, product_id_list,
                               quantity_entry_list, cost_price_list, mode, order_date_entry, delivery_date_entry, checkbutton_list)


def add_shipment_window(addshipment_window, checkbutton_values, product_name_list, product_id_list,
                        quantity_entry_list, cost_price_list, mode, order_date_entry, delivery_date_entry):
    addshipment_button = Button(addshipment_window, text='Create shipment', command=lambda: add_shipment_query
    (checkbutton_values, product_name_list, product_id_list,
     quantity_entry_list, cost_price_list, mode, order_date_entry, delivery_date_entry, addshipment_window))
    addshipment_button.grid(row=len(product_name_list) + 5, column=0, columnspan=2, sticky='ew')
    # add payment type and order and delivery date


def add_shipment_query(check_values, product_name_list, product_id_list, quantity_entry_list, cost_price_list, pay_mode,
                       order_date, delivery_date, curr_window, s_id='0'):
    print([x.get() for x in check_values])
    print([x.get() for x in quantity_entry_list])
    print(cost_price_list)
    selected_prod = []
    qty_list = []
    cp_list = []
    total_cost = 0
    for i in range(len(product_name_list)):
        if check_values[i].get() == 1:
            selected_prod.append(product_id_list[i])
            cp_list.append(cost_price_list[i])
            try:
                qty_list.append(int(quantity_entry_list[i].get()))
                print(qty_list, cp_list, i)
                total_cost += qty_list[-1] * cp_list[-1]
            except:
                messagebox.showwarning("Error!", "Enter a number for quantity please")
                return

    cursor.execute("select shipment_id from shipments;")
    shipment_id = cursor.fetchall()
    if s_id == '0':
        s_id = generate_id(shipment_id)
    print(selected_prod, qty_list, cp_list, total_cost, pay_mode.get(), order_date.get(), delivery_date.get(), s_id)

    try:
        query = "INSERT INTO shipments VALUES('{}','{}','{}','{}',{});".format(s_id, pay_mode.get(), order_date.get(),
                                                                               delivery_date.get(), total_cost)
        print(query)
        cursor.execute(query)
        print_result(get_shipments(), root.nametowidget("table_frame"))
    except:
        messagebox.showerror("Error!", "Failed to insert record")
        return

    try:
        for i in range(len(selected_prod)):
            query = "INSERT INTO product_shipment VALUES('{}','{}',{},{});".format(s_id, selected_prod[i], cp_list[i],
                                                                                   qty_list[i])
            print(query)
            cursor.execute(query)
        db.commit()
        messagebox.showinfo("Success", "Success!")
    except:
        messagebox.showerror("Error!", "Failed to insert record")
        return

    # update qty in product list
    try:
        for i in range(len(selected_prod)):
            query = "UPDATE products SET quantity= quantity+{} WHERE product_id = '{}';".format(qty_list[i],
                                                                                                selected_prod[i])
            cursor.execute(query)
        db.commit()
        curr_window.destroy()
    except:
        messagebox.showerror("Error!", "Failed to update quantities")
        return


def update_shipment_window(addshipment_window, checkbutton_values, product_name_list, product_id_list,
                           quantity_entry_list, cost_price_list, mode, order_date_entry, delivery_date_entry,
                           checkbutton_list):
    cursor.execute("SELECT * from shipments;")
    shipments = cursor.fetchall()
    shipments = [x[0] for x in shipments]

    selected_shipment = StringVar(addshipment_window)
    selected_shipment.set(shipments[0])

    select_shipment_label = Label(addshipment_window, text="Select Shipment ID")
    select_shipment_label.grid(row=0, column=0)
    shipment_menu = OptionMenu(addshipment_window, selected_shipment, *shipments)
    shipment_menu.grid(row=0, column=1)

    updateshipment_button = Button(addshipment_window, text='Update shipment',
                                   command=lambda: update_shipment_query(selected_shipment, product_name_list,
                                                                         product_id_list, checkbutton_values,
                                                                         quantity_entry_list, mode, order_date_entry,
                                                                         delivery_date_entry, cost_price_list,
                                                                         addshipment_window)
                                   )

    updateshipment_button.grid(row=len(product_name_list) + 5, column=0, columnspan=2, sticky='ew',)

    selected_shipment.trace('w', lambda *args, b=checkbutton_values, c=product_name_list, d=product_id_list,
                                         e=quantity_entry_list, f=cost_price_list, g=mode, h=order_date_entry,
                                         i=delivery_date_entry, j=checkbutton_list: set_values_shipment(selected_shipment, b, c, d, e, f, g,
                                                                                  h, i, j, *args))
    # TODO add values to entries and create query


def update_shipment_query(selected, product_name_list, product_id_list, checkbutton_values, quantity_entry_list, pay_mode,
                          order_date, delivery_date, cost_price_list, curr_window):
    print(selected.get())
    print(product_id_list)
    print([x.get() for x in checkbutton_values])
    check_values = [x.get() for x in checkbutton_values]
    print(quantity_entry_list)
    print(pay_mode.get())
    print(order_date.get())
    print(delivery_date.get())
    delete_shipment_query(selected)
    add_shipment_query(checkbutton_values, product_name_list, product_id_list, quantity_entry_list, cost_price_list, pay_mode,
                       order_date, delivery_date, curr_window,selected.get())
    print_result(get_shipments(), root.nametowidget("table_frame"))


def set_values_shipment(selected, checkbutton_values, product_name_list, product_id_list,
                        quantity_entry_list, cost_price_list, mode, order_date_entry, delivery_date_entry,
                        checkbutton_list, *args):
    print(selected.get())
    cursor.execute("SELECT * from shipments where shipment_id = '{}'; ".format(selected.get()))
    shipment_table = cursor.fetchall()
    cursor.execute("SELECT product_id, quantity from product_shipment where shipment_id = '{}'; ".format(selected.get()))
    print(shipment_table)
    product_shipment_table = cursor.fetchall()
    product_list = [x[0] for x in product_shipment_table]
    qty_list = [x[1] for x in product_shipment_table]
    s_id = selected.get()
    pay_mode = shipment_table[0][1]
    order_date = shipment_table[0][2]
    delivery_date = shipment_table[0][3]

    for i in range(len(product_name_list)):
        checkbutton_list[i].deselect()
        quantity_entry_list[i].delete(0,'end')

    for j, p_id in enumerate(product_list, 0):
        i = product_id_list.index(p_id)
        quantity_entry_list[i].delete(0, 'end')
        quantity_entry_list[i].insert(0, qty_list[j])
        # mode
        order_date_entry.delete(0, 'end')
        order_date_entry.insert(0, order_date)
        delivery_date_entry.delete(0,'end')
        delivery_date_entry.insert(0, delivery_date)
        checkbutton_list[i].select()
        mode.set(pay_mode)

#     can update quantities, add products, dates, payment method


def delete_shipment_window():
    deleteshipment_window = Tk()

    cursor.execute("SELECT * from shipments;")
    shipments = cursor.fetchall()
    shipments = [x[0] for x in shipments]

    selected_shipment = StringVar(deleteshipment_window)
    selected_shipment.set(shipments[0])

    select_shipment_label = Label(deleteshipment_window, text="Select Shipment ID")
    select_shipment_label.grid(row=1, column=0)
    shipment_menu = OptionMenu(deleteshipment_window, selected_shipment, *shipments)
    shipment_menu.grid(row=1, column=1, sticky='ew')

    delete_button = Button(deleteshipment_window, text='Delete',
                           command=lambda: delete_shipment_query(selected_shipment, deleteshipment_window))
    delete_button.grid(row=2, column=0, columnspan=2, sticky='ew')

    shipment_table = get_shipments()
    print(shipment_table)
    print_result(shipment_table, deleteshipment_window)


def delete_shipment_query(selected_shipment, curr_window=None):
    try:
        query = " update products p inner join product_shipment ps on ps.product_id = p.product_id" \
                " set p.quantity = p.quantity - ps.quantity where shipment_id = '{}';".format(selected_shipment.get())
        print(query)
        cursor.execute(query)
        db.commit()
        # messagebox.showinfo("Success", "Quantities updated!")
    except Exception as e:
        print(e)
        messagebox.showerror("Error!", "Failed to update product quantities")

    try:
        query = "DELETE from shipments where shipment_id= '{}'".format(selected_shipment.get())
        print(query)
        cursor.execute(query)
        db.commit()
        if curr_window:
            messagebox.showinfo("Success", "Success!")
            print_result(get_shipments(), root.nametowidget("table_frame"))
            curr_window.destroy()
            delete_shipment_window()
    except:
        messagebox.showerror("Error!", "Failed to delete shipment")


# TODO ask if quantity should be reduced or not (triggers??)


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
