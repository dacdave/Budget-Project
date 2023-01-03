#New budget UI
#Icon attributed to freepik

from asyncio.windows_events import NULL
from tkinter import ttk
from venv import create
import BudgetCalculations
import BudgetExports
import BudgetDatabaseCommands
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import datetime
from decimal import Decimal
import psycopg2

accounts = []



window = Tk()

window.wm_title("Budget Manager")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
window.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")

base_frame = LabelFrame(window, text="Open Ledger", padx=5, pady=5)
base_frame.pack(padx=10, pady=10)

def clear_display():
    for item in ledger_box.get_children():
        ledger_box.delete(item)

def item_created(item):
    global accounts
    head = item + " created"
    if item == "Account":
        response = messagebox.askyesno(head, "Would you like to create default categories for this account?")
        if response == 1:
            accounts[0].create_defaults(BudgetCalculations.default_categories)
            fill_text = " has been created successfully. The following default categories have been added:\n"
            cat = []
            for i in accounts[0].root_category.children:
                cat.append(i.name)
                #BudgetDatabaseCommands.category_insert(i.name, 0, accounts[0].name)
            categories = "\n".join(cat)
            message = item + fill_text + categories
            messagebox.showinfo(head, message)
        else:
            fill_text = " has been created successfully. No categories have been added."
            message = item + fill_text
            messagebox.showinfo(head, message)
    else:
        message = item + " has been created successfully."
        messagebox.showinfo(head, message)


def new_account_window():
    account_window = Toplevel(window)
    account_window.title("Create New Account")
    account_window.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    account_window.geometry("300x100")

    account_name = StringVar()
    name_field = Entry(account_window, textvariable=account_name)
    name_field.grid(row=0, column=1, columnspan=2)

    account_label = Label(account_window, text="Account Name")
    account_label.grid(row=0, column=0)

    def create_account():
        global accounts
        account = BudgetCalculations.Account(account_name.get())
        BudgetDatabaseCommands.account_insert(account_name.get())
        accounts.append(account)
        item_created("Account")
        name_field.delete(0, END)

        file_menu.entryconfig("New Ledger", state="active")
        file_menu.entryconfig("Open Ledger", state="active")
        file_menu.entryconfig("Save Ledger", state="active")
        bar_menu.entryconfig("Budget", state="active")
        bar_menu.entryconfig("Edit Ledger", state="active")

        account_window.destroy()

        display_ledger()
        

    submit = Button(account_window, text="Submit", width=8, command=create_account)
    submit.grid(row=1, column=1)

    exit = Button(account_window, text="Close", width=8, command=account_window.destroy)
    exit.grid(row=1, column=2)

def display_ledger():
    global ledger_box
    account_frame = LabelFrame(window, text="Primary Ledger", borderwidth=0, highlightthickness=0, padx=5, pady=5)
    account_frame.pack(fill=BOTH, expand=1)
    ledger_frame = LabelFrame(account_frame, text="Transactions", padx=5, pady=5)
    ledger_frame.pack(fill=BOTH, expand=1)

    ledger_frame.columnconfigure(0,weight=1)
    ledger_frame.rowconfigure(0,weight=1)
    ledger_frame.columnconfigure(6,weight=0)
    ledger_font = ("Times", "14")
    columns = ("Date", "Description", "Amount", "Balance")
    style = ttk.Style()
    style.configure("myStyle.Treeview", bd=0, font=ledger_font)
    style.configure("myStyle.Treeview.Heading", font=ledger_font)
    style.layout("myStyle.Treeview", [("myStyle.Treeview.treearea",{"sticky": "nswe"})])
    ledger_box = ttk.Treeview(ledger_frame, style="myStyle.Treeview", columns=columns, show="headings")
    ledger_box.column("#0", width=0, stretch=NO)
    ledger_box.column("Date", anchor=W, width=90, minwidth=25)
    ledger_box.column("Description", anchor=W, width=180, minwidth=25)
    ledger_box.column("Amount", anchor=W, width=120, minwidth=25)
    ledger_box.column("Balance", anchor=E, width=120, minwidth=25)
    ledger_box.heading("#0", text="", anchor=W)
    ledger_box.heading("Date", text="Date", anchor=W)
    ledger_box.heading("Description", text="Description", anchor=W)
    ledger_box.heading("Amount", text="Amount", anchor=W)
    ledger_box.heading("Balance", text="Account Balance", anchor=E)


    ledger_box.grid(row=0, column=0, rowspan=5, columnspan=5, padx=500, pady=20, sticky=NSEW)
    # b = Button(account_frame, text="Close Ledger", command=account_frame.forget)
    # b.grid(row=0, column=6, sticky=EW)

