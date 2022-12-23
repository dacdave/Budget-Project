import psycopg2

#Account Table Commands
def account_insert(account_name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO Account (AccountName) VALUES (%s)", [account_name])
    conn.commit()
    conn.close()

def account_view_all():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT AccountID, AccountName FROM Account")
    rows = cur.fetchall()
    conn.close()
    return rows

def account_search(name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT AccountID, AccountName FROM Account WHERE name=?", [name])
    rows = cur.fetchall()
    conn.close()
    return rows

def account_update(id, name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("UPDATE Account SET AccountName=%s WHERE AccountID=%s", [name, id])
    conn.commit()
    conn.close()

def account_delete(account_id):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM Account WHERE AccountID=%s", [account_id])
    conn.commit()
    conn.close()

def account_clear():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM Account")
    conn.commit()
    conn.close()

#User Table Commands
def user_insert(user_name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO BudgetUser (UserName) VALUES (%s)", [user_name])
    conn.commit()
    conn.close()

def user_view_all():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT UserID, UserName FROM BudgetUser")
    rows = cur.fetchall()
    conn.close()
    return rows

def user_search(name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT UserID, UserName FROM BudgetUser WHERE name=?", [name])
    rows = cur.fetchall()
    conn.close()
    return rows

def user_update(id, name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("UPDATE BudgetUser SET UserName=%s WHERE UserID=%s", [name, id])
    conn.commit()
    conn.close()

def user_delete(user_id):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM BudgetUser WHERE UserID=%s", [user_id])
    conn.commit()
    conn.close()

def user_clear():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM BudgetUser")
    conn.commit()
    conn.close()

#Ledger Table Commands
def ledger_insert(ledger_name, balance, account_id):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO Ledger (LedgerName, Balance, LedgerAccountID) VALUES (%s,%s,%s)", [ledger_name, balance, account_id])
    conn.commit()
    conn.close()

def ledger_view_all():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT LedgerID, LedgerName, Balance FROM Ledger")
    rows = cur.fetchall()
    conn.close()
    return rows

def ledger_search(name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT LedgerID, LedgerName, Balance FROM Ledger WHERE name=?", [name])
    rows = cur.fetchall()
    conn.close()
    return rows

def ledger_update(id, name, balance):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("UPDATE Ledger SET LedgerName=%s, Balance=%s WHERE UserID=%s", [name, balance, id])
    conn.commit()
    conn.close()

def ledger_delete(id):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM Ledger WHERE LedgerID=%s", [id])
    conn.commit()
    conn.close()

def ledger_clear():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM Ledger")
    conn.commit()
    conn.close()

#Transaction Table Commands
def transaction_insert(amount, description, category, date, ledger, user):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO Ledger (Amount, TransactionDescription, TransactionCategory, TransactionDate, TransactionLedger, TransactionUser) VALUES (%s,%s,%s,%s,%s,%s)",
    [amount, description, category, date, ledger, user])
    conn.commit()
    conn.close()

def transaction_view_all():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT TransactionID, TransactionDate, TransactionDescription, Amount FROM BudgetTransaction")
    rows = cur.fetchall()
    conn.close()
    return rows

def transaction_search(name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT TransactionID, TransactionDate, TransactionDescription, Amount FROM BudgetTransaction WHERE name=?", [name])
    rows = cur.fetchall()
    conn.close()
    return rows

def transaction_update(id, date, description, amount, category):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("UPDATE BudgetTransaction SET TransactionDate=%s, TransactionDescription=%s, Amount=%s, TransactionCategory=%s WHERE TransactionID=%s",
    [date, description, amount, category, id])
    conn.commit()
    conn.close()

def transaction_delete(id):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM BudgetTransaction WHERE TransactionID=%s", [id])
    conn.commit()
    conn.close()

def ledger_clear():
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM BudgetTransaction")
    conn.commit()
    conn.close()


# def category_insert(category, goal, account, parent=-1):
#     conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
#     cur = conn.cursor()
#     if parent == -1:
#         cur.execute("INSERT INTO Category (CategoryName, Goal, AccountID) VALUES (%s,%s,%s)", [category, goal, account])
#     else:
#         cur.execute("INSERT INTO Category (CategoryName, ParentID, Goal, AccountID) VALUES (%s,%s,%s,%s)", [category, parent, goal, account])
#     conn.commit()
#     conn.close()

#account_insert('Main')
# account_clear()
# content = account_view()
# print(content)