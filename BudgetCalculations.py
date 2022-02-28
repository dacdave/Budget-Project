from datetime import datetime
import json
import datetime
import os.path
from os import path

class Category:
  categories = []

  @classmethod
  def add_category(cls, item):
    Category.categories.append(item)

  def __init__(self, expense_type):
    self.expense_type = expense_type
    self.ledger = []
    self.total = 0
    self.spending = 0
    self.expense_target = 0
    self.expense_target_frequency = "Monthly"
    Category.add_category(self)

  def set_target(self, amount, frequency="Monthly"):
    self.expense_target = int(amount)
    self.expense_target_frequency = frequency

  def deposit(self, amount, description="", date = datetime.datetime.now()):
    self.total += amount
    date_string = date.strftime("%d-%b-%Y")
    self.ledger.append({"amount": amount, "description": description, "date": date_string})
  
  def withdraw(self, amount, description="", date = datetime.datetime.now()):
    self.total -= amount
    self.spending += amount
    date_string = date.strftime("%d-%b-%Y")
    self.ledger.append({"amount": -amount, "description": description, "date": date_string})
    return True
  
  def transfer(self, amount, other):
    transfer = self.withdraw(amount, description=f"Transfer to {other.expense_type}")
    if transfer == True:
      other.deposit(amount, description=f"Transfer from {self.expense_type}")
    return transfer

  def check_funds(self, amount):
    if amount > self.total:
      over_target = abs(self.total - amount)
      return over_target
    else:
      return True

  def __str__(self):
    expenses = self.ledger
    format = head_spacing(self.expense_type, "*", 30)
    line_items = [format]
    for i in expenses:
      index = self.ledger.index(i)
      expense = expenses[index]
      expense_desc = expense["description"]
      expense_amount = "{:.2f}".format(expense["amount"])
      line_item = item_spacing(expense_desc, " ", 30, expense_amount)
      line_items.append(line_item)
    total = item_spacing("Total:", " ", 30, str(self.get_balance()))
    line_items.append(total)
    display = "\n".join(line_items)
    return display
    
  def get_balance(self):
    return self.total

#Default categories for expenditures
food = Category("Food")
transportation = Category("Transportation")
clothes = Category("Clothing")
fun = Category("Entertainment")
house = Category("Household")
debts = Category("Debt Payoff")
pets = Category("Pets")
misc = Category("Miscellaneous")

# def save_budget(file_name):
#   content = []
#   for i in Category.categories:
#     content.append(i.expense_type)
#     for x in i.ledger:
#         cat_ledger = []
#         for key in x:
#             cat_ledger.append(f"{key}:  {x[key]}")
#         content.append(", ".join(cat_ledger))
#     content.extend([f"Total: {i.total}", f"Spending: {i.spending}"])
#   save_file = open(f"{file_name}.txt", "w")
#   save_file.write("\n".join(content))

def save_budget(file_name):
  full_ledger = {}
  for i in Category.categories:
    full_ledger[i.expense_type] = i.ledger
  save_file = open(f"{file_name}.json", "w")
  json.dump(full_ledger, save_file)
  save_file.close()

def load_budget(file_name):
  load_file = open(f"{file_name}.json", "r")
  data = json.load(load_file)
  Category.categories.clear()
  for category in data:
    cat = Category(category)
    cat.ledger = data[category]

def head_spacing(name, symbol, length):
  space_length = length - len(name)
  left_side = symbol * (space_length//2)
  right_side = symbol * (length - len(name) - len(left_side))
  formatting = left_side + name + right_side
  return formatting

def item_spacing(description, symbol, length, amount):
  if len(description) > 23:
    descript = description[0:23]
    space_length = length - (len(descript) + len(amount))
    side = symbol * space_length
    formatting = descript + side + amount
  else:
    space_length = length - (len(description) + len(amount))
    side = symbol * space_length
    formatting = description + side + amount
  return formatting
    
def spending(categories):
    total_sum = sum(i.spending for i in categories)
    result = []
    for i in categories:
      result.append((i.expense_type, (i.spending * 100) // total_sum))
    return result


def create_spend_chart(categories):
  bar_chart = AsciiBarChart("Percentage spent by category")
  for name, value in spending(categories):
    bar_chart.add_bar(name, value)
  return str(bar_chart)

def right_align(s, width):
  return " " * (width - len(s)) + s

class AsciiBarChart:

  def __init__(self, title, bar_glyph="o"):
    self.title = title
    self.values = []
    self.bar_glyph = bar_glyph
    self.max_label_len = 0
  
  def add_bar(self, name, value):
    self.values.append((name, value))
    self.max_label_len = max(self.max_label_len, len(name))

  def __str__(self):

    def bar_line(i):
      return "  ".join(
        self.bar_glyph if value >= i else " "
        for name, value in self.values)

    def label_line(i):
      return "  ".join(
        name[i] if len(name) > i else " "
        for name, value in self.values)

    lines = [
      self.title
    ] + [
      right_align(str(i), 3) + "| " + bar_line(i) + "  "
      for i in range(100, -1, -10)
    ] + ["    " + "---" * len(self.values) + "-"] + [
      "     " + label_line(i) + "  "
      for i in range(0, self.max_label_len)
    ]

    return "\n".join(lines)

def test():
  food.deposit(1000, "deposit")
  food.transfer(100, transportation)
  transportation.deposit(5000,"new car payment plus some prep money for future payments")
  clothes.deposit(200,"new shirt")
  print(food)
  print(transportation)
  print(clothes)
  print(create_spend_chart(Category.categories))