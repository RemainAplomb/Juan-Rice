#===========================================================================================================#
"""
    DEVELOPER:
        DIBANSA, RAHMANI 
   BRIEF DESCRIPTION OF THE PROGRAM:
"""
#===========================================================================================================#

#========== IMPORTING NECESSARY PYTHON MODULES ==========#
"""
 THE MODULES BELOW ARE BUILT IN PYTHON MODULES.
 THERE'S NO NEED TO INSTALL THESE MODULES.
"""
import random
import sys
import os
import csv
import ast
from datetime import datetime

import hashlib


#==========  IMPORTING NECESSARY KIVY MODULES  ==========#
"""
 THESE MODULES ARE FROM KIVY. THE MODULES REQUIRED CAN BE
 ACQUIRED BY USING THESE COMMANDS:
       pip install kivy
       pip install --upgrade pip wheel setuptools
       pip install docutils pygments pypiwin32
       pip install kivy.deps.gstreamer
       pip install kivy.deps.angle
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.core.window import Window, Keyboard
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, CardTransition

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty

import kivy.utils
from kivy.utils import platform

from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.utils import get_color_from_hex

from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior

from kivy.clock import Clock
from functools import partial

from kivymd.app import MDApp

# Chart
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

# from kivymd.uix.chart import PieChart
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas, NavigationToolbar2Kivy, FigureCanvasKivyAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt




#==========  IMPORTING NECESSARY PYTHON FILES  ==========#
"""
 THESE PYTHON FILES ARE IMPORTED FROM THE SAME FOLDER.
 THE .py FILE NAMES ARE:
       Backend_Functionalities.py
"""
from Backend_Functionalities import *


#==========          GLOBAL VARIABLES          ==========#
"""
 THESE ARE THE GLOBAL VARIABLES THAT WILL BE USED BY THE
 PROGRAM'S CLASSES/OBJECTS.
 THE GLOBAL VARIABLES ARE AS FOLLOWS:
  accounts_list: THIS WILL CONTAIN ALL THE ACCOUNT NAMES.
  sys.path: THIS WILL CONTAIN THE DIRECTORY OF main.py
"""
WINDOW_MIN_WIDTH = 360
WINDOW_MIN_HEIGHT = 640

#===========================================================================================================#


#========== CLASSES FOR THE PROGRAM'S SCREENS/WINDOWS ==========#
"""
 EACH OF THESE CLASSES REPRESENTS A SCREEN THAT CAN BE SEEN IN
 THE ACTUAL ANDROID APPLICATION. THESE OBJECTS ARE REFERENCES
 USED BY THE main.kv AND SOME OF ITS SUBSIDIARY .kv FILES.

 THE SCREENS ARE AS FOLLOWS:
   StartUpScreen: THE VERY FIRST SCREEN THAT WILL WELCOME THE
                  USER WHEN THE APP RUNS.

   LogInScreen: THE SCREEN THAT FACILITATES THE USER'S LOG IN.

   SignUpScreen: THE SCREEN THAT FACILITATES THE USER'S ACCOUNT
                 CREATION.

   MainScreen: THIS SCREEN HOLDS A LIST OF WORKOUT ROUTINES.
               THIS SCREEN CAN ONLY BE ACCESSED AFTER LOGGING IN.
"""
class StartUpScreen( Screen ):
    pass


class LogInScreen( Screen ):
    pass


class SignUpScreen( Screen ):
    pass

class MachineScreen( Screen ):
    pass

class AddMachineScreen( Screen ):
    pass

class MainScreen( Screen ):
    pass

class RiceStatusScreen( Screen ):
    pass

class MiscStatusScreen( Screen ):
    pass

class SalesScreen( Screen ):
    pass

class SalesStatsScreen( Screen ):
    pass

class RefillScreen( Screen ):
    pass

class RefillHistoryScreen( Screen ):
    pass

class RefillStatsScreen( Screen ):
    pass

class NotificationScreen( Screen ):
    pass

class NotificationCard(FloatLayout):
    def __init__(self, button_text, image_source, **kwargs):
        super(NotificationCard, self).__init__(**kwargs)
        
        background = Image(source=image_source, allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        
        button = Button(text=button_text, background_color=(0, 0, 0, 0))
        self.add_widget(button)


class VerticalBar(Widget):
    value = NumericProperty(0)
    value_normalized = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])
    max = NumericProperty(100)

    def on_value(self, instance, value):
        self.value_normalized = value / self.max if self.max else 0
            

class MenuDropDown( DropDown ):
    state = BooleanProperty( False )


#========== IMAGE BUTTON CLASS ==========#
"""
 THIS CLASS IS INHERITS THE BUTTON BEHAVIOUR AND IMAGE
 MODULE FROM KIVY. THIS ALLOWS OUR PROGRAM TO HAVE A
 NEW FUNCTIONALITY THAT CATERS TO IMAGE BUTTONS.
"""
class ImageButton(ButtonBehavior, Image):
    pass

class RootLayout(RelativeLayout):
	font_scaling = NumericProperty()
	def on_size(self, *args):
		self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)

#==========               THE APP CLASS               ==========#
"""
 THE CLASS 'MainApp' IS THE CORE OF THE ENTIRE PROGRAM.
 THIS CLASS CONTAINS MOST OF THE METHODS NECESSARY TO RUN THIS
 PROGRAM.
 THE METHODS CONTAINED WITHIN THIS CLASS ARE AS FOLLOWS:
   build: THE METHOD THAT BUILDS THE KIVY DEPENDENT PROGRAM.

