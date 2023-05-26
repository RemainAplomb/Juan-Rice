#===========================================================================================================#
"""
    Developer:
        Dibansa, Rahmani
    Designer:
        Garcia, Bhee Jay 
    
    Brief description of the program:
        This program is a monitoring system for a smart vending machine, developed for an undergraduate thesis.
"""
#===========================================================================================================#

#==========          IMPORTS          ==========#
# Built-in Python modules
import time
import datetime
from datetime import timedelta, date
import uuid
import hashlib

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from google.auth.transport.requests import Request

from firebase_admin import firestore

# Notifications
from plyer import notification


#========== Backend_Functionalities ==========#
"""
    This Backend_Functionalities class holds 
    the backend-related functions that we need
    
    (As for other functions, I decided to put the documentation
   for it directly. So just read along. Thank you.)

"""
class Backend_Functionalities:
    def __init__( self ):
        """
        Constructor:

        Initializes the Firebase app using the provided credentials and sets up a database reference to the root of the 
        Firebase database. It also retrieves the list of users from the database.
        """
        # Initialize Firebase app
        self.cred = credentials.Certificate('juan-rice-firebase-adminsdk-lqyju-c65f392acb.json')
        self.firebase_app = firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://juan-rice-default-rtdb.firebaseio.com/'
        })

        # Get a database reference
        self.ref = db.reference('/')

        # Read data from the database
        self.users = self.ref.child('users').get()

        # Print the users
        # print("User database: ", self.users)
    
    def get_current_date(self):
        """
        Returns the current date as a date object.
        """
        return date.today()
    
    def convert_timestamp(self, timestamp, timestamp_format = "%m-%d %H:%M"):
        """
        Converts a Unix timestamp to a formatted string representation using the specified timestamp_format.
            - timestamp: The Unix timestamp to convert.
            - timestamp_format (optional): The format string to use for the converted timestamp. 
              Default is "%m-%d %H:%M".
            - Returns the converted timestamp as a string.
        """
        dt_object = datetime.datetime.fromtimestamp(int(timestamp))
        return dt_object.strftime(timestamp_format)
    
    def convert_to_hash(self, convert_this):
        """
        Converts a string to its SHA-256 hash value.
            - convert_this: The string to convert.
            - Returns the SHA-256 hash value as a string.
        This will be used for encrypting passwords.
        """
        return hashlib.sha256(convert_this.encode()).hexdigest()
    
    def check_username_password(self, username, password):
        """
        Checks the validity of a username and password.
            - username: The username to check.
            - password: The password to check.
            - Returns True if the username and password are 
              valid, or an error message as a string if they are 
              invalid.
        """
        # Check if username and password are not empty
        if not username:
            # print('Error: empty username')
            return "Empty username"
        if not password:
            # print('Error: empty password')
            return "Empty password"
        
        # Check if username contains whitespace
        if ' ' in username:
            return "Username cannot contain whitespace"
        # Check if password contains whitespace
        if ' ' in password:
            return "Password cannot contain whitespace"

        # # Check if username and password meet minimum length requirements
        # if len(username) < 6:
        #     print('Error: username must be at least 6 characters')
        #     return "Username must be at least 6 characters"
        # if len(password) < 8:
        #     print('Error: password must be at least 8 characters')
        #     return "Password must be at least 8 characters"

        # # Check if username contains only alphanumeric characters
        # if not username.isalnum():
        #     print('Error: username must contain only alphanumeric characters')
        #     return "Username must contain only alphanumeric characters"
        return True

    def firebase_signup(self, username, password):
        """
        Creates a new user account in Firebase.
            - username: The desired username for the new account.
            - password: The password for the new account.
            - Returns a tuple containing the user data as a dictionary and a success message if the
              signup is successful, or None and an error message if an error occurs.
            - This is for the accounts for the vending machines
        """
        self.username = str(username).lower()
        self.password = str(password)
        try:
            self.prelim_check = self.check_username_password(self.username, self.password)
            if self.prelim_check != True:
                return None, self.prelim_check
            # Check if the username already exists in the database
            if self.username in self.users:
                # print('Error creating user: username already exists')
                return None, "Username already exists"

            # Create the new user account
            self.email = self.username + "@cvsu.juanrice"
            self.user_ref = db.reference('users').child(self.username)
            self.user_ref.set({
                'username': self.username,
                'password': self.password,
                'email': self.email
            })
            self.users = self.ref.child('users').get()

            self.storage_ref = db.reference('users').child(self.username).child('storage')
            self.storage_ref.update({
                'misc': {
                    'cups': 0,
                    "coin1": 0,
                    "coin2": 0
                },
                'rice': {
                    'premium': 0,
                    'standard': 0,
                    'cheap': 0
                }
            })

            self.price_ref = db.reference('users').child(self.username).child('price')
            self.price_ref.update({
                'premium': 50,
                'standard': 40,
                'cheap': 30,
            })

            self.transactions_ref = db.reference('users').child(self.username).child('transactions')
            # print("User database: ", self.users)
            # print("User Ref: ", user_ref)
            return db.reference('users').order_by_child('username').equal_to(self.username).get(), "Successful sign up"
        except Exception as e:
            # Handle error here
            # print('Error creating user: {}'.format(e))
            return None, f"Error: {e}"
    
    def firebase_signup2(self, username, password):
        """
        Creates a new user account in the 'users2' collection of Firebase.
            - username: The desired username for the new account.
            - password: The password for the new account.
            - Returns a tuple containing the user data as a dictionary and a success message if the signup is successful, 
              or None and an error message if an error occurs.
            - This is for the accounts on the monitoring system
        """
        self.username = str(username).lower()
        self.password = str(password)
        try:
            self.prelim_check = self.check_username_password(self.username, self.password)
            if self.prelim_check != True:
                return None, self.prelim_check

            # Check if the username already exists in the database
            if self.username in self.users:
                return None, "Username already exists"

            # Create the new user account
            self.email = self.username + "@cvsu.juanrice"
            self.user_ref = db.reference('users2').child(self.username)
            self.user_ref.set({
                'username': self.username,
                'password': self.password,
                'email': self.email
            })

            self.users = db.reference('users2').get()
            self.storage_ref = db.reference('users2').child(self.username).child('machines')
            if self.storage_ref.get() is None:
                self.storage_ref.set({})  # Set a placeholder value

            return self.user_ref.get(), "Successful sign up"
        except Exception as e:
            return None, f"Error: {e}"
    

    def firebase_login(self, username, password):
        """
        Performs a login operation by checking the provided username and password against the 'users' collection in Firebase.
            - username: The username of the user trying to log in.
            - password: The password of the user trying to log in.
            - Returns a tuple containing the user data as a dictionary and a success message if the login is successful, 
              or None and an error message if an error occurs.
            - This is for adding/connecting a machine to a specific account in the monitoring system
        """
        self.username = str(username).lower()
        self.password = str(password)
        try:
            self.prelim_check = self.check_username_password(self.username, self.password)
            if self.prelim_check != True:
                return None, self.prelim_check
            self.user_ref = db.reference('users').order_by_child('username').equal_to(self.username).get()
            if self.user_ref is not None and len(self.user_ref) == 1:
                self.uid = list(self.user_ref.keys())[0]
                # print(list(user_ref.keys())[0])
                if self.user_ref[self.uid]['password'] == self.password:
                    return self.user_ref[self.uid], "Successful log in"
                    #return db.reference('users').child(username).get(), "Successful log in"
                else:
                    # Handle error here if password is incorrect
                    # print("Incorrect password: ", self.user_ref[self.uid]['password'])
                    return None, "Incorrect password"
            else:
                # Handle error here if multiple users with same username or no user found
                # print("User not found")
                return None, "User not found"
        except Exception as e:
            # Handle error here
            # print('Error logging in: {}'.format(e))
            return None, f"Error: {e}"
    
    def firebase_login2(self, username, password):
        """
        Performs a login operation by checking the provided username and password against the 'users2' collection in Firebase.
            - username: The username of the user trying to log in.
            - password: The password of the user trying to log in.
            - Returns a tuple containing the user data as a dictionary and a success message if the login is successful, 
              or None and an error message if an error occurs.
            - This is for logging in an account in the monitoring system
        """
        self.username = str(username).lower()
        self.password = str(password)
        try:
            self.prelim_check = self.check_username_password(self.username, self.password)
            if self.prelim_check != True:
                return None, self.prelim_check
            self.user_ref = db.reference('users2').order_by_child('username').equal_to(self.username).get()
            if self.user_ref is not None and len(self.user_ref) == 1:
                self.uid = list(self.user_ref.keys())[0]
                # print(list(user_ref.keys())[0])
                if self.user_ref[self.uid]['password'] == self.password:
                    return self.user_ref, "Successful log in"
                else:
                    # Handle error here if password is incorrect
                    # print("Incorrect password: ", self.user_ref[self.uid]['password'])
                    return None, "Incorrect password"
            else:
                # Handle error here if multiple users with same username or no user found
                # print("User not found")
                return None, "User not found"
        except Exception as e:
            # Handle error here
            # print('Error logging in: {}'.format(e))
            return None, f"Error: {e}"

    
    def add_machine_details(self, username, machine_id, details):
        """
        Adds machine details for a specified user in the 'users2' collection of Firebase.
            - username: The username of the user.
            - machine_id: The unique ID of the machine.
            - details: A dictionary containing machine details such as name, location, and status.
            - Returns a tuple containing a boolean indicating if the machine details were added successfully 
              and a corresponding message.
        
        username = "example_user"
        machine_id = "machine1"
        details = {
            "name": "Machine 1",
            "location": "Building A",
            "status": "Active"
        }
        """
        # Get a reference to the machines node under the specified user
        machines_ref = db.reference('users2').child(username).child('machines')

        # Check if the machine ID already exists
        machine_data = machines_ref.get()
        if machine_data is not None and machine_id in machine_data:
            return False, "Machine ID already exists"

        # Set the details for the machine
        details['machine_id'] = machine_id
        machines_ref.child(machine_id).set(details)
        return True, "Machine details added successfully"
    
    def get_user_machines(self, username):
        """
        Retrieves the machines associated with a specified user from the 'users2' collection of Firebase.
            - username: The username of the user.
            - Returns a dictionary containing the machine details, or None if no machines are found.
            - This will retrieve the machines connected to the given monitoring system's account
        """
        machines_ref = db.reference('users2').child(username).child('machines')
        machines = machines_ref.get()
        if machines:
            return machines
        else:
            return None
    
    def retrieve_storage(self, username, storage_type="rice"):
        """
        Retrieves the storage details for a specified user and storage type from the 'users' collection of Firebase.
            - username: The username of the user.
            - storage_type: The type of storage (default is "rice").
            - Returns the storage details or None if the storage type is not found.
            - This will retrieve the storage details of a given vending machine
        """
        self.username = str(username).lower()
        self.storage_type = str(storage_type).lower()
        self.storage_ref = db.reference('users').child(self.username).child('storage').child(self.storage_type)
        return self.storage_ref.get()
    
    def check_storage_notification(self, username, rice_max=20, misc_max=200, threshold=0.3):
        """
        Checks the storage levels for a specified user and generates a list of storage notifications based on predefined thresholds.
            - username: The username of the user.
            - rice_max: The maximum storage limit for rice (default is 20 kg).
            - misc_max: The maximum storage limit for miscellaneous items (default is 200 units).
            - threshold: The threshold level (percentage) below which a storage notification is generated (default is 0.3).
            - Returns a list of dictionaries containing notification data, including the notification title, message, and image source.
        """
        # notification_data = [
        #     {"notif_title": "Premium Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_premium.png"},
        #     # Add more notification data as needed
        # ]
        self.notification_data = []
        self.rice_storage = self.retrieve_storage(username, "rice")
        for key, value in self.rice_storage.items():
            if (float(value)/rice_max) <= threshold:
                self.notification_data.append({"notif_title" : f"Rice: {key.capitalize()}", "notif_message" : f"{value} kg left in storage", "image_src" : f"resources/buttons/rice_alert_{key.lower()}.png"})

        self.misc_storage = self.retrieve_storage(username, "misc")
        for key, value in self.misc_storage.items():
            self.misc_type = key.lower()
            if self.misc_type.startswith("coin"):
                self.misc_type = "coins"
            if (float(value)/misc_max) <= threshold:
                self.notification_data.append({"notif_title" : f"Misc: {key.capitalize()}", "notif_message" : f"{value} {key.lower()} left in storage", "image_src" : f"resources/buttons/misc_alert_{self.misc_type}.png"})
        
        return self.notification_data

    def add_transaction(self, username, transaction_type, item_type, amount):
        """
        Adds a transaction for a specified user to the 'users' collection of Firebase.
            - username: The username of the user.
            - transaction_type: The type of transaction (e.g., "refill" or "sell").
            - item_type: The type of item in the transaction (e.g., "rice-premium" or "misc-coin1").
            - amount: The amount associated with the transaction.
            - Returns a tuple containing a boolean indicating if the transaction was added successfully and a 
              corresponding message.
        """
        self.username = str(username).lower()

        self.transaction_type = transaction_type.lower()
        self.item_type = item_type.lower()

        self.valid_transaction_types = [ "refill", "sell"]
        self.valid_rice_types = [ "rice-premium", "rice-standard", "rice-cheap"]
        self.valid_misc_types = [ "misc-cups", "misc-coin1", "misc-coin2"]

        try:
            self.amount= float(amount)
        except:
            # print("Invalid Amount")
            return False, "Invalid Amount"
        try:
            # Get the current date
            self.date = datetime.date.today().strftime('%Y-%m-%d')

            #Check if the transaction type is valid
            if self.transaction_type in self.transaction_type:
                # print( "Valid transaction type: ", self.transaction_type)
                pass
            else:
                # print( "Invalid transaction type: ", self.transaction_type)
                return False, f"Invalid transaction type: {self.transaction_type}"

            # Check if the item type is valid
            if self.item_type in self.valid_rice_types or self.item_type in self.valid_misc_types:
                # print('Valid item  type: ', self.item_type)
                pass
            else:
                # print('Invalid item type: ', self.item_type)
                return False, f'Invalid item type: {self.item_type}'
            
            # Get a reference to the user's transaction history for the current date
            self.transactions_ref = db.reference('users').child(self.username).child('transactions').child(self.date)

            while True:
                # Generate a unique transaction ID
                self.transaction_id = str(uuid.uuid4())
                # Check if the transaction ID already exists in the user's transaction history for the current date
                if self.transactions_ref.child(self.transaction_id).get() is not None:
                    pass
                else:
                    break

            # Create a new transaction object
            self.transaction = {
                'transaction_type': self.transaction_type,
                'item_type': self.item_type,
                'amount': self.amount,
                'timestamp': int(time.time())
            }
            
            # Add the transaction to the user's transaction history for the current date
            self.transactions_ref.child(self.transaction_id).set(self.transaction)

            # Update the user's storage based on the transaction type and item type
            if self.transaction_type == 'sell':
                if self.item_type.startswith('rice'):
                    self.storage_ref = db.reference('users').child(self.username).child('storage').child('rice').child(self.item_type.split('-')[1])
                    self.storage_ref.set(self.storage_ref.get() - self.amount)
                elif self.item_type.startswith('misc'):
                    self.storage_ref = db.reference('users').child(self.username).child('storage').child('misc').child(self.item_type.split('-')[1])
                    self.storage_ref.set(self.storage_ref.get() - self.amount)
            elif self.transaction_type == 'refill':
                # print(" Item Type: ", self.item_type, self.item_type.split('-')[1])
                if self.item_type.startswith('rice'):
                    self.storage_ref = db.reference('users').child(self.username).child('storage').child('rice').child(self.item_type.split('-')[1])
                    self.storage_update_amount = self.storage_ref.get() + self.amount
                    if self.storage_update_amount >= 20:
                        # Storage Limit Exceeded
                        return False, "Storage Limit Exceeded"
                    else:
                        self.storage_ref.set(self.storage_update_amount)
                elif self.item_type.startswith('misc'):
                    self.storage_ref = db.reference('users').child(self.username).child('storage').child('misc').child(self.item_type.split('-')[1])
                    self.storage_update_amount = self.storage_ref.get() + self.amount
                    if self.storage_update_amount >= 200:
                        return False, "Storage Limit Exceeded"
                    else:
                        self.storage_ref.set(self.storage_update_amount)

            # Print success message
            # print('Transaction added successfully')
            return True, "Successfully Added Transaction"
        except Exception as e:
            # Handle error here
            # print('Error adding transaction: {}'.format(e))
            return False, e
    
    def get_pricelist(self, username):
        """
        Retrieves the price list for a specified user from the 'users' collection of Firebase.
            - username: The username of the user.
            - Returns the price list or None if it is not found.
        """
        self.username = str(username).lower()
        self.price_ref = db.reference('users').child(self.username).child('price')
        return self.price_ref.get()

    def get_transactions_in_range(self, username, start_date, end_date):
        """
        Retrieves the transactions within a specified date range for a specified user from the 'users' collection of Firebase.
            - username: The username of the user.
            - start_date: The start date of the range (format: "YYYY-MM-DD").
            - end_date: The end date of the range (format: "YYYY-MM-DD").
            - Returns a list of dictionaries containing transaction data within the specified date range.
        """
        self.username = str(username).lower()
        self.start_date = start_date
        self.end_date = end_date

        try:
            # Convert start_date and end_date to date objects
            self.start_date_obj = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()
            self.end_date_obj = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()

            # Get a reference to the user's transaction history
            self.transactions_ref = db.reference('users').child(self.username).child('transactions')

            # Initialize an empty list to hold the transactions within the specified range
            self.transactions_in_range = []

            # Loop through all dates between start_date and end_date (inclusive)
            for self.single_date in (self.start_date_obj + datetime.timedelta(n) for n in range((self.end_date_obj - self.start_date_obj).days + 1)):
                self.date_str = self.single_date.strftime('%Y-%m-%d')
                self.date_transactions = self.transactions_ref.child(self.date_str).get()

                # If there are transactions for the current date, add them to the transactions_in_range list
                if self.date_transactions is not None:
                    for self.transaction_id, self.transaction_data in self.date_transactions.items():
                        self.transaction_data['transaction_id'] = self.transaction_id
                        self.transactions_in_range.append(self.transaction_data)
            
            return self.transactions_in_range

        except Exception as e:
            # Handle error here
            # print('Error getting transactions: {}'.format(e))
            return []
    
    def get_latest_transactions(self, username, num_transactions=30):
        """
        Retrieves the latest transactions for a specified user from the 'users' collection of Firebase.
            - username: The username of the user.
            - num_transactions: The number of latest transactions to retrieve (default is 30).
            - Returns a list of dictionaries containing the latest transactions.
        """
        self.username = str(username).lower()
        self.transactions_ref = db.reference('users').child(self.username).child('transactions')

        # Get a reference to the user's transactions, sorted in reverse chronological order
        self.transactions = self.transactions_ref.order_by_child('timestamp').limit_to_last(num_transactions).get()

        # print("Latest 30: ", self.transactions)

        # If there are no transactions, return an empty list
        if self.transactions is None:
            return []

        # Loop through the transactions and add them to the transactions_list
        self.transactions_list = []
        for self.transaction_id_date, self.transaction_id_data in self.transactions.items():
            for self.transaction_id, self.transaction_data in self.transaction_id_data.items():
                self.transaction_data['transaction_id'] = self.transaction_id
                # print(" Transaction ID: ", self.transaction_id)
                # print(" Transaction data: ", self.transaction_data)
                self.transactions_list.append(self.transaction_data)

        # Reverse the transactions_list so that they are in chronological order
        self.transactions_list.reverse()

        return self.transactions_list
    
    def get_sales(self, transactions):
        """
        Calculates the sales data based on the provided transactions.
        transactions: A list of dictionaries containing transaction data.
        Returns a tuple containing the sales data:
            - A dictionary (sales_by_product) with item types as keys and total sales amounts as values.
            - A nested dictionary (sales_by_date) with item types as outer keys, dates as inner keys, and sales amounts as values.
            - A dictionary (total_sales_by_date) with dates as keys and total sales amounts as values.
        """
        self.transactions = transactions
        sales_by_product = {}
        total_sales_by_date = {}
        sales_by_date = {}

        for transaction in self.transactions:
            item_type = transaction['item_type']
            amount = transaction['amount']
            date = self.convert_timestamp(transaction['timestamp'], "%y-%m-%d")
            if item_type in sales_by_product:
                sales_by_product[item_type] += amount
            else:
                sales_by_product[item_type] = amount
            if item_type in sales_by_date:
                if date in sales_by_date[item_type]:
                    sales_by_date[item_type][date] += amount
                else:
                    sales_by_date[item_type][date] = amount
            else:
                sales_by_date[item_type] = {date: amount}

            if date in total_sales_by_date:
                total_sales_by_date[date] += amount
            else:
                total_sales_by_date[date] = amount

        return sales_by_product, sales_by_date, total_sales_by_date
    

    def get_refill(self, transactions):
        """
        Calculates the refill data based on the provided transactions.
        transactions: A list of dictionaries containing transaction data.
        Returns a tuple containing the refill data:
            - A dictionary (refill_by_product) with item types as keys and total refill amounts as values.
            - A nested dictionary (refill_by_date) with item types as outer keys, dates as inner keys, and refill amounts as values.
            - A dictionary (total_refill_by_date) with dates as keys and total refill amounts as values.
        """
        self.transactions = transactions
        refill_by_product = {}
        total_refill_by_date = {}
        refill_by_date = {}

        for transaction in self.transactions:
            item_type = transaction['item_type']
            amount = transaction['amount']
            date = self.convert_timestamp(transaction['timestamp'], "%y-%m-%d")
            if item_type in refill_by_product:
                refill_by_product[item_type] += amount
            else:
                refill_by_product[item_type] = amount
            if item_type in refill_by_date:
                if date in refill_by_date[item_type]:
                    refill_by_date[item_type][date] += amount
                else:
                    refill_by_date[item_type][date] = amount
            else:
                refill_by_date[item_type] = {date: amount}

            if date in total_refill_by_date:
                total_refill_by_date[date] += amount
            else:
                total_refill_by_date[date] = amount

        return refill_by_product, refill_by_date, total_refill_by_date

    
    def process_transactions(self, transactions):
        """
        Processes the transactions and calculates the total sell and refill amounts for each item type.
        transactions: A list of dictionaries containing transaction data.
        Returns a tuple containing the summary of sell transactions and refill transactions:
            - A dictionary (sell_transactions_summary) with item types as keys and total sell amounts as values.
            - A dictionary (refill_transactions_summary) with item types as keys and total refill amounts as values.
        """
        self.transactions = transactions
        self.sell_transactions = {}
        self.refill_transactions = {}

        for self.transaction in self.transactions:
            if self.transaction['transaction_type'] == 'sell':
                self.item_type = self.transaction['item_type']
                if self.item_type in self.sell_transactions:
                    self.sell_transactions[self.item_type] += self.transaction['amount']
                else:
                    self.sell_transactions[self.item_type] = self.transaction['amount']
            elif self.transaction['transaction_type'] == 'refill':
                self.item_type = self.transaction['item_type']
                if self.item_type in self.refill_transactions:
                    self.refill_transactions[self.item_type] += self.transaction['amount']
                else:
                    self.refill_transactions[self.item_type] = self.transaction['amount']

        sell_transactions_summary = {}
        for item_type, total_amount in self.sell_transactions.items():
            sell_transactions_summary[item_type] = total_amount

        refill_transactions_summary = {}
        for item_type, total_amount in self.refill_transactions.items():
            refill_transactions_summary[item_type] = total_amount

        return sell_transactions_summary, refill_transactions_summary
    
    def categorize_transactions(self, transactions):
        """
        Categorizes the transactions into sell transactions and refill transactions based on the item type.
        transactions: A list of dictionaries containing transaction data.
        Returns a tuple containing the sell transactions and refill transactions:
            - A list of dictionaries (sell_transactions) containing sell transactions.
            - A list of dictionaries (refill_transactions) containing refill transactions.
        """
        self.transactions = transactions
        self.sell_transactions = []
        self.refill_transactions = []

        for self.transaction in self.transactions:
            if self.transaction["item_type"].startswith("rice"):
                self.item_type = self.transaction["item_type"].replace("rice-", "")
                self.transaction["item_type"] = self.item_type
                if self.transaction['transaction_type'] == 'sell':
                    self.sell_transactions.append(self.transaction)
                elif self.transaction['transaction_type'] == 'refill':
                    self.refill_transactions.append(self.transaction)
            if self.transaction["item_type"].startswith("misc"):
                self.item_type = self.transaction["item_type"].replace("misc-", "")
                self.transaction["item_type"] = self.item_type
                if self.transaction['transaction_type'] == 'refill':
                    self.refill_transactions.append(self.transaction)

        # print(self.sell_transactions)
        return self.sell_transactions, self.refill_transactions
    
    def remove_transaction(self, username, date, transaction_id):
        """
        Removes a specific transaction from the 'users' collection in the Firebase database.
            - username: The username of the user/ machine name
            - date: The date of the transaction (format: "YYYY-MM-DD").
            - transaction_id: The ID of the transaction to be removed.
            - Returns True if the transaction is successfully removed, False otherwise.
        """
        try:
            # Remove the transaction with the provided transaction_id
            db.reference('users').child(username).child('transactions').child(date).child(transaction_id).delete()
            return True  # Transaction successfully removed

        except Exception as e:
            # Handle any errors that occur during the database operation
            # print("Error removing transaction:", e)
            return False  # Failed to remove transaction
    
    def remove_machine(self, username, machineName):
        """
        Removes a specific machine from the 'machines' collection in the Firebase database.
            - username: The username of the user.
            - machineName: The name of the machine to be removed.
            - Returns True if the machine is successfully removed, False otherwise.
            - Unbinds a machine to the monitoring system account
        """
        try:
            # Remove the transaction with the provided transaction_id
            db.reference('users2').child(username).child('machines').child(machineName).delete()
            return True  # Transaction successfully removed

        except Exception as e:
            # Handle any errors that occur during the database operation
            # print("Error removing transaction:", e)
            return False  # Failed to remove transaction
    
    def push_notifications(self, notif_title, notif_message):
        """
        Displays a notification with the provided title and message using the notification library.
            - notif_title: The title of the notification.
            - notif_message: The message of the notification.
            - No return value.
        """
        notification.notify(title=notif_title,
                    message=notif_message,
                    #app_icon="path/to/icon.png",
                    #timeout=10
                    )
    


