from BudgetCalculations import *

def test():
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
  transportation.deposit(5000,"new car payment plus some prep money for future payments")
  clothes.deposit(200,"new shirt")
  print(food)
  print(transportation)
  print(clothes)
  print(create_spend_chart(Category.categories))

test()