def new_ledger_window():
    ledger_window = Toplevel(window)
    ledger_window.title("Create New Ledger")
    ledger_window.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    ledger_window.geometry("300x100")
        
    ledger_name = StringVar()
    name_field = Entry(ledger_window, textvariable=ledger_name)
    name_field.grid(row=0, column=1, columnspan=2)
        
    ledger_label = Label(ledger_window, text="Ledger Name")
    ledger_label.grid(row=0, column=0)
    
    def create_ledger():
        global accounts
        item_created("Ledger")
        Label(window, text=ledger_name.get()).pack()
        name_field.delete(0, END)

        file_menu.entryconfig("Save Ledger", state="active")
        bar_menu.entryconfig("Budget", state="active")

        ledger_window.destroy()
    
    submit = Button(ledger_window, text="Submit", width=8, command=create_ledger)
    submit.grid(row=1, column=1)

    exit = Button(ledger_window, text="Close", width=8, command=ledger_window.destroy)
    exit.grid(row=1, column=2)

def new_budget_window():
    budget_window = Toplevel(window)
    budget_window.title("Create New Budget")
    budget_window.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    budget_window.geometry("300x100")
        
    budget_name = StringVar()
    name_field = Entry(budget_window, textvariable=budget_name)
    name_field.grid(row=0, column=1)
        
    budget_label = Label(budget_window, text="Budget Name")
    budget_label.grid(row=0, column=0)

    def create_budget():
        global accounts
        item_created("Budget")
        Label(window, text=budget_name.get()).pack()
        name_field.delete(0, END)

        budget_menu.entryconfig("Save Budget", state="active")
        budget_menu.entryconfig("Modify Budget", state="active")
        bar_menu.entryconfig("Cash Flow", state="active")

        budget_window.destroy()
        
    submit = Button(budget_window, text="Submit", width=8, command=create_budget)
    submit.grid(row=1, column=1)

    exit = Button(budget_window, text="Close", width=8, command=budget_window.destroy)
    exit.grid(row=1, column=2)
    

def select_ledger():
    file_open_frame.pack(fill="both", expand=1)
    window.filename = filedialog.askopenfilename(initialdir="D:\Python learning materials and programs\Budget Project", title="Select a file", filetypes=(("JSON", "*.json"),("all files","*.*")))
    label_opened = Label(file_open_frame, text = window.filename)
    label_opened.grid(row=0, column=0)

    # select_ledger = Toplevel(window)
    # select_ledger.title("Select Budget")
    # select_ledger.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    # select_ledger.geometry("300x200")

    select = Label(select_ledger, text="This is where you'll choose which ledger to open.")
    select.grid(row=0, column=1)

def save_ledger():
    ledger_save = Toplevel(window)
    ledger_save.title("Save Ledger")
    ledger_save.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    ledger_save.geometry("300x200")

    select = Label(ledger_save, text="This is where you'll save the ledger.")
    select.grid(row=0, column=1)

def select_budget():
    select_budget = Toplevel(window)
    select_budget.title("Select Budget")
    select_budget.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    select_budget.geometry("300x200")

    select = Label(select_budget, text="This is where you'll choose which budget to open.")
    select.grid(row=0, column=1)

def select_account():
    select_account = Toplevel(window)
    select_account.title("Select Account")
    select_account.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    select_account.geometry("300x200")

    select = Label(select_account, text="This is where you'll choose which account to open.")
    select.grid(row=0, column=1)

def new_transaction():
    create_transaction = Toplevel(window)
    create_transaction.title("New One-Time Transaction")
    create_transaction.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    create_transaction.geometry("550x100")

    entry_frame = Frame(create_transaction, borderwidth=0, highlightthickness=0, padx=10, pady=10)
    entry_frame.grid(row=0, column=0, columnspan=100)

    date_label = Label(entry_frame, text="Transaction Date")
    amount_label = Label(entry_frame, text="Transaction Amount")
    description_label = Label(entry_frame, text="Transaction Description")
    category_label = Label(entry_frame, text="Spending Category")

    date_var = StringVar()
    date_var.set("mm-dd-yyyy")
    date_field = Entry(entry_frame, textvariable=date_var)
    amount_var = DoubleVar()
    amount_field = Entry(entry_frame, textvariable=amount_var)
    desc_var = StringVar()
    desc_field = Entry(entry_frame, textvariable=desc_var)
    cat_var = StringVar()
    cat_var.set("All")
    cat_field = Entry(entry_frame, textvariable=cat_var)

    entry_frame.columnconfigure(0, weight=0)
    entry_frame.columnconfigure(1, weight=2)
    entry_frame.columnconfigure(2, weight=0)
    entry_frame.columnconfigure(3, weight=1)
    date_label.grid(row=0, column=0, padx=10, sticky=EW)
    date_field.grid(row=0, column=1, sticky=EW)
    amount_label.grid(row=0, column=2, sticky=EW)
    amount_field.grid(row=0, column=3, padx=10, sticky=EW)
    description_label.grid(row=1, column=0, padx=10, sticky=EW)
    desc_field.grid(row=1, column=1, sticky=EW)
    category_label.grid(row=1, column=2, sticky=EW)
    cat_field.grid(row=1, column=3, padx=10, sticky=EW)

    def submit_transaction():
        global accounts
        accounts[0].ledger.add_transaction(BudgetCalculations.Transaction(
            Decimal(amount_field.get()),
            desc_field.get(),
            accounts[0].get_category(cat_field.get()),
            datetime.datetime.strptime(date_field.get(), "%m-%d-%Y").date()), accounts[0]
        )
        trans_index = len(accounts[0].ledger.transactions) - 1
        ledger_box.insert(parent="", index=END, iid=trans_index, text="", values=accounts[0].ledger.transactions[trans_index])

    submit_b = Button(create_transaction, text="Submit", width=8, command=submit_transaction)
    submit_b.grid(row=1, column=49)

    exit = Button(create_transaction, text="Close", width=8, command=create_transaction.destroy)
    exit.grid(row=1, column=50)