"""
class MainApp(MDApp):
    # APP VARIABLES
    username = "" 
    password = ""

    font_scaling = NumericProperty()

    def build(self):
        Window.size = (
			(WINDOW_MIN_WIDTH if Window.width > WINDOW_MIN_WIDTH else Window.width), 
			(WINDOW_MIN_HEIGHT if Window.height > WINDOW_MIN_HEIGHT else Window.height))
        
        self.initialize_resources()
        self.backend = Backend_Functionalities() # REFERENCE THE LOGIN AND SIGN UP SYSTEM
        self.menu_dropdown = MenuDropDown() # REFERENCE THE DROP DOWN MENU

        self.on_resize()
        Window.bind(size=self.on_resize)

        # Schedule the function to be called every 5 minutes
        Clock.schedule_interval(self.run_update_5mins, 3600)
        Clock.schedule_interval(self.run_update_1hour, 3600)  # 3600 seconds = 1 hour
        
        return Builder.load_file("main.kv") # BUILD THE KIVY APP
    
    def initialize_resources(self):
        #self.loggedInUser = "test_acc"
        # Get the current working directory
        self.current_directory = os.getcwd()

        self.clear_flags(True)
    

    def clear_flags(self, clear_user=False):
        # User related
        if clear_user:
            self.loggedInUser = None
            self.loggedInUser2 = None

        # TRANSACTION RELATED
        self.transactions = None
        self.sell_transactions = None
        self.refill_transactions = None

        # INITIALIZE
        self.machineScreen_initialized= False

        self.salesScreen_initialized = False
        self.salesStatsScreen_initialized = False
        self.riceStatusScreen_initialized = False

        self.refillScreen_initialized = False
        self.refillHistoryScreen_initialized = False
        self.refillStatsScreen_initialized = False

        self.figure = plt.figure()
        pass
    
    def run_update_5mins(self, dt):
        if self.loggedInUser == None:
            return
        # print("Updated")
        self.clear_flags()
        # notification_data = [
        #     {"notif_title": "Premium Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_premium.png"},
        #     {"notif_title": "Standard Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_standard.png"},
        #     {"notif_title": "Cheap Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_cheap.png"},
        #     {"notif_title": "Cups", "notif_message": "N cups left in storage.", "image_src" : "resources/buttons/misc_alert_cups.png"},
        #     {"notif_title": "Coin1", "notif_message": "N coins1 left in storage.", "image_src" : "resources/buttons/misc_alert_coins.png"},
        #     {"notif_title": "Coin2", "notif_message": "N coins2 left in storage.", "image_src" : "resources/buttons/misc_alert_coins.png"},
        #     # Add more notification data as needed
        # ]
    
    def run_update_1hour(self, dt):
        if self.loggedInUser == None:
            return
        self.check_storage_notifications()
    
    def check_storage_notifications(self):
        notification_data = self.backend.check_storage_notification(self.loggedInUser)
        for data in notification_data:
            self.backend.push_notifications(data["notif_title"], data["notif_message"])


    def on_resize(self, *args):
        try:
            self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)
        except ValueError:
            self.font_scaling = 1
        #print(f"font_scaling: {self.font_scaling*24}")
    
    def show_popup(self, notif_title, notif_message=None):
        if notif_message is None:
            popup = Popup(title=notif_title,
                        title_size=self.font_scaling * 15,
                        separator_height=0,
                        title_align="center",
                        size_hint=(0.9, 0.15))
        else:
            content_label = Label(text=notif_message, font_size= self.font_scaling * 15)
            popup = Popup(title=notif_title,
                        content=content_label,
                        title_size=self.font_scaling * 16,
                        separator_height=self.font_scaling * 0.8,
                        title_align="center",
                        size_hint=(0.9, 0.4))
        popup.open()
    
    def on_enter_machineScreen(self):
        if self.machineScreen_initialized == False:
            if self.loggedInUser2 == "":
                self.loggedInUser2 = "test_acc"
            self.on_MachineScreen_refresh_BTN()
            self.machineScreen_initialized = True
        self.root.current = "machine_screen"
    
    def on_enter_addMachineScreen(self):
        self.root.current = "add_machine_screen"
    
    def on_enter_riceStatusScreen(self, storage_type="rice"):
        self.max_storage = 20
        self.rice_storage = self.backend.retrieve_storage(self.loggedInUser, storage_type)

        if self.rice_storage:
            for key, value in self.rice_storage.items():
                self.tempBar_value = (value / self.max_storage) * 100
                if self.tempBar_value >= 100 :
                    self.tempBar_value = 100
                self.root.ids['rice_status_screen'].ids["RiceStatusScreen_bar_" + key].value = self.tempBar_value
                self.root.ids['rice_status_screen'].ids["RiceStatusScreen_riceLabel_" + key].text = key.capitalize()
        self.root.transition.direction = "left"
        self.root.current = "rice_status_screen"
    
    def on_enter_miscStatusScreen(self, storage_type="misc"):
        self.max_storage = 200
        self.misc_storage = self.backend.retrieve_storage(self.loggedInUser, storage_type)

        if self.misc_storage:
            for key, value in self.misc_storage.items():
                self.tempBar_value = (value / self.max_storage) * 100
                if self.tempBar_value >= 100 :
                    self.tempBar_value = 100
                self.root.ids['misc_status_screen'].ids["MiscStatusScreen_bar_" + key].value = self.tempBar_value
                self.root.ids['misc_status_screen'].ids["MiscStatusScreen_miscLabel_" + key].text = key.capitalize()
        self.root.transition.direction = "left"
        self.root.current = "misc_status_screen"
    
    def on_enter_salesScreen(self):
        if self.salesScreen_initialized == False:
            self.root.ids['sales_screen'].ids['SalesScreen_timeSpinner'].text = "Latest"
            if self.loggedInUser == "":
                self.loggedInUser = "test_acc"
            if self.transactions == None or self.salesScreen_initialized == False:
                self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
                self.populate_sales_scroll_view(self.transactions)
            else:
                self.on_SalesScreen_refresh_BTN()
            self.salesScreen_initialized = True
        self.root.current = "sales_screen"
    
    def on_enter_refillScreen(self):
        if self.refillScreen_initialized == False:
            self.root.ids['refill_screen'].ids['RefillScreen_amountInput'].text = ""
            self.root.ids['refill_screen'].ids['RefillScreen_storageTimeSpinner'].text = "Rice"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text = "Premium"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].values = ["Premium", "Standard", "Cheap"]
            self.refillScreen_initialized = True
        self.root.current = "refill_screen"
    
    def on_enter_refillHistoryScreen(self):
        if self.refillHistoryScreen_initialized == False:
            self.root.ids['refill_history_screen'].ids['RefillHistoryScreen_timeSpinner'].text = "Latest"
            if self.loggedInUser == "":
                self.loggedInUser = "test_acc"
            if self.transactions == None or self.refillHistoryScreen_initialized == False:
                self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
                self.populate_refill_history_scroll_view(self.transactions)
            else:
                self.on_RefillHistoryScreen_refresh_BTN()
            self.refillHistoryScreen_initialized = True
        self.root.current = "refill_history_screen"
    
    def on_enter_notificationScreen(self):
        # notification_data = [
        #     {"notif_title": "Premium Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_premium.png"},
        #     {"notif_title": "Standard Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_standard.png"},
        #     {"notif_title": "Cheap Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_cheap.png"},
        #     {"notif_title": "Cups", "notif_message": "N cups left in storage.", "image_src" : "resources/buttons/misc_alert_cups.png"},
        #     {"notif_title": "Coin1", "notif_message": "N coins1 left in storage.", "image_src" : "resources/buttons/misc_alert_coins.png"},
        #     {"notif_title": "Coin2", "notif_message": "N coins2 left in storage.", "image_src" : "resources/buttons/misc_alert_coins.png"},
        #     # Add more notification data as needed
        # ]
        notification_data = self.backend.check_storage_notification(self.loggedInUser)
        #print(" Notification Data: ", notification_data)
        self.populate_notification_scroll_view(notification_data)
        self.root.current = "notification_screen"
    
    def get_spinner_transactions(self, text):
        self.today = self.backend.get_current_date()
        self.current_date = self.today.strftime("%Y-%m-%d")
        self.week_earlier = (self.today - timedelta(days=7)).strftime("%Y-%m-%d")
        self.month_earlier = (self.today - timedelta(days=30)).strftime("%Y-%m-%d")

        if text == "1-day":
            self.transactions = self.backend.get_transactions_in_range(self.loggedInUser, self.current_date, self.current_date)
        elif text == "1-week":
            self.transactions = self.backend.get_transactions_in_range(self.loggedInUser, self.week_earlier, self.current_date)
        elif text == "1-month":
            self.transactions = self.backend.get_transactions_in_range(self.loggedInUser, self.month_earlier, self.current_date)
        else:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
        return self.transactions
    
    def on_salesScreen_spinner_select(self, text):
        self.transactions = self.get_spinner_transactions(text)
        self.populate_sales_scroll_view(self.transactions)
    
    def on_refillScreen_spinner_select(self, text, spinner_type="storage"):
        # self.transactions = self.get_spinner_transactions(text)
        # self.populate_sales_scroll_view(self.transactions)
        if text.lower() == "rice":
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text = "Premium"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].values = ["Premium", "Standard", "Cheap"]
        if text.lower() == "misc":
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text = "Cups"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].values = ["Cups", "Coin1", "Coin2"]
    
    def on_refillHistoryScreen_spinner_select(self, text):
        self.transactions = self.get_spinner_transactions(text)
        self.populate_refill_history_scroll_view(self.transactions)
    
    def on_RefillScreen_add_BTN(self):
        self.storage_type = self.root.ids['refill_screen'].ids['RefillScreen_storageTimeSpinner'].text
        self.item_type = self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text
        # print(" Storage Type: ", self.storage_type)
        # print(" Item Type: ", self.item_type)
        try:
            self.refill_amount = float(self.root.ids['refill_screen'].ids['RefillScreen_amountInput'].text)
            # print(" Refill Amount: ", self.refill_amount)
            self.refill_status, self.refill_message = self.backend.add_transaction(self.loggedInUser, "refill", f"{self.storage_type.lower()}-{self.item_type.lower()}", self.refill_amount)
            # print(" Refill Status: ", self.refill_status)
            # print(" Refill Message: ", self.refill_message)
            self.show_popup(self.refill_message)
        except:
            # print(" Invalid Amount Input")
            self.show_popup("Invalid Amount Input")

    def on_MachineScreen_refresh_BTN(self):
        self.machines = self.backend.get_user_machines(self.loggedInUser2)
        #print("Self Machines", self.machines)
        self.populate_machine_scroll_view(self.machines)
        

    def on_SalesScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['sales_screen'].ids['SalesScreen_timeSpinner'].text
        self.on_salesScreen_spinner_select(self.refresh_this)
        # self.show_popup("Sales History Refreshed")
    
    def on_RefillHistoryScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['refill_history_screen'].ids['RefillHistoryScreen_timeSpinner'].text
        self.on_refillHistoryScreen_spinner_select(self.refresh_this)
        # self.show_popup("Refill History Refreshed")
    
    def on_NotificationScreen_card_BTN(self, button, notif_title, notif_message):
        # print(" Title: ", notif_title)
        # print(" Message: ", notif_message)
        self.show_popup(notif_title, notif_message)
    
    def populate_machine_scroll_view(self, machines):
        print(" Here's the machine: ", machines)
        if machines == None:
            self.machines = self.backend.get_user_machines(self.loggedInUser2)
            #self.transactions2 = self.backend.get_transactions_in_range(username="test_acc", start_date="2023-05-08", end_date="2023-05-08")
        else:
            self.machines = machines
        
        if not self.machines:
            self.show_popup("No Machines")
            self.scroll_view = self.root.ids['machine_screen'].ids["MachineScreen_machineScrollView"]
            self.scroll_view.clear_widgets()
            return
        else:
            self.show_popup("Machine List Refreshed")

        # Clear the scroll view
        self.scroll_view = self.root.ids['machine_screen'].ids["MachineScreen_machineScrollView"]
        self.scroll_view.clear_widgets()

        for machineId in self.machines.keys():
            #print(" Machine2 : ", self.machines[machineId])
            self.temp_machineName = self.machines[machineId]["machineName"]
            row_layout = GridLayout(cols=3, size_hint_y=None, height=self.font_scaling * 30)
            row_layout.bind(minimum_height=row_layout.setter('height'))

            machine_name_label = Label(text=self.temp_machineName.capitalize(), font_size=self.font_scaling*12)

            login_machine_button = Button(text="Log in", font_size=self.font_scaling*12, size_hint=(None, None), size=(self.font_scaling*80, self.font_scaling*30))
            login_machine_button.bind(
                on_release=partial(
                    self.on_MachineScreen_loginMachine_BTN,
                    machineName= self.temp_machineName
                )
            )

            remove_button = Button(text="Remove", font_size=self.font_scaling*12, size_hint=(None, None), size=(self.font_scaling*80, self.font_scaling*30))
            remove_button.bind(
                on_release=partial(
                    self.on_MachineScreen_remove_BTN,
                    machineName= self.temp_machineName
                )
            )        

            row_layout.add_widget(machine_name_label)
            row_layout.add_widget(remove_button)
            row_layout.add_widget(login_machine_button)  # Add the remove button to the row

            # Set the size_hint property of each widget to control column widths
            machine_name_label.size_hint_x = 0.4  # 40% of the row width
            remove_button.size_hint_x = 0.3 # 30% of the row width
            login_machine_button.size_hint_x = 0.3  # 30% of the row width

            self.root.ids['machine_screen'].ids["MachineScreen_machineScrollView"].add_widget(row_layout)
    
    def on_MachineScreen_loginMachine_BTN(self, button, machineName):
        row_layout = button.parent
        self.confirmation_popup = Popup(
            title='Confirmation',
            title_size=self.font_scaling*15,
            content=Label(text='Are you sure you want to access this machine?'),
            size_hint=(None, None),
            size=(self.font_scaling*175, self.font_scaling*200),
            auto_dismiss=False
        )

        # Create buttons for confirmation popup
        confirm_button = Button(text='Confirm', on_release=lambda button: self.confirm_loginMachine(machineName),
                                font_size=self.font_scaling * 14,
                                # size_hint=(0.4, None),
                                height=self.font_scaling * 40)
        cancel_button = Button(text='Cancel', on_release=self.confirmation_popup.dismiss,
                            font_size=self.font_scaling * 14,
                            # size_hint=(0.4, None),
                            height=self.font_scaling * 40)
        
        # Add buttons to the confirmation popup
        self.confirmation_popup.content = BoxLayout(orientation='vertical')
        self.confirmation_popup.content.add_widget(confirm_button)
        self.confirmation_popup.content.add_widget(cancel_button)
        
        # Open the confirmation popup
        self.confirmation_popup.open()
    
    def confirm_loginMachine(self, machineName):
        self.loggedInUser = machineName
        self.clear_flags()
        self.check_storage_notifications()
        self.confirmation_popup.dismiss()
        self.root.current = "main_screen"
    

    def on_MachineScreen_remove_BTN(self, button, machineName):
        row_layout = button.parent
        self.confirmation_popup = Popup(
            title='Confirmation',
            title_size=self.font_scaling*15,
            content=Label(text='Are you sure you want to unbind this machine?'),
            size_hint=(None, None),
            size=(self.font_scaling*175, self.font_scaling*200),
            auto_dismiss=False
        )

        # Create buttons for confirmation popup
        confirm_button = Button(text='Confirm', on_release=lambda button: self.confirm_removeMachine(machineName),
                                font_size=self.font_scaling * 14,
                                # size_hint=(0.4, None),
                                height=self.font_scaling * 40)
        cancel_button = Button(text='Cancel', on_release=self.confirmation_popup.dismiss,
                            font_size=self.font_scaling * 14,
                            # size_hint=(0.4, None),
                            height=self.font_scaling * 40)
        
        # Add buttons to the confirmation popup
        self.confirmation_popup.content = BoxLayout(orientation='vertical')
        self.confirmation_popup.content.add_widget(confirm_button)
        self.confirmation_popup.content.add_widget(cancel_button)
        
        # Open the confirmation popup
        self.confirmation_popup.open()
    
    def confirm_removeMachine(self, machineName):
        self.confirmation_popup.dismiss()
        self.backend.remove_machine(self.loggedInUser2, machineName)
        self.on_MachineScreen_refresh_BTN()
        #self.show_popup("Machine unbind successful")


    def populate_notification_scroll_view(self, notification_data):
        notification_scrollview = self.root.ids['notification_screen'].ids['NotificationScreen_notificationScrollView']
        notification_scrollview.clear_widgets()

        for data in notification_data:
            row_layout = GridLayout(cols=1)
            notif_title = str(data["notif_title"])
            notif_message = str(data["notif_message"])
            # print(notif_message)
            notification_card = ImageButton(source=data["image_src"], allow_stretch=True, keep_ratio=False, on_release=partial(self.on_NotificationScreen_card_BTN, notif_title=notif_title, notif_message=notif_message))

            row_layout.add_widget(notification_card)
            notification_scrollview.add_widget(row_layout)

    
    def populate_sales_scroll_view(self, transactions):
        if transactions == None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
            #self.transactions2 = self.backend.get_transactions_in_range(username="test_acc", start_date="2023-05-08", end_date="2023-05-08")
        else:
            self.transactions = transactions
        
        if not self.transactions:
            self.show_popup("No transactions")
        else:
            self.show_popup("Sales History Refreshed")

        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        self.price_list = self.backend.get_pricelist(self.loggedInUser)

        # Clear the scroll view
        self.scroll_view = self.root.ids['sales_screen'].ids["SalesScreen_salesScrollView"]
        self.scroll_view.clear_widgets()

        for transaction in self.sell_transactions:
            self.temp_itemType = transaction["item_type"]
            row_layout = GridLayout(cols=5, size_hint_y=None, height=self.font_scaling * 30)
            row_layout.bind(minimum_height=row_layout.setter('height'))

            time_label = Label(text=self.backend.convert_timestamp(transaction['timestamp'], "%m-%d %H:%M"), font_size=self.font_scaling*10)
            rice_type_label = Label(text=self.temp_itemType.capitalize(), font_size=self.font_scaling*12)
            weight_type_label = Label(text=str(transaction['amount']), font_size=self.font_scaling*12)
            total_type_label = Label(text=str(transaction['amount'] * self.price_list[self.temp_itemType]), font_size=self.font_scaling*12)

            remove_button = Button(text="Remove", font_size=self.font_scaling*12, size_hint=(None, None), size=(self.font_scaling*80, self.font_scaling*30))
            remove_button.bind(
                on_release=partial(
                    self.remove_transaction,
                    date=self.backend.convert_timestamp(transaction['timestamp'], "%Y-%m-%d"),
                    transaction_id=transaction["transaction_id"],
                    transaction_type="sell"
                )
            )         

            row_layout.add_widget(time_label)
            row_layout.add_widget(rice_type_label)
            row_layout.add_widget(weight_type_label)
            row_layout.add_widget(total_type_label)
            row_layout.add_widget(remove_button)  # Add the remove button to the row

            # Set the size_hint property of each widget to control column widths
            time_label.size_hint_x = 0.25  # 20% of the row width
            rice_type_label.size_hint_x = 0.2  # 30% of the row width
            weight_type_label.size_hint_x = 0.175  # 20% of the row width
            total_type_label.size_hint_x = 0.175  # 20% of the row width
            remove_button.size_hint_x = 0.2  # 10% of the row width

            self.root.ids['sales_screen'].ids["SalesScreen_salesScrollView"].add_widget(row_layout)
    
    def populate_refill_history_scroll_view(self, transactions):
        if transactions == None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
            #self.transactions2 = self.backend.get_transactions_in_range(username="test_acc", start_date="2023-05-08", end_date="2023-05-08")
        else:
            self.transactions = transactions
        
        if not self.transactions:
            self.show_popup("No transactions")
        else:
            self.show_popup("Refill History Refreshed")

        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        # self.price_list = self.backend.get_pricelist(self.loggedInUser)

        # Clear the scroll view
        self.scroll_view = self.root.ids['refill_history_screen'].ids["RefillHistoryScreen_refillHistoryScrollView"]
        self.scroll_view.clear_widgets()

        for transaction in self.refill_transactions:
            self.temp_itemType = transaction["item_type"]
            row_layout = GridLayout(cols=4, size_hint_y=None, height=self.font_scaling * 30)
            row_layout.bind(minimum_height=row_layout.setter('height'))

            time_label = Label(text=self.backend.convert_timestamp(transaction['timestamp'], "%m-%d %H:%M"), font_size=self.font_scaling*10)
            item_type_label = Label(text=self.temp_itemType.capitalize(), font_size=self.font_scaling*12)
            amount_type_label = Label(text=str(transaction['amount']), font_size=self.font_scaling*12)
            # total_type_label = Label(text=str(transaction['amount'] * self.price_list[self.temp_itemType]), font_size=self.font_scaling*12)

            remove_button = Button(text="Remove", font_size=self.font_scaling*12, size_hint=(None, None), size=(self.font_scaling*80, self.font_scaling*30))
            remove_button.bind(
                on_release=partial(
                    self.remove_transaction,
                    date=self.backend.convert_timestamp(transaction['timestamp'], "%Y-%m-%d"),
                    transaction_id=transaction["transaction_id"],
                    transaction_type="refill"
                )
            )         

            row_layout.add_widget(time_label)
            row_layout.add_widget(item_type_label)
            row_layout.add_widget(amount_type_label)
            # row_layout.add_widget(total_type_label)
            row_layout.add_widget(remove_button)  # Add the remove button to the row

            # Set the size_hint property of each widget to control column widths
            time_label.size_hint_x = 0.3  # 20% of the row width
            item_type_label.size_hint_x = 0.25  # 30% of the row width
            amount_type_label.size_hint_x = 0.25  # 20% of the row width
            # total_type_label.size_hint_x = 0.175  # 20% of the row width
            remove_button.size_hint_x = 0.2  # 10% of the row width

            self.root.ids['refill_history_screen'].ids["RefillHistoryScreen_refillHistoryScrollView"].add_widget(row_layout)

    def remove_transaction(self, button, date, transaction_id, transaction_type="sell"):
        row_layout = button.parent
        self.confirmation_popup = Popup(
            title='Confirmation',
            title_size=self.font_scaling*15,
            content=Label(text='Are you sure you want to delete this transaction?'),
            size_hint=(None, None),
            size=(self.font_scaling*175, self.font_scaling*200),
            auto_dismiss=False
        )

        # Create buttons for confirmation popup
        confirm_button = Button(text='Confirm', on_release=lambda button: self.confirm_remove_transaction(row_layout, date, transaction_id, transaction_type),
                                font_size=self.font_scaling * 14,
                                # size_hint=(0.4, None),
                                height=self.font_scaling * 40)
        cancel_button = Button(text='Cancel', on_release=self.confirmation_popup.dismiss,
                            font_size=self.font_scaling * 14,
                            # size_hint=(0.4, None),
                            height=self.font_scaling * 40)
        
        # Add buttons to the confirmation popup
        self.confirmation_popup.content = BoxLayout(orientation='vertical')
        self.confirmation_popup.content.add_widget(confirm_button)
        self.confirmation_popup.content.add_widget(cancel_button)
        
        # Open the confirmation popup
        self.confirmation_popup.open()

    def confirm_remove_transaction(self, row_layout, date, transaction_id, transaction_type = "sell"):
        # Close the confirmation popup
        self.confirmation_popup.dismiss()

        remove_status = self.backend.remove_transaction(self.loggedInUser, date, transaction_id)
        if remove_status:
            # Get the reference to the scroll view
            if transaction_type == "sell":
                scroll_view = self.root.ids['sales_screen'].ids["SalesScreen_salesScrollView"]
            else:
                scroll_view = self.root.ids['refill_history_screen'].ids["RefillHistoryScreen_refillHistoryScrollView"]

            # Remove the parent widget (row layout) from the scroll view
            scroll_view.remove_widget(row_layout)

    
    def on_enter_salesStatsScreen(self):
        if self.salesStatsScreen_initialized == False:
            self.root.ids['sales_stats_screen'].ids['SalesStatsScreen_timeSpinner'].text = "Latest"
            if self.loggedInUser == "":
                self.loggedInUser = "test_acc"
            if self.transactions == None or self.salesStatsScreen_initialized == False:
                self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
                self.populate_salesStats_scroll_view(self.transactions)
            else:
                self.on_SalesStatsScreen_refresh_BTN()
            self.salesStatsScreen_initialized = True
        self.root.current = "sales_stats_screen"
    
    def on_enter_refillStatsScreen(self):
        if self.refillStatsScreen_initialized == False:
            self.root.ids['refill_stats_screen'].ids['RefillStatsScreen_timeSpinner'].text = "Latest"
            if self.loggedInUser == "":
                self.loggedInUser = "test_acc"
            if self.transactions == None or self.refillStatsScreen_initialized == False:
                self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
                self.populate_refillStats_scroll_view(self.transactions)
            else:
                self.on_RefillStatsScreen_refresh_BTN()
            self.refillStatsScreen_initialized = True
        self.root.current = "refill_stats_screen"
    
    def on_salesStatsScreen_spinner_select(self, text):
        self.transactions = self.get_spinner_transactions(text)
        self.populate_salesStats_scroll_view(self.transactions)
    
    def on_refillStatsScreen_spinner_select(self, text):
        self.transactions = self.get_spinner_transactions(text)
        self.populate_refillStats_scroll_view(self.transactions)
    
    def on_SalesStatsScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['sales_stats_screen'].ids['SalesStatsScreen_timeSpinner'].text
        self.on_salesStatsScreen_spinner_select(self.refresh_this)
    
    def on_RefillStatsScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['refill_stats_screen'].ids['RefillStatsScreen_timeSpinner'].text
        self.on_refillStatsScreen_spinner_select(self.refresh_this)
    
    def populate_salesStats_scroll_view(self, transactions=None):
        if transactions is None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
        else:
            self.transactions = transactions
        
        if not self.transactions:
            self.show_popup("No transactions")
        else:
            self.show_popup("Sales Stats Refreshed")

        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        self.sales_by_product, self.sales_by_date, self.total_sales_by_date = self.backend.get_sales(self.sell_transactions)

        # print("Sales by Product: ", self.sales_by_product)
        # print("Sales by Date: ", self.sales_by_date)
        # print("Total sales by Date: ", self.total_sales_by_date)
        # print("Transactions: ", self.transactions)

        sales_scroll_view = self.root.ids['sales_stats_screen'].ids["SalesStatsScreen_salesScrollView"]
        sales_scroll_view.clear_widgets()

        if self.transactions:
            # PIE CHART
            self.fig_pie_chart, ax = plt.subplots()
            labels = [label.capitalize() for label in self.sales_by_product.keys()]
            values = self.sales_by_product.values()
            wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%.2f%%')
            for text in texts:
                text.set_fontsize(self.font_scaling * 8)
            for autotext in autotexts:
                autotext.set_fontsize(self.font_scaling * 8)
            ax.set_aspect('auto')
            ax.set_title('Sales Pie Chart', fontsize=self.font_scaling * 16)
            canvas = FigureCanvasKivyAgg(self.fig_pie_chart)
            sales_scroll_view.add_widget(canvas)

            # BAR CHART - Sales by Rice Type
            self.fig_bar_chart, ax = plt.subplots()
            rice_types = list(self.sales_by_product.keys())
            sales_values = list(self.sales_by_product.values())
            ax.bar([rice_type.capitalize() for rice_type in rice_types], sales_values)

            # Customize the chart
            ax.set_title('Sales by Rice Type', fontsize=self.font_scaling * 16)
            ax.set_xlabel('Rice Type', fontsize=self.font_scaling * 8)
            ax.set_ylabel('Total Sales', fontsize=self.font_scaling * 8)

            # Set font size for x-axis and y-axis labels
            ax.tick_params(axis='x', labelsize=self.font_scaling * 7)
            ax.tick_params(axis='y', labelsize=self.font_scaling * 7)

            # Move the y-axis label to the right side
            ax.yaxis.set_label_position('right')
            # Convert the matplotlib figure to a Kivy widget
            canvas = FigureCanvasKivyAgg(self.fig_bar_chart)
            # Update the chart layout with the new chart
            sales_scroll_view.add_widget(canvas)

            # LINE CHART - Total Sales by Date
            sorted_dates = sorted(self.total_sales_by_date.keys())
            dates = [datetime.datetime.strptime(date, '%y-%m-%d').date() for date in sorted_dates]
            sales = [self.total_sales_by_date[date] for date in sorted_dates]
            self.fig_line_chart_total_sales, ax = plt.subplots()
            # print(" Sorted Dates: ", sorted_dates)
            # print(" Dates: ", dates)
            # print(" Sales: ", sales)
            line = ax.plot_date(sorted_dates, sales, linestyle='-', fmt='o')
            for label in ax.xaxis.get_ticklabels():
                label.set_fontsize(self.font_scaling * 7)
            for label in ax.yaxis.get_ticklabels():
                label.set_fontsize(self.font_scaling * 7)
            ax.set_title('Sales Trend', fontsize=self.font_scaling * 16)
            ax.set_xlabel('Date', fontsize=self.font_scaling * 8)
            ax.set_ylabel('Total Sales', fontsize=self.font_scaling * 8)
            ax.yaxis.set_label_position('right')
            canvas = FigureCanvasKivyAgg(self.fig_line_chart_total_sales)
            sales_scroll_view.add_widget(canvas)

            # LINE CHART - Sales by Rice Type
            self.fig_line_charts_rice_type = {}
            for rice_type, sales_data in self.sales_by_date.items():
                sorted_dates = sorted(sales_data.keys())
                sales = [sales_data[date] for date in sorted_dates]

                fig, ax = plt.subplots()
                line = ax.plot_date(sorted_dates, sales, linestyle='-', fmt='o')
                for label in ax.xaxis.get_ticklabels():
                    label.set_fontsize(self.font_scaling * 7)
                for label in ax.yaxis.get_ticklabels():
                    label.set_fontsize(self.font_scaling * 7)
                ax.set_title(f'{rice_type.capitalize()} Sales Trend', fontsize=self.font_scaling * 16)
                ax.set_xlabel('Date', fontsize=self.font_scaling * 8)
                ax.set_ylabel('Total Sales', fontsize=self.font_scaling * 8)
                ax.yaxis.set_label_position('right')
                
                self.fig_line_charts_rice_type[rice_type] = fig
                canvas = FigureCanvasKivyAgg(fig)
                sales_scroll_view.add_widget(canvas)
    
    def populate_refillStats_scroll_view(self, transactions=None):
        if transactions is None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
        else:
            self.transactions = transactions
        
        if not self.transactions:
            self.show_popup("No transactions")
        else:
            self.show_popup("Refill Stats Refreshed")

        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        self.refill_by_product, self.refill_by_date, self.total_refill_by_date = self.backend.get_refill(self.refill_transactions)

        # print("Refill by Product: ", self.refill_by_product)
        # print("Refill by Date: ", self.refill_by_date)
        # print("Total refill by Date: ", self.total_refill_by_date)
        # print("Transactions: ", self.transactions)

        refill_scroll_view = self.root.ids['refill_stats_screen'].ids["RefillStatsScreen_refillScrollView"]
        refill_scroll_view.clear_widgets()

        if self.transactions:
            # PIE CHART
            self.fig_pie_chart, ax = plt.subplots()
            labels = [label.capitalize() for label in self.refill_by_product.keys()]
            values = self.refill_by_product.values()
            wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%.2f%%')
            for text in texts:
                text.set_fontsize(self.font_scaling * 8)
            for autotext in autotexts:
                autotext.set_fontsize(self.font_scaling * 8)
            ax.set_aspect('auto')
            ax.set_title('Refill Pie Chart', fontsize=self.font_scaling * 16)
            canvas = FigureCanvasKivyAgg(self.fig_pie_chart)
            refill_scroll_view.add_widget(canvas)

            # BAR CHART - Refill by Item Type
            self.fig_bar_chart, ax = plt.subplots()
            item_types = list(self.refill_by_product.keys())
            refill_values = list(self.refill_by_product.values())
            ax.bar([item_type.capitalize() for item_type in item_types], refill_values)

            # Customize the chart
            ax.set_title('Refill by Item Type', fontsize=self.font_scaling * 16)
            ax.set_xlabel('Item Type', fontsize=self.font_scaling * 8)
            ax.set_ylabel('Total Refill', fontsize=self.font_scaling * 8)

            # Set font size for x-axis and y-axis labels
            ax.tick_params(axis='x', labelsize=self.font_scaling * 7)
            ax.tick_params(axis='y', labelsize=self.font_scaling * 7)

            # Move the y-axis label to the right side
            ax.yaxis.set_label_position('right')
            # Convert the matplotlib figure to a Kivy widget
            canvas = FigureCanvasKivyAgg(self.fig_bar_chart)
            # Update the chart layout with the new chart
            refill_scroll_view.add_widget(canvas)

            # LINE CHART - Total Refill by Date
            sorted_dates = sorted(self.total_refill_by_date.keys())
            dates = [datetime.datetime.strptime(date, '%y-%m-%d').date() for date in sorted_dates]
            refill = [self.total_refill_by_date[date] for date in sorted_dates]
            self.fig_line_chart_total_refill, ax = plt.subplots()
            # print(" Sorted Dates: ", sorted_dates)
            # print(" Dates: ", dates)
            # print(" Refill: ", refill)
            line = ax.plot_date(sorted_dates, refill, linestyle='-', fmt='o')
            for label in ax.xaxis.get_ticklabels():
                label.set_fontsize(self.font_scaling * 7)
            for label in ax.yaxis.get_ticklabels():
                label.set_fontsize(self.font_scaling * 7)
            ax.set_title('Refill Trend', fontsize=self.font_scaling * 16)
            ax.set_xlabel('Date', fontsize=self.font_scaling * 8)
            ax.set_ylabel('Total Refill', fontsize=self.font_scaling * 8)
            ax.yaxis.set_label_position('right')
            canvas = FigureCanvasKivyAgg(self.fig_line_chart_total_refill)
            refill_scroll_view.add_widget(canvas)

            # LINE CHART - Refill by Item Type
            self.fig_line_charts_item_type = {}
            for item_type, refill_data in self.refill_by_date.items():
                sorted_dates = sorted(refill_data.keys())
                refill = [refill_data[date] for date in sorted_dates]

                fig, ax = plt.subplots()
                line = ax.plot_date(sorted_dates, refill, linestyle='-', fmt='o')
                for label in ax.xaxis.get_ticklabels():
                    label.set_fontsize(self.font_scaling * 7)
                for label in ax.yaxis.get_ticklabels():
                    label.set_fontsize(self.font_scaling * 7)
                ax.set_title(f'{item_type.capitalize()} Refill Trend', fontsize=self.font_scaling * 16)
                ax.set_xlabel('Date', fontsize=self.font_scaling * 8)
                ax.set_ylabel('Total Refill', fontsize=self.font_scaling * 8)
                ax.yaxis.set_label_position('right')
                
                self.fig_line_charts_item_type[item_type] = fig
                canvas = FigureCanvasKivyAgg(fig)
                refill_scroll_view.add_widget(canvas)
    

    def on_SalesStatsScreen_export_BTN(self):
        # Determine the platform
        if os.name == 'posix':  # POSIX systems (Linux, macOS)
            self.save_directory = os.path.join(self.current_directory, "save_directory")
        else:  # Windows
            self.save_directory = os.path.join(self.current_directory, "save_directory")

        # Create the save directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        # Save sales transaction CSV
        sales_transactions_filename = "sales_transactions.csv"
        sales_transactions_path = os.path.join(self.save_directory, sales_transactions_filename)

        with open(sales_transactions_path, 'w', newline='') as csvfile:
            fieldnames = self.sell_transactions[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for transaction in self.sell_transactions:
                writer.writerow(dict(transaction))

        # Save the graphs one by one
        if self.transactions:
            # Save the pie chart
            pie_chart_path = os.path.join(self.save_directory, "sales_pie_chart.png")
            self.save_figure(self.fig_pie_chart, pie_chart_path)

            # Save the bar chart
            bar_chart_path = os.path.join(self.save_directory, "sales_bar_chart.png")
            self.save_figure(self.fig_bar_chart, bar_chart_path)

            # Save the line chart for total sales by date
            line_chart_total_sales_path = os.path.join(self.save_directory, "line_chart_total_sales.png")
            self.save_figure(self.fig_line_chart_total_sales, line_chart_total_sales_path)

            # Save the line charts for sales by rice type
            for rice_type, fig_line_chart_rice_type in self.fig_line_charts_rice_type.items():
                line_chart_rice_type_path = os.path.join(self.save_directory, f"line_chart_{rice_type}_sales.png")
                self.save_figure(fig_line_chart_rice_type, line_chart_rice_type_path)

            # Show a message indicating the graphs have been saved
            # print("Graphs saved successfully!")
            self.show_popup("Graphs saved successfully!")
    
    def on_RefillStatsScreen_export_BTN(self):
        # Determine the platform
        if os.name == 'posix':  # POSIX systems (Linux, macOS)
            self.save_directory = os.path.join(self.current_directory, "save_directory")
        else:  # Windows
            self.save_directory = os.path.join(self.current_directory, "save_directory")

        # Create the save directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        # Save refill transaction CSV
        refill_transactions_filename = "refill_transactions.csv"
        refill_transactions_path = os.path.join(self.save_directory, refill_transactions_filename)

        with open(refill_transactions_path, 'w', newline='') as csvfile:
            fieldnames = self.refill_transactions[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for transaction in self.refill_transactions:
                writer.writerow(dict(transaction))

        # Save the graphs one by one
        if self.transactions:
            # Save the pie chart
            pie_chart_path = os.path.join(self.save_directory, "refill_pie_chart.png")
            self.save_figure(self.fig_pie_chart, pie_chart_path)

            # Save the bar chart
            bar_chart_path = os.path.join(self.save_directory, "refill_bar_chart.png")
            self.save_figure(self.fig_bar_chart, bar_chart_path)

            # Save the line chart for total refill by date
            line_chart_total_refill_path = os.path.join(self.save_directory, "line_chart_total_refill.png")
            self.save_figure(self.fig_line_chart_total_refill, line_chart_total_refill_path)

            # Save the line charts for refill by item type
            for item_type, fig_line_chart_item_type in self.fig_line_charts_item_type.items():
                line_chart_item_type_path = os.path.join(self.save_directory, f"line_chart_{item_type}_refill.png")
                self.save_figure(fig_line_chart_item_type, line_chart_item_type_path)

            # Show a message indicating the graphs have been saved
            # print("Graphs saved successfully!")
            self.show_popup("Graphs saved successfully!")
    
    def on_MainScreen_signout_BTN(self):
        self.clear_flags(True)
        self.show_popup("Succesfully logged out")
        self.root.current = "startup_screen"
        self.root.transition.direction = "right"
        # print(" Logged in user: ", self.loggedInUser)


    def save_figure(self, fig, save_path):
        # Save the figure to the specified path
        fig.savefig(save_path)
        plt.close(fig)


    def prevent_keypress(self, *args):
        keycode = args[1] if len(args) > 1 else None
        if isinstance(keycode, tuple) and keycode[1] in ["enter", "tab"]:
            self.focus = False
     
    def try_login(self, username, password):
        self.try_login_username = str(username)
        self.try_login_password = str(password)

        self.user, self.try_login_message = self.backend.firebase_login2(self.try_login_username, self.try_login_password)

        if self.user is not None:
            self.root.ids['login_screen'].ids['login_username'].text = ""
            self.root.ids['login_screen'].ids['login_password'].text = ""
            self.root.ids['login_screen'].ids['login_message'].text = ""

            #self.show_popup("Login Successful")
            self.loggedInUser2 = self.try_login_username
            #self.check_storage_notifications()
            #self.root.current = "machine_screen"
            self.on_enter_machineScreen()
            return True
        else:
            self.root.ids['login_screen'].ids['login_message'].text = self.try_login_message
            #self.root.ids['login_screen'].ids['login_username'].text = ""
            self.root.ids['login_screen'].ids['login_password'].text = ""
    
    def try_AddMachineScreen(self, username, password):
        self.try_login_username = str(username)
        self.try_login_password = str(password)

        self.user, self.try_login_message = self.backend.firebase_login(self.try_login_username, self.try_login_password)

        if self.user is not None:
            self.root.ids['add_machine_screen'].ids['AddMachineScreen_username'].text = ""
            self.root.ids['add_machine_screen'].ids['AddMachineScreen_password'].text = ""
            self.root.ids['add_machine_screen'].ids['AddMachineScreen_message'].text = ""

            print(" User: ", self.user)
            print(" Username: ", self.user["username"])

            self.machineName = self.user["username"]
            self.machineStatus = "Active"

            self.machineDetails = { "machineName" : self.machineName, "machineStatus" : self.machineStatus}

            self.backend.add_machine_details(self.loggedInUser2, self.machineName, self.machineDetails)

            #self.show_popup("Machine Added")
            self.on_MachineScreen_refresh_BTN()
            #self.loggedInUser = self.try_login_username
            self.root.current = "machine_screen"
            return True
        else:
            self.root.ids['add_machine_screen'].ids['AddMachineScreen_message'].text = self.try_login_message
            #self.root.ids['login_screen'].ids['login_username'].text = ""
            self.root.ids['add_machine_screen'].ids['AddMachineScreen_password'].text = ""
    
    def try_signup(self, username, password):
        self.try_signup_username = str(username)
        self.try_signup_password = str(password)

        self.user, self.try_signup_message = self.backend.firebase_signup2(self.try_signup_username, self.try_signup_password)

        if self.user is not None:
            self.root.ids['signup_screen'].ids['signup_username'].text = ""
            self.root.ids['signup_screen'].ids['signup_password'].text = ""
            self.root.ids['signup_screen'].ids['signup_message'].text = ""
            self.show_popup("Signup Successful")
            self.root.current = "startup_screen"
        else:
            self.root.ids['signup_screen'].ids['signup_message'].text = self.try_signup_message
    


#===============================================================#

# THE KIVY APP WILL START/RUN.        
MainApp().run()
