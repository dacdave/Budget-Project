import psycopg2

#Account Table Commands
def account_insert(account_name):
    conn = psycopg2.connect("dbname=budget user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO Account (AccountName) VALUES (%s)", [account_name])
    conn.commit()
    conn.close()

def account_view():
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