def new_recurring():
    new_recurring = Toplevel(window)
    new_recurring.title("New Recurring Transaction")
    new_recurring.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    new_recurring.geometry("700x100")

    entry_frame = Frame(new_recurring, borderwidth=0, highlightthickness=0, padx=10, pady=10)
    entry_frame.grid(row=0, column=0, columnspan=100)

    start_date_label = Label(entry_frame, text="First Transaction Date")
    last_date_label = Label(entry_frame, text="Last Transaction Date")
    amount_label = Label(entry_frame, text="Transaction Amount")
    description_label = Label(entry_frame, text="Transaction Description")
    category_label = Label(entry_frame, text="Spending Category")

    def activate_days(choice):
        choice = selection.get()
        if choice == "Regularly":
            days_field.config(state="normal")

    start_date_var = StringVar()
    start_date_var.set("mm-dd-yyyy")
    start_date_field = Entry(entry_frame, textvariable=start_date_var)
    last_date_var = StringVar()
    last_date_var.set("mm-dd-yyyy")
    last_date_field = Entry(entry_frame, textvariable=last_date_var)
    amount_var = DoubleVar()
    amount_field = Entry(entry_frame, textvariable=amount_var)
    desc_var = StringVar()
    desc_field = Entry(entry_frame, textvariable=desc_var)
    cat_var = StringVar()
    cat_var.set("All")
    cat_field = Entry(entry_frame, textvariable=cat_var)
    selection = StringVar()
    selection.set("Monthly")
    dropdown = OptionMenu(entry_frame, selection, "Monthly", "Annually", "Regularly", command=activate_days)
    days_var = StringVar()
    days_field = Entry(entry_frame, textvariable=days_var)
    days_field.config(state="disabled")

    entry_frame.columnconfigure(0, weight=0)
    entry_frame.columnconfigure(1, weight=2)
    entry_frame.columnconfigure(2, weight=0)
    entry_frame.columnconfigure(3, weight=1)
    entry_frame.columnconfigure(4, weight=0)
    entry_frame.columnconfigure(5, weight=1)
    start_date_label.grid(row=0, column=0, padx=10, sticky=EW)
    start_date_field.grid(row=0, column=1, sticky=EW)
    amount_label.grid(row=0, column=2, sticky=EW)
    amount_field.grid(row=0, column=3, padx=10, sticky=EW)
    description_label.grid(row=0, column=4, padx=10, sticky=EW)
    desc_field.grid(row=0, column=5, sticky=EW)
    last_date_label.grid(row=1, column=0, padx=10, sticky=EW)
    last_date_field.grid(row=1, column=1, sticky=EW)
    category_label.grid(row=1, column=2, sticky=EW)
    cat_field.grid(row=1, column=3, padx=10, sticky=EW)
    dropdown.grid(row=1, column=4, padx=10, sticky=EW)
    days_field.grid(row=1, column=5, padx=10, sticky=EW)

    if selection.get() == "Annually":
        frequency = BudgetCalculations.Yearly()
    elif selection.get() == "Regularly":
        frequency = BudgetCalculations.Regularly(int(days_field.get()))
    else:
        frequency = BudgetCalculations.Monthly()

    def submit_recurring():
        global accounts
        sample = BudgetCalculations.Transaction(
            Decimal(amount_field.get()),
            desc_field.get(),
            accounts[0].get_category(cat_field.get()),
            datetime.datetime.strptime(start_date_field.get(), "%m-%d-%Y").date()
        )
        accounts[0].schedules.append(BudgetCalculations.TransactionSchedule(
                    sample,
                    sample.date,
                    datetime.datetime.strptime(last_date_field.get(), "%m-%d-%Y").date(),
                    frequency))

    submit_b = Button(new_recurring, text="Submit", width=8, command=submit_recurring)
    submit_b.grid(row=1, column=49)

    exit = Button(new_recurring, text="Close", width=8, command=new_recurring.destroy)
    exit.grid(row=1, column=50)

