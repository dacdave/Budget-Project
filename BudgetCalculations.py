from __future__ import annotations
from datetime import date, datetime
import json
import datetime
import os.path
from os import path
#from typing_extensions import Self
from typing import List, Optional
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import copy

# def __str__(self):
#         expenses = self.ledger
#         format = head_spacing(self.expense_type, "*", 30)
#         line_items = [format]
#         for i in expenses:
#             index = self.ledger.index(i)
#             expense = expenses[index]
#             expense_desc = expense["description"]
#             expense_amount = "{:.2f}".format(expense["amount"])
#             line_item = item_spacing(expense_desc, " ", 30, expense_amount)
#             line_items.append(line_item)
#         total = item_spacing("Total:", " ", 30, str(self.get_balance()))
#         target_left = item_spacing("Remaining budget:", " ", 30, str(
#             self.expense_target - self.spending))
#         line_items.append(total)
#         line_items.append(target_left)
#         display = "\n".join(line_items)
#         return display

# for i in problem:
#       len_list = [i[0], i[2]]
#       spacing = len(max(len_list, key=len)) + 2
#       l1.append(str(i[0]).rjust(spacing, " "))
#       l2.append(str(i[1]).ljust(1, " ") + str(i[2]).rjust(spacing - 1, " "))
#       l3.append("-" * spacing)
#       if resolve == True:
#           l4.append(str(i[3]).rjust(spacing, " "))
#   line1 = "    ".join(l1)
#   line2 = "    ".join(l2)
#   line3 = "    ".join(l3)

class Account:
    def __init__(self, name: str):
        self.ledger = Ledger(name)
        self.root_category = Category_new("All")
        self.root_category.add_child_category("Food")
        self.root_category.add_child_category("Transportation")
        self.root_category.add_child_category("Clothing")
        self.root_category.add_child_category("Entertainment")
        self.root_category.add_child_category("Household")
        self.root_category.add_child_category("Debt Payoff")
        self.root_category.add_child_category("Pets")
        


class Transaction:
    def __init__(
            self,
            category: Category_new,
            amount: Decimal,
            description: str,
            date: date = datetime.date.today()):

        if type(date) == str:
            self.date = datetime.datetime.strptime(date, "%m-%d-%Y")
        else:
            self.date = date
        self.amount = amount
        self.description = description
        self.category = category

    def __str__(self):
        transaction_date = self.date.strftime("%m-%d-%Y")
        transaction_amount = "$ " + "{:.2f}".format(self.amount)
        if len(transaction_amount) > 14:
            transaction_amount = "Too Large."
        name = self.description
        if len(name) > 23:
            name = name[0:24]
        elements = [
            transaction_date.ljust(9, " "),
            name.ljust(23, " "),
            transaction_amount.rjust(14, " ")]
        display = "  ".join(elements)  # should be 50 characters across
        return display

    def get_amount(self):
        return self.amount

    def get_date(self):
        return self.date

    def get_category(self):
        return self.category

    def get_description(self):
        return self.description


class Frequency(ABC):
    @abstractmethod
    def get_occurrences(
            self,
            range_start: date,
            range_end: date,
            reference_date: date):
        pass


class Monthly(Frequency):
    def get_occurrences(
            self,
            range_start: date,
            range_end: date,
            reference_date: date):
        pass


class Yearly(Frequency):
    pass


class Regularly(Frequency):
    pass


class TransactionSchedule:
    def __init__(
            self,
            template: Transaction,
            start_date: date,
            *end_date: Optional[date],
            frequency: Frequency = Monthly):
        self.template = template
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
    
    def get_transactions(self, range_start, range_end):
        dates = self.frequency.get_occurrences(range_start, range_end, self.start_date)
        sched_transactions = []
        for date in dates:
            transaction = copy(self.template)
            transaction.date = date
            sched_transactions.append(transaction)
        return sched_transactions
            




