from BudgetCalculations import *


def old_test():
    food.set_target(850)
    house.set_target(1667.31)
    pets.set_target(80)
    debts.set_target(85)
    transportation.set_target(60)
    fun.set_target(69)
    subs = Category("Subscriptions")
    subs.set_target(121.03)
    misc.set_target(180)
    food.transfer(100, transportation)
    transportation.deposit(
        5000, "new car payment plus some prep money for future payments")
    clothes.deposit(200, "new shirt")
    print(food)
    print(transportation)
    print(clothes)
    print(create_spend_chart(Category.categories))


def new_test():
    print("Welcome to the Budget Manager test loop.")
    start = str(input("Please enter the name of a budget. "))
    start_target = str(input("Please enter the available balance for this budget. "))
    cat_done = False
    categories = []
    while cat_done == False:
        cat_name = str(input("Please enter a category name. "))
        categories.append(cat_name)
        more_cat = str(input("Would you like to add another category?"))
        if more_cat == "n":
            cat_done = True
    for i in categories:
        i = Category_new(i)

def transaction_test():
      print("This is a test of the transaction methods.")
      main = Account("Main Account")
      food = Category_new("Food", 600)
      eatingout = food.add_child_category("Eating out", 200)
      main.ledger.add_transaction(Transaction(Decimal(500), "Paycheck", main.root_category,"03-04-2022"))
      main.ledger.add_transaction(Transaction(Decimal(-20), "Pizza", eatingout, datetime.date.today()))
      print(main.ledger.get_balance())
      print(main.ledger)
    
    



transaction_test()