def display_transactions():
    clear_display()
    get_dates = Toplevel(window)
    get_dates.title("Ledger Display")
    get_dates.iconbitmap("D:/Python learning materials and programs/Budget Project/budget.ico")
    get_dates.geometry("400x100")
    text = Label(get_dates, text="Please enter the date range you want to display transactions within.")
    start_date = Label(get_dates, text="Start Date")
    end_date = Label(get_dates, text="End Date")
    
    start_var = StringVar()
    start_var.set("mm-dd-yyyy")
    start_field = Entry(get_dates, textvariable=start_var)
    end_var = StringVar()
    end_var.set("mm-dd-yyyy")
    end_field = Entry(get_dates, textvariable=end_var)

    text.grid(row=0, column=0, columnspan=5)
    start_date.grid(row=1, column=0)
    end_date.grid(row=1, column=2)
    start_field.grid(row=1, column=1)
    end_field.grid(row=1, column=3)

    def submit_view():
        display = accounts[0].ledger.coalate_transactions(
            datetime.datetime.strptime(start_field.get(), "%m-%d-%Y").date(),
            datetime.datetime.strptime(end_field.get(), "%m-%d-%Y").date(),
            accounts[0])
        balance = 0
        for item in display:
            balance += item.get_amount()
            trans_index = display.index(item)
            entry = str(item).split()
            entry.append("{:.2f}".format(balance))
            ledger_box.insert(parent="", index=END, iid=trans_index, text="", values=entry)
        get_dates.destroy()

    submit_b = Button(get_dates, text="Submit", width=8, command=submit_view)
    submit_b.grid(row=2, column=1)

    exit = Button(get_dates, text="Close", width=8, command=get_dates.destroy)
    exit.grid(row=2, column=2)

bar_menu = Menu(window)
window.config(menu=bar_menu)

file_menu = Menu(bar_menu, tearoff=False)
bar_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Account", command=new_account_window)
file_menu.add_command(label="Open Account", command=select_account)
file_menu.add_command(label="New Ledger", command=new_ledger_window, state='disabled')
file_menu.add_command(label="Open Ledger", command=select_ledger, state='disabled')
file_menu.add_command(label="Save Ledger", command=save_ledger, state='disabled')
file_menu.add_separator()
file_menu.add_command(label="Close Program", command=window.quit)

edit_menu = Menu(bar_menu, tearoff=False)
bar_menu.add_cascade(label="Edit Ledger", menu=edit_menu, state='disabled')
edit_menu.add_command(label="Add Transaction", command=new_transaction)
edit_menu.add_command(label="Add Recurring Transaction", command=new_recurring)
edit_menu.add_command(label="Modify Transaction", command=new_ledger_window)
edit_menu.add_command(label="View Transactions", command=display_transactions)
edit_menu.add_separator()
edit_menu.add_command(label="Add Spending Category", command=new_ledger_window)
edit_menu.add_command(label="Modify Spending Category", command=new_ledger_window)
edit_menu.add_command(label="View Spending Categories", command=new_ledger_window)
edit_menu.add_separator()
edit_menu.add_command(label="Add User", command=new_ledger_window)
edit_menu.add_command(label="Modify User", command=new_ledger_window)
edit_menu.add_command(label="Select Current User", command=new_ledger_window)
edit_menu.add_command(label="View User List", command=new_ledger_window)

budget_menu = Menu(bar_menu, tearoff=False)
bar_menu.add_cascade(label="Budget", menu=budget_menu, state='disabled')
budget_menu.add_command(label="New Budget", command=new_budget_window)
budget_menu.add_command(label="Open Budget", command=select_budget)
budget_menu.add_command(label="Save Budget", command=select_budget, state='disabled')
budget_menu.add_command(label="Modify Budget", command=select_budget, state='disabled')


cash_flow_menu = Menu(bar_menu, tearoff=False)
bar_menu.add_cascade(label="Cash Flow", menu=cash_flow_menu, state='disabled')
cash_flow_menu.add_command(label="Generate Cash Flow", command=new_budget_window)
cash_flow_menu.add_command(label="Save Cash Flow", command=new_budget_window)
cash_flow_menu.add_command(label="Modify Cash Flow", command=new_budget_window)
cash_flow_menu.add_command(label="Export to Excel", command=new_budget_window)

file_open_frame = Frame(base_frame, width=450, height=450, bg="white")

window.mainloop()