class Ledger:

    def __init__(self, name: str):
        self.name = name
        self.transactions = []
        self.balance = 0

    def __str__(self):
        header = head_spacing(self.name, "*", 50)
        elements = [header]
        for i in self.transactions:
            elements.append(str(i))
        total = item_spacing("\nBalance:", " ", 51, str(
            "$ " + "{:.2f}".format(self.get_balance())))
        elements.append(total)
        display = "\n".join(elements)  # should be 50 characters across
        return display

    def add_transaction(self, transaction: Transaction) -> None:
        self.balance += transaction.get_amount()
        self.transactions.append(transaction)
    
    def add_scheduled_transaction():
        pass

    def get_transactions_in_range(
            self, start_date: date, end_date: date) -> List[Transaction]:
        pass

    def compare(self, other: Ledger) -> LedgerDiff:
        pass

    def get_balance(self):
        return self.balance


class LedgerDiff:
    pass


class Category_new:
    def __init__(self, name: str, goal: Optional[Decimal]=None, parent: Optional[Category_new]=None):
        self.name = name
        self.parent = parent
        self.goal = goal
        self.spending = 0
        self.children = []

    def set_goal(self, amount):
        self.goal = Decimal(amount)

    def check_available(self):
        remaining = self.goal - self.spending
        if remaining <= 0:
            return "No balance available."
        else:
            return f"$ {remaining} available in budget."
    
    def add_child_category(self, *args, **kwargs):
        c = Category_new(*args, **kwargs, parent = self)
        self.children.append(c)
        return c


class Category:
    categories = ["Uncategorized"]

    @classmethod
    def add_category(cls, item):
        Category.categories.append(item)

    def __init__(self, *expense_type, **target):
        self.expense_type = expense_type
        self.ledger = []
        self.balance = 0
        self.spending = 0
        self.expense_target = target if target != None else 0
        self.expense_target_frequency = "Monthly"
        self.activity_log = []
        Category.add_category(self)

    def set_target(self, amount, frequency="Monthly"):
        self.expense_target = int(amount)
        self.expense_target_frequency = frequency

    def deposit(self, amount, description="", date=datetime.datetime.now()):
        self.balance += amount
        date_string = date.strftime("%d-%b-%Y")
        activity = {"amount": amount,
                    "activity type": "deposit", "date": date_string}
        self.activity_log.append(activity)
        self.ledger.append(
            {"amount": amount, "description": description, "date": date_string})

    def recurring_deposit(self, amount, date, description=""):
        self.balance += amount
        date_string = date.strftime("%d-%b-%Y")
        activity = {"amount": amount,
                    "activity type": "deposit", "date": date_string}
        self.activity_log.append(activity)
        self.ledger.append(
            {"amount": amount, "description": description, "date": date_string})

    def withdraw(self, amount, description="", date=datetime.datetime.now()):
        self.balance -= amount
        self.spending += amount
        date_string = date.strftime("%d-%b-%Y")
        activity = {"amount": amount, "type": "withdraw", "date": date_string}
        self.activity_log.append(activity)
        self.ledger.append(
            {"amount": -amount, "description": description, "date": date_string})
        return True

    def transfer(self, amount, other):
        transfer = self.withdraw(
            amount, description=f"Transfer to {other.expense_type}")
        if transfer == True:
            other.deposit(
                amount, description=f"Transfer from {self.expense_type}")
        return transfer

    def check_funds(self, amount):
        if amount > self.balance:
            over_target = abs(self.balance - amount)
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
        target_left = item_spacing("Remaining budget:", " ", 30, str(
            self.expense_target - self.spending))
        line_items.append(total)
        line_items.append(target_left)
        display = "\n".join(line_items)
        return display

    def get_balance(self):
        return self.balance

    def get_target(self):
        return [self.expense_target, self.expense_target_frequency]


# Default categories for expenditures
food = Category("Food")
transportation = Category("Transportation")
clothes = Category("Clothing")
fun = Category("Entertainment")
house = Category("Household")
debts = Category("Debt Payoff")
pets = Category("Pets")
misc = Category("Miscellaneous")


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


def cash_report(start, stop, initial_balance=0):
    report = []
    for i in Category.categories:
        # Pretty sure date doesn't work this way
        if i.activity_log[2] > start and i.activity_log[2] < stop:
            report.append(i.activity_log)
            # curently no attribute of class called "date"
            report.sort(key=lambda x: x.date)
