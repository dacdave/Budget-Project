from BudgetCalculations import *
import tkinter as tk
from tkinter import messagebox

default_categories = [category.expense_type for category in Category.categories]

class UpdatableOptionMenu(tk.OptionMenu):
    def __init__(self, parent, value, *options, **kwargs):
        self.value = value
        super().__init__(parent, value, *options, **kwargs)

    def set_options(self, options):
        selection = self.value.get()
        if selection not in options:
          selection = options[0]

        menu = self["menu"]
        menu.delete(0, "end")
        for option in options:
            menu.add_command(
                label=option,
                command=lambda x=option: self.value.set(x)
            )

        self.value.set(selection)

def main():
  new_item = []

#Creation of primary Window
  window = tk.Tk()
  window.minsize(800, 300)
  window.title("Budget Manager")

#Functionality of buttons in main window
  def add_to_cat(categories, amount, description):
    for i in categories:
      if new_item[0] == i.expense_type:
        i.deposit(float(amount), description)

  def sub_from_cat(categories, amount, description):
    for i in categories:
      if new_item[0] == i.expense_type:
        i.withdraw(float(amount), description)

  def clear_text():
    value_add.delete(0, tk.END)
    desc_add.delete(0, tk.END)

  def add_deposit():
    new_item.append(amount_val.get())
    new_item.append(desc_val.get())
    add_to_cat(Category.categories, amount_val.get(), desc_val.get())
    activity.insert(tk.END, new_item)
    activity.insert(tk.END, "\n")
    new_item.clear()
    clear_text()
    select.set("Miscellaneous")

  def overdraft_submit():
      sub_from_cat(Category.categories, amount_val.get(), desc_val.get())
      activity.insert(tk.END, new_item)
      activity.insert(tk.END, "\n")
      new_item.clear()

  def confirm_window(process):
    overdraft_amount = "{:.2f}".format(process)
    overdraft_window = tk.messagebox.askquestion("Overdraft Warning", f"This withdraw will exceed your target budget by ${overdraft_amount}. Proceed?")
    if overdraft_window == "yes":
      overdraft_submit()
    else:
      new_item.clear()
      tk.messagebox.showinfo("Transaction Cancelled", "This transaction has been cancelled.")
    

  def add_withdraw():
    new_item.append(-float(amount_val.get()))
    new_item.append(desc_val.get())
    for i in Category.categories:
      if new_item[0] == i.expense_type:
        process = i.check_funds(float(amount_val.get()))
        if process == True:
          sub_from_cat(Category.categories, amount_val.get(), desc_val.get())
          activity.insert(tk.END, new_item)
          activity.insert(tk.END, "\n")
        else:
          confirm_window(process)
    clear_text()
    select.set("Miscellaneous")

  def save_screen():
    save_window = tk.Toplevel(window)
    save_window.title("Save Budget")
    save_window.geometry("200x200")
  
    def save_confirm(name):
      confirm = tk.messagebox.askquestion("File Overwrite Warning", f"{name}.json already exists. Would you like to overwrite the file?")
      if confirm == "yes":
        save_budget(file_name_val.get())
        file_name.delete(0, tk.END)
      else:
        tk.messagebox.showinfo("Save Cancelled", "The file was not saved.")

    def save_submit():
      name = file_name_val.get()
      if path.isfile(f"{name}.json"):
        save_confirm(name)
      else:
        save_budget(file_name_val.get())
        file_name.delete(0, tk.END)


    file_name_val = tk.StringVar()
    file_name = tk.Entry(save_window, textvariable=file_name_val)
    file_name.grid(row=1, column=1)

    save_button = tk.Button(save_window, text="Save", command=save_submit)
    save_button.grid(row=1, column=2)
  
  def load_screen():
    load_window = tk.Toplevel(window)
    load_window.title("Load Budget")
    load_window.geometry("200x200")

    def load_submit():
      load_budget(file_name_val.get())
      file_name.delete(0, tk.END)


    file_name_val = tk.StringVar()
    file_name = tk.Entry(load_window, textvariable=file_name_val)
    file_name.grid(row=1, column=1)

    load_button = tk.Button(load_window, text="Load", command=load_submit)
    load_button.grid(row=1, column=2)

#Beginning of category add window
  def cat_add_window():
    pop_up = tk.Toplevel(window)
    pop_up.title("Add New Category")
    pop_up.geometry("200x200")

    new_cat_val = tk.StringVar()
    new_cat = tk.Entry(pop_up, textvariable=new_cat_val)
    new_cat.grid(row=0, column=0)

    def add_category():
      cat_name = str(new_cat.get()).capitalize()
      name = Category(cat_name)
      default_categories.append(name.expense_type)
      drop_menu.set_options(default_categories)
      new_cat.delete(0,tk.END)

    submit = tk.Button(pop_up, text="Create Category", command=add_category)
    submit.grid(row=1, column=0)
# End of category add window
  
  def chart_display():
    chart_window = tk.Toplevel(window)
    chart_window.title("Spending Chart")
    chart_window.geometry("300x600")
    chart = create_spend_chart(Category.categories)
    chart_disp = tk.Label(chart_window, text=chart).pack()

#Fields and buttons on primary window
  amount_value = tk.Label(window, text="Amount").place(x=100, y=20) #Amount Field
  amount_val = tk.StringVar()
  value_add = tk.Entry(window, textvariable=amount_val)
  value_add.grid(row=0, column=1)

  descr_value = tk.Label(window, text="Description").place(x=230, y=20) #Description Field
  desc_val = tk.StringVar()
  desc_add = tk.Entry(window, textvariable=desc_val)
  desc_add.grid(row=0, column=2)

  deposit = tk.Button(window, text="Deposit", command=add_deposit)
  deposit.grid(row=0, column=0)

  withdraw = tk.Button(window, text="Withdraw", command=add_withdraw)
  withdraw.grid(row=1, column=0)

  display = tk.Label(window)
  display.grid(row=2, column=1)

  def cat_select(new_value): #Drop Down Menu category selection
    new_item.clear()
    new_item.append(new_value)
  
  select = tk.StringVar()
  select.set("Miscellaneous") #Drop Down Menu Default Value
  
  drop_menu = UpdatableOptionMenu(window, select, *default_categories, command=cat_select) #Drop Down Menu functionality
  drop_menu.grid(row=1, column=2)

  show_chart = tk.Button(window, text="Show Spending Chart", command=chart_display)
  show_chart.grid(row=2, column=2) 
  
  save = tk.Button(window, text="Save Data", command=save_screen)
  save.grid(row=2, column=0)

  load = tk.Button(window, text="Load Data", command=load_screen)
  load.grid(row=2, column=1)
  
  add_cat = tk.Button(window, text="Add Budget Category", command=cat_add_window)
  add_cat.grid(row=1, column=1)

  activity_name = tk.Label(window, text="Activity Log").place(x=350, y=10)
  activity = tk.Text(window, height=5, width=20)
  activity.grid(row=1, column=3)

  window.mainloop()



#Main program code
if __name__ == "__main__":
  main()