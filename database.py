import mysql.connector
import uuid
from datetime import datetime

class Database:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.user = None
        self.user_pk = None

    def open_connection(self):
        file1 = open('info.txt', 'r')
        line = file1.readline().strip()
        self.connection = mysql.connector.connect(user="root", database="piyali_db", password=line)
        self.cursor = self.connection.cursor()

    def create_account(self, user_name, user_pin):
        primary_key = self.get_key()
        addData = f"INSERT INTO customer_table (PK,NAME,PIN) VALUES('{primary_key}','{user_name}', {user_pin})"
        self.cursor.execute(addData)
        self.connection.commit()

    def remove_account(self, user_name, user_pin):
        addData = f"DELETE FROM customer_table WHERE NAME = '{user_name}' and PIN = {user_pin}"
        self.cursor.execute(addData)
        self.connection.commit()

    def modify_account(self, user_name, new_pin):

       # SELECT PK FROM customer_table WHERE name = 'Cust_67'
       # UPDATE customer_table SET PIN=9999 WHERE NAME = 'Cust_67'
        pk = self.get_cust_pk(user_name)
        if pk == None:
            print(f"Error: The customer {user_name} does not exist")
        else:
            addData = f"UPDATE customer_table SET PIN={new_pin} WHERE PK = '{pk}'"
            self.cursor.execute(addData)
            self.connection.commit()

    def get_cust_pk(self, user_name):
        testQuery = f"SELECT PK FROM customer_table  WHERE name = '{user_name}'"
        self.cursor.execute(testQuery)
        pk_list = []
        for item in self.cursor:
            pk_list.append(item[0])
        if len(pk_list) == 0:
            return None
        else:
            return pk_list[0]
        pass

    def get_all_accounts(self):
        testQuery = "SELECT NAME FROM customer_table"
        self.cursor.execute(testQuery)
        all_user_list = []
        for item in self.cursor:
            all_user_list.append(item[0])
        return all_user_list

    def login_customer(self, user_name, user_pin):

        testQuery = f"SELECT * FROM customer_table WHERE NAME = '{user_name}' and PIN = {user_pin}"
        self.cursor.execute(testQuery)
        user_list = []

        for item in self.cursor:
            user_list.append(item)

        if len(user_list) == 0:
            print (f"Error:  No user named {user_name}")
            return False
        else:
            self.user = user_list[0][1]
            self.user_pk = user_list[0][0]
            print(f"{user_name} is logged in")
        return True

    def logout_customer(self, user_name, user_pin):
        self.user = None
        self.user_pk = None

    def deposit_money(self, amount):  # negative amount is withdrawal

        if self.user == None:
            print("Error: User need to login first")
            return
        else:
            primary_key = self.get_key()
            now = now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            addData = f"INSERT INTO transaction_table (PK,FK_customer,transaction,date_time) VALUES('{primary_key}','{self.user_pk}',{amount}, '{date_time}')"
            self.cursor.execute(addData)
            self.connection.commit()

    def avilable_balance(self):
        if self.user == None:
            print("Error: User need to login first")
            return
        else:
            testQuery = f"SELECT transaction FROM transaction_table WHERE FK_customer = '{self.user_pk}'"
            self.cursor.execute(testQuery)
            balance = 0
            for item in self.cursor:
                balance = balance + item[0]

            return balance

    def get_key(self):
        key = str(uuid.uuid4())
        return key

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
