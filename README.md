# Budget-Project
Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@dacdave 
dacdave
/
Budget-Project
Public
forked from chelseaharper/Budget-Project
Code
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Budget-Project/Budget App Readme
@chelseaharper
chelseaharper Readme Update
Latest commit 1b043a5 21 minutes ago
 History
 1 contributor
31 lines (23 sloc)  1.49 KB
   
Program to manage personal budgets with quickbooks style evaluation

Project creates categories of expenses to track budgeting; accept deposits, withdraws, and transfers from users, and generates a spending chart to display breakdowns of spending (NOT fluxuation in finances--deposits are excluded). Currently, data can be stored in a JSON file and read back into the program on load.

Features to add:

Implement save and restore via file storing:
write to JSON file and select file to read from when opening program

Read/Write to Files:
Read CSV to import data from bank account
Run report on overspending for various categories
Run report on spending breakdowns within a category (requires subcategories)

Date Tracking/Trend Evaluations:
Add recurring charges
Add functionality to generate a future predicting cash flow analysis from budget history
Store projected budget for categories and compare to actual numbers
Add automatic sorting into categories by expense description (Primarily for imported data)
Add custom keywords for automatic sorting

Data Visualization:
Add more types of usage charts (i.e., a deposits chart; a spending within category chart, etc.)

Database Use (SQL?):
Store data between uses
MAYBE: allow creation of different budgets and user selects which budget

Other:
Add custom budget categories (**Partially Implemented**)
Allow moving of expense from one category to another (i.e., instead of "transfer money to X Category" have a "Oh, this shirt was actually Gifts instead of Clothing" option)
