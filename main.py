from database import Database

def database_functions():

    db = Database()
    db.open_connection()

    """
    Account Administration Functions
    """
    #db.create_account("Customer_99", 2234)
    # db.create_account("Customer_5", 1537)
    all_customer = db.get_all_accounts()
    # print(all_customer)
    #db.remove_account("cust_33", 1234)
    new_pin = 9998
    db.modify_account("Cust_67", new_pin)

    """
    Banking Functions
    """
    db.login_customer("Custome_1", 2376)
    db.deposit_money(5000)  # deposit $1000
    db.deposit_money(-100)  # withdraw $500
    db.deposit_money(250)
    balance = db.avilable_balance()
    print(f"Available balance ${balance}")

    db.close_connection()


if __name__ == '__main__':
    database_functions()