if __name__ == "__main__":
    def is_success(user, is_login=True):
        if user is not False:
            uid = list(user.keys())[0]
            # print("UID", uid)
            # print("User", user[uid])
            # print("Password", user[uid]['password'])
            if is_login:
                print(f"{user[uid]['username']} logged in successfully!")
            else:
                print(f"{user[uid]['username']} created successfully!")
        else:
            if is_login:
                print("Login failed!")
            else:
                print('Signup failed!')
        return

    # Initialize the POS class
    pos = Backend_Functionalities()

    # Sign up a new user
    # signup_user = pos.firebase_signup('r', 'r12345678')
    # is_success(signup_user, is_login=False)

    # signup_user = pos.firebase_signup('yy', 'r12345678')
    # is_success(signup_user, is_login=False)

    # signup_user = pos.firebase_signup('test_acc', 12345678)
    # is_success(signup_user, is_login=False)

    # signup_user = pos.firebase_signup('TEst_acc', 12345678)
    # is_success(signup_user, is_login=False)

    # login_user = pos.firebase_login('test_acc', '12345678')
    # is_success(login_user)

    # status, message = pos.add_transaction("test_acc", "sell", "rice-premium", 1)
    # status, message = pos.add_transaction("test_acc", "sell", "rice-premium", 2)
    # status, message = pos.add_transaction("test_acc", "sell", "rice-premium", 0.5)
    # status, message = pos.add_transaction("test_acc", "sell", "rice-standard", 1)
    # status, message = pos.add_transaction("test_acc", "sell", "rice-standard", 2)
    # status, message = pos.add_transaction("test_acc", "sell", "rice-standard", 3)

    # transactions = pos.get_transactions_in_range("test_acc", "2023-01-01", "2023-05-08")
    # transactions = pos.get_transactions_in_range("test_acc", "2023-05-08", "2023-05-08")
    # if len(transactions) == 0:
    #     print("--------------")
    #     print(" No transactions")
    #     print("--------------")
    # for transaction in transactions:
    #     print("--------------")
    #     print(" Transaction ID: ", transaction['transaction_id'])
    #     print(" Item Type: ", transaction['item_type'])
    #     print(" Amount: ", transaction['amount'])
    #     print(" Transaction Type: ", transaction['transaction_type'])
    #     print(" Timestamp: ", pos.convert_timestamp(transaction['timestamp']))
    #     print("--------------")
    
    # sell_transactions, refill_transactions = pos.process_transactions(transactions)
    # print("\n--------------\n")
    # print(" Total Sell Transactions:")
    # for item_type, total_amount in sell_transactions.items():
    #     print(f" {item_type}: {total_amount}")
    # print("\n--------------")

    # print("\n--------------\n")
    # print(" Total Refill Transactions:")
    # for item_type, total_amount in refill_transactions.items():
    #     print(f" {item_type}: {total_amount}")
    # print("\n--------------")

    # storage = pos.retrieve_storage("test_acc", "rice")
    # print("\n--------------\n")
    # print(" Total Storage:")
    # for key, value in storage.items():
    #     print(f" {key}: {value}")
    # print("\n--------------")

    # price = pos.get_pricelist("test_acc")
    # print(price)


    # Log in an existing user
    # login_user = pos.firebase_login('r', 'r')
    # is_success(login_user)

    # login_user = pos.firebase_login('r', 'r12345678')
    # is_success(login_user)

    # login_user = pos.firebase_login('Rahms', 12345678)
    # is_success(login_user)

    # login_user = pos.firebase_login('rahms', '12345678')
    # is_success(login_user)

    pos.push_notifications("Hey", "Barabaraaaa")
