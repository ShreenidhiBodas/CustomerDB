from tkinter import *
from tkinter import messagebox

import cx_Oracle as cx

conn = cx.connect("hr/hr@pdborcl")
cursor = conn.cursor()


class NullEntryError (Exception):
    def __init__(self, msg):
        self.msg = msg


master = Tk()
master.title("Customer DB")
master.geometry("500x300")


def disable_all():
    add.config(state=DISABLED)
    show.config(state=DISABLED)
    update.config(state=DISABLED)
    delete.config(state=DISABLED)
    exit_btn.config(state=DISABLED)


def enable_all():
    add.config(state=NORMAL)
    show.config(state=NORMAL)
    update.config(state=NORMAL)
    delete.config(state=NORMAL)
    exit_btn.config(state=NORMAL)


def add_item():

    def add_data():
        enable_all()
        try:
            query = "insert into customer values ('" + ent1.get() + "', '" + ent2.get() + "', '" + ent3.get() + "', '" + ent4.get() + "')"
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully")
        except cx.DatabaseError as e:
            error_obj, = e.args
            messagebox.showerror("Error", "Database Error " + error_obj.message)

        child.destroy()

    disable_all()
    child = Tk()
    child.title("Add Data")
    child.geometry("260x200")
    lbl1 = Label(child, text="Customer ID")
    lbl1.grid(row=1, column=0)
    ent1 = Entry(child)
    ent1.grid(row=1, column=2)
    lbl2 = Label(child, text="Customer Name")
    lbl2.grid(row=2, column=0)
    ent2 = Entry(child)
    ent2.grid(row=2, column=2)
    lbl3 = Label(child, text="Acc Type")
    lbl3.grid(row=3, column=0)
    ent3 = Entry(child)
    ent3.grid(row=3, column=2)
    lbl4 = Label(child, text="Balance")
    lbl4.grid(row=4, column=0)
    ent4 = Entry(child)
    ent4.grid(row=4, column=2)

    add2 = Button(child, text="Add", command=add_data)
    add2.grid(row=6, column=1)
    child.protocol("WM_DELETE_WINDOW", lambda: (enable_all(), child.destroy()))


def del_data():

    def on_delete():
        enable_all()
        try:
            if not ent1.get():
                raise NullEntryError("Null value entered")
            query = "delete from customer where customer_id = '"+ent1.get()+"'"
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Success", "Data Deleted Successfully")
        except cx.DatabaseError as e:
            err, = e.args
            messagebox.showerror("Error", "Database Error " + err.message)
        except NullEntryError as error:
            messagebox.showerror("Error", error.msg)
        child.destroy()

    disable_all()
    child = Tk()
    child.title("Delete Data")
    child.geometry("250x200")
    lbl1 = Label(child, text="Enter Customer ID")
    lbl1.place(x=5, y=10)
    ent1 = Entry(child)
    ent1.place(x=90, y=10)
    btn1 = Button(child, text="Delete", command=on_delete)
    btn1.place(x=100, y=40)
    child.protocol("WM_DELETE_WINDOW", lambda: (enable_all(), child.destroy()))


def show_customer():

    def on_exit():
        enable_all()
        child.destroy()

    disable_all()
    child = Tk()
    child.title("Show Data")
    query = "select * from customer"
    cursor.execute(query)
    # print(cursor)
    # if cursor.rowcount == 0:
    #     messagebox.showwarning("Warning", "Table empty")
    #     on_exit()
    #     return
    i = 0
    for result in cursor:
        col_1 = result[0]
        col_2 = result[1]
        col_3 = result[2]
        col_4 = result[3]
        id1 = Label(child, text=col_1)
        id1.place(x=10, y=20+i)
        id2 = Label(child, text=col_2)
        id2.place(x=40, y=20+i)
        id3 = Label(child, text=col_3)
        id3.place(x=110, y=20+i)
        id4 = Label(child, text=col_4)
        id4.place(x=160, y=20+i)
        i = i + 20

    okay = Button(child, text="Okay", command=on_exit)
    okay.place(x=80, y=40+i)
    child.protocol("WM_DELETE_WINDOW", lambda: (enable_all(), child.destroy()))


def update_customer():

    def update_customer_1():
        enable_all()
        try:
            if not ent1.get():
                raise NullEntryError("Null value entered")
            query = "update customer set balance = '" + ent2.get() + "' where customer_id = '" + ent1.get() + "'"
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Success", "Balance Updated")
        except cx.DatabaseError as e:
            err, = e.args
            messagebox.showerror("Error", "Database Error " + err.message)
        except NullEntryError as error:
            messagebox.showerror("Error", error.msg)
        child.destroy()

    disable_all()
    child = Tk()
    child.title("Update Data")
    child.geometry("250x200")
    lbl1 = Label(child, text="Customer ID")
    lbl1.place(x=5, y=20)
    ent1 = Entry(child)
    ent1.place(x=90, y=20)
    lbl2 = Label(child, text="New Balance")
    lbl2.place(x=5, y=60)
    ent2 = Entry(child)
    ent2.place(x=90, y=60)
    btn1 = Button(child, text="Update", command=update_customer_1)
    btn1.place(x=90, y=90)
    child.protocol("WM_DELETE_WINDOW", lambda: (enable_all(), child.destroy()))


def exit_app():
    messagebox.showinfo("Alert", "Application will close")
    master.destroy()


add = Button(master, text="Add Customer", command=add_item, font=('Arial', 10), fg="#353535")
add.place(height=50, width=100, x=100, y=50)
add.config(bg="#D9D9D9")

show = Button(master, text="Show Customer", command=show_customer, font=('Arial', 10), fg="#353535")
show.place(height=50, width=100, x=270, y=50)
show.config(bg="#D9D9D9")

update = Button(master, text="Update Customer", command=update_customer, fg="#353535")
update.place(height=50, width=100, x=100, y=130)
update.config(bg="#D9D9D9")

delete = Button(master, text="Delete Customer", command=del_data, fg="#353535")
delete.place(height=50, width=100, x=270, y=130)
delete.config(bg="#D9D9D9")

Heading = Label(master, text="Customer Database", font=('Times New Roman', 20), fg="#282F44")
Heading.place(x=155, y=10)
Heading.config(bg="#F4C9A8")

exit_btn = Button(master, text="Exit", command=exit_app, font=('Arial', 10), fg="#353535")
exit_btn.place(height=50, width=100, x=190, y=200)
exit_btn.config(bg="#D9D9D9")
master.mainloop()
