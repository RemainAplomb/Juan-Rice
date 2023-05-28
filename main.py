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



#========== IMPORTING NECESSARY PYTHON MODULES ==========#
"""
    The modules below are built-in Python modules.
    There's no need to install these.
"""
import random  # Module for generating random numbers
import sys  # Module for system-specific parameters and functions
import os  # Module for interacting with the operating system
import csv  # Module for reading and writing CSV files
import ast  # Module for evaluating strings as Python expressions
from datetime import datetime  # Module for working with dates and times

import hashlib  # Module for hashing functions



#==========  IMPORTING NECESSARY KIVY MODULES  ==========#
"""
    These modules are from Kivy. The modules can be acquired
    by creating a conda environment using the environment.yml
    or requirements.txt that we have provided in the repository.
"""
from kivy.app import App  # Base class for creating Kivy applications
from kivy.lang import Builder  # Module for creating Kivy GUI using a language similar to JSON or CSS
from kivy.clock import Clock  # Module for scheduling functions to be called at a later time

from kivy.core.window import Window, Keyboard  # Module for window management and keyboard events
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, CardTransition  # Module for managing multiple screens in Kivy

from kivy.uix.relativelayout import RelativeLayout  # Layout that arranges children relative to its own position and size
from kivy.uix.gridlayout import GridLayout  # Layout that arranges children in a grid-like structure
from kivy.uix.boxlayout import BoxLayout  # Layout that arranges children in a horizontal or vertical box
from kivy.uix.floatlayout import FloatLayout  # Layout that allows specifying the position and size of children using floating point values

from kivy.properties import ListProperty  # Property that allows a list value
from kivy.properties import BooleanProperty  # Property that allows a boolean value
from kivy.properties import NumericProperty  # Property that allows a numeric value

import kivy.utils  # Module for various utility functions in Kivy
from kivy.utils import platform  # Function for getting the current platform (e.g., 'android', 'ios', 'win', 'linux')

from kivy.uix.scrollview import ScrollView  # Scrollable view that contains a single child
from kivy.uix.popup import Popup  # Modal dialog box that appears on top of the current screen
from kivy.uix.label import Label  # Widget for displaying text


from kivy.uix.behaviors import ButtonBehavior # For button behaviour
from kivy.uix.image import Image  # Widget for displaying images
from kivy.graphics import Rectangle, Color, RoundedRectangle  # Graphics instructions for drawing shapes
from kivy.utils import get_color_from_hex  # Function for getting a color value from a hexadecimal string

from kivy.uix.widget import Widget  # Base class for creating widgets
from kivy.uix.dropdown import DropDown  # Widget for creating a drop-down menu
from kivy.uix.button import Button  # Widget for displaying a button

from kivy.clock import Clock  # Module for scheduling functions to be called at a later time
from functools import partial  # Function for creating a new function with partially defined arguments

from kivymd.app import MDApp  # Base class for creating Material Design applications



#==========  IMPORTING NECESSARY MATPLOTLIB MODULES  ==========#
"""
    These matplotlib modules are used to display graphs
"""
# Chart
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas, NavigationToolbar2Kivy, FigureCanvasKivyAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



#==========  IMPORTING NECESSARY PYTHON FILES  ==========#
"""
    These python files are imported from the repository.
    Examples of which:
        Backend_Functionalities.py
"""
from Backend_Functionalities import * # This contains the backend functions that we will need


#==========          GLOBAL VARIABLES          ==========#
"""
    These are the global variables that will be used by the
    program.
"""
WINDOW_MIN_WIDTH = 360 # For setting the window's minimum width
WINDOW_MIN_HEIGHT = 640 # For setting the window's minimum height

#===========================================================================================================#



#========== CLASSES FOR THE PROGRAM'S SCREENS/WINDOWS ==========#
"""
    Each of these classes represents a screen that can be seen in
    the actual application. These objects are references used by 
    the main.kv and some of its subsidiary .kv files.

    The screens are as follows:
        StartUpScreen: The very first screen that will welcome the 
            user when the app runs.
        LogInScreen: The screen that facilitates the user's log in.
        SignUpScreen: The screen that facilitates the user's sign up.
        MachineScreen: The main screen that displays information and 
            controls related to the machines that are binded to the 
            user's monitoring account.
        AddMachineScreen: The screen for adding a new vending machine 
            to the system.
        MainScreen: The main screen of the application after the user 
            logs in.
        RiceStatusScreen: The screen that displays the status and 
            information of the rice in the vending machine.
        MiscStatusScreen: The screen that displays the status and 
            information of miscellaneous items in the vending machine.
        SalesScreen: The screen that displays the sales information 
            and transaction logs of the vending machine.
        SalesStatsScreen: The screen that displays statistics and 
            charts related to the sales of the vending machine.
        RefillScreen: The screen for refilling the inventory of the 
            vending machine.
        RefillHistoryScreen: The screen that displays the refill 
            history and logs of the vending machine.
        RefillStatsScreen: The screen that displays statistics and 
            charts related to the refill activities of the vending 
            machine.
        NotificationScreen: The screen that displays notifications 
            and alerts related to the vending machine.
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



#========== CLASSES FOR THE PROGRAM'S KIVY-RELATED ASSET CLASS ==========#
"""
    These classes are kivy-related and are used as assets by
    the front-end.

    The classes are as follows:
        ImageButton: This class inherits the button behavior and
            image module from Kivy. It allows our program to have
            image buttons with custom functionality.
        VerticalBar: This class is used to display vertical bars
            in the status-related screens (rice and misc). It
            provides a visual representation of a value compared
            to a maximum value.
"""
class ImageButton(ButtonBehavior, Image):
    pass

class VerticalBar(Widget):
    value = NumericProperty(0)
    value_normalized = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])
    max = NumericProperty(100)

    def on_value(self, instance, value):
        self.value_normalized = value / self.max if self.max else 0
#===========================================================================================================#



#==========               THE APP CLASS               ==========#
"""
 The class 'MainApp' is the core of the entire program.
 This class contains most of the methods necessary to run this
 program.

 The methods contained within this class are as follows:
   build: The method that builds the Kivy-dependent program.

   (As for other functions, I decided to put the documentation
   for it directly. So just read along. Thank you.)
"""
class MainApp(MDApp):
    # APP VARIABLES
    username = "" 
    password = ""

    font_scaling = NumericProperty()

    def build(self):
        """
        Method that builds the Kivy-dependent program.

        Returns:
            Builder: The built Kivy app.
        """
        # Initialize resources and backend functions
        self.initialize_resources()
        self.backend = Backend_Functionalities() 

        # Set the initial window size
        Window.size = (
			(WINDOW_MIN_WIDTH if Window.width > WINDOW_MIN_WIDTH else Window.width), 
			(WINDOW_MIN_HEIGHT if Window.height > WINDOW_MIN_HEIGHT else Window.height))
        self.on_resize()
        Window.bind(size=self.on_resize)

        # Schedule the function to be called every 5 minutes
        Clock.schedule_interval(self.run_update_5mins, 3600)
        Clock.schedule_interval(self.run_update_1hour, 3600)  # 3600 seconds = 1 hour
        
        return Builder.load_file("main.kv") # BUILD THE KIVY APP
    
    def initialize_resources(self):
        """
        Initialize resources required by the app.
        """
        # Get the current working directory
        self.current_directory = os.getcwd()

        # Clear flags
        self.clear_flags(True)
    

    def clear_flags(self, clear_user=False):
        """
        Clear flags and variables used by the app.

        Args:
            clear_user (bool, optional): Whether to clear user-related flags and variables. Defaults to False.
        """
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
        """
        Method that is called every 5 minutes to perform updates.

        Args:
            dt (float): Time elapsed since the last call.
        """
        if self.loggedInUser == None:
            return
        self.clear_flags()
    
    def run_update_1hour(self, dt):
        """
        Method that is called every hour to perform updates.

        Args:
            dt (float): Time elapsed since the last call.
        """
        if self.loggedInUser == None:
            return
        self.check_storage_notifications()
    
    def check_storage_notifications(self):
        """
        Method to check storage notifications and push them to the app.

        This method retrieves storage notifications from the backend and pushes them to the app for display.
        """
        notification_data = self.backend.check_storage_notification(self.loggedInUser)
        for data in notification_data:
            self.backend.push_notifications(data["notif_title"], data["notif_message"])


    def on_resize(self, *args):
        """
        Method that is called when the window is resized.

        Args:
            *args: Variable length argument list.
        """
        try:
            self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)
        except ValueError:
            self.font_scaling = 1
    
    def show_popup(self, notif_title, notif_message=None):
        """
        Method to show a popup with a notification message.

        Args:
            notif_title (str): The title of the notification.
            notif_message (str, optional): The message of the notification. Defaults to None.
        """
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
        """
        Method called when entering the machine screen.

        If the screen is not initialized, it performs necessary initializations.
        """
        if self.machineScreen_initialized == False:
            if self.loggedInUser2 == "":
                self.loggedInUser2 = "y"
            self.on_MachineScreen_refresh_BTN()
            self.machineScreen_initialized = True
        self.root.current = "machine_screen"
    
    def on_enter_addMachineScreen(self):
        """
        Method called when entering the add machine screen.
        """
        self.root.current = "add_machine_screen"
    
    def on_enter_riceStatusScreen(self, storage_type="rice"):
        """
        Method called when entering the rice status screen.

        Args:
            storage_type (str, optional): The type of storage. Defaults to "rice".
        """
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
        """
        Method called when entering the miscellaneous status screen.

        Args:
            storage_type (str, optional): The type of storage. Defaults to "misc".
        """
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
        """
        Method called when entering the sales screen.

        If the screen is not initialized, it performs necessary initializations.
        """
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
        """
        Method called when entering the refill screen.

        If the screen is not initialized, it performs necessary initializations.
        """
        if self.refillScreen_initialized == False:
            self.root.ids['refill_screen'].ids['RefillScreen_amountInput'].text = ""
            self.root.ids['refill_screen'].ids['RefillScreen_storageTimeSpinner'].text = "Rice"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text = "Premium"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].values = ["Premium", "Standard", "Cheap"]
            self.refillScreen_initialized = True
        self.root.current = "refill_screen"
    
    def on_enter_refillHistoryScreen(self):
        """
        This method is called when entering the "refill_history_screen" screen. It initializes the screen, 
        retrieves the latest transactions for the logged-in user, and populates the UI
        """
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
        """
        This method is called when entering the "notification_screen" screen. 
        It retrieves notification data and populates the UI.

        notification_data = [
            {"notif_title": "Premium Rice", "notif_message": "N kg left in storage.", "image_src" : "resources/buttons/rice_alert_premium.png"},
            # Add more notification data as needed
        ]
        """
        notification_data = self.backend.check_storage_notification(self.loggedInUser)
        self.populate_notification_scroll_view(notification_data)
        self.root.current = "notification_screen"
    
    def get_spinner_transactions(self, text):
        """
        This method retrieves transactions based on the selected time period (text) and returns the transactions.
        """
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
        """
        This method is called when selecting an option in the spinner on the "sales_screen" screen. 
        It retrieves the transactions based on the selected time period and updates the UI.
        """
        self.transactions = self.get_spinner_transactions(text)
        self.populate_sales_scroll_view(self.transactions)
    
    def on_refillScreen_spinner_select(self, text, spinner_type="storage"):
        """
        This method is called when selecting an option in the spinner on the "refill_screen" screen. 
        It updates the available options in the item spinner based on the selected storage type.
        """
        if text.lower() == "rice":
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text = "Premium"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].values = ["Premium", "Standard", "Cheap"]
        if text.lower() == "misc":
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text = "Cups"
            self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].values = ["Cups", "Coin1", "Coin2"]
    
    def on_refillHistoryScreen_spinner_select(self, text):
        """
        This method is called when selecting an option in the spinner on the "refill_history_screen" screen. 
        It retrieves the transactions based on the selected time period and updates the UI.
        """
        self.transactions = self.get_spinner_transactions(text)
        self.populate_refill_history_scroll_view(self.transactions)
    
    def on_RefillScreen_add_BTN(self):
        """
        This method is called when the "add" button is clicked on the "refill_screen" screen. 
        It retrieves the selected storage type, item type, and refill amount, and adds a refill transaction.
        """
        self.storage_type = self.root.ids['refill_screen'].ids['RefillScreen_storageTimeSpinner'].text
        self.item_type = self.root.ids['refill_screen'].ids['RefillScreen_itemTimeSpinner'].text
        try:
            self.refill_amount = float(self.root.ids['refill_screen'].ids['RefillScreen_amountInput'].text)
            self.refill_status, self.refill_message = self.backend.add_transaction(self.loggedInUser, "refill", f"{self.storage_type.lower()}-{self.item_type.lower()}", self.refill_amount)
            self.show_popup(self.refill_message)
        except:
            self.show_popup("Invalid Amount Input")

    def on_MachineScreen_refresh_BTN(self):
        """
        This method is called when the "refresh" button is clicked on the "machine_screen" screen. 
        It retrieves the user's machines and updates the UI.
        """
        self.machines = self.backend.get_user_machines(self.loggedInUser2)
        #print("Self Machines", self.machines)
        self.populate_machine_scroll_view(self.machines)
        

    def on_SalesScreen_refresh_BTN(self):
        """
        This method is called when the "refresh" button is clicked on the "sales_screen" screen. 
        It retrieves the selected time period and updates the UI with the corresponding transactions.
        """
        self.refresh_this = self.root.ids['sales_screen'].ids['SalesScreen_timeSpinner'].text
        self.on_salesScreen_spinner_select(self.refresh_this)
    
    def on_RefillHistoryScreen_refresh_BTN(self):
        """
        This method is called when the "refresh" button is clicked on the "refill_history_screen" screen. 
        It retrieves the selected time period and updates the UI with the corresponding transactions.
        """
        self.refresh_this = self.root.ids['refill_history_screen'].ids['RefillHistoryScreen_timeSpinner'].text
        self.on_refillHistoryScreen_spinner_select(self.refresh_this)
    
    def on_NotificationScreen_card_BTN(self, button, notif_title, notif_message):
        """
        This is for showing the details of the notifications present in the
        notification screen.
        """
        self.show_popup(notif_title, notif_message)
    
    def populate_machine_scroll_view(self, machines):
        """
        This method populates the machine scroll view on the machine screen with the provided 
        machine data. It first checks if the machines variable is None and retrieves the user's 
        machines if necessary. Then, it clears the scroll view and iterates over each machine 
        to create a row layout containing the machine name, remove button, and login button. 
        The size hints are set to control the column widths, and the row layout is added to the 
        scroll view.
        """
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
        """
        This method is called when the "Log in" button is clicked for a specific machine on the 
        machine screen. It creates a confirmation popup asking the user if they want to access 
        the selected machine. The method initializes the confirmation popup with the appropriate 
        title, content, and buttons for confirmation and cancellation. If the user confirms the 
        login, the method confirm_loginMachine(machineName) is called.
        """
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
        """
        This method is called when the user confirms the login to a machine in the confirmation popup. 
        It sets the loggedInUser variable to the selected machine name, clears any flags, checks for 
        storage notifications, dismisses the confirmation popup, and switches the root to the main screen.
        """
        self.loggedInUser = machineName
        self.clear_flags()
        self.check_storage_notifications()
        self.confirmation_popup.dismiss()
        self.root.current = "main_screen"
    

    def on_MachineScreen_remove_BTN(self, button, machineName):
        """
        This method is called when the "Remove" button is clicked for a specific machine on the machine 
        screen. It creates a confirmation popup asking the user if they want to unbind the selected 
        machine. The method initializes the confirmation popup with the appropriate title, content, and 
        buttons for confirmation and cancellation. If the user confirms the removal, the method 
        confirm_removeMachine(machineName) is called.
        """
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
        """
        This method is called when the user confirms the removal of a machine in the confirmation popup. 
        It dismisses the confirmation popup, calls the backend method to remove the machine, refreshes 
        the machine screen, and updates the notification screen if needed.
        """
        self.confirmation_popup.dismiss()
        self.backend.remove_machine(self.loggedInUser2, machineName)
        self.on_MachineScreen_refresh_BTN()


    def populate_notification_scroll_view(self, notification_data):
        """
        This method populates the notification scroll view on the notification screen with the provided 
        notification data. It clears the scroll view and iterates over each notification data item to 
        create a row layout containing an image button representing the notification. The image source, 
        on-release action, and other properties are set accordingly. The row layout is then added to the 
        scroll view.
        """
        notification_scrollview = self.root.ids['notification_screen'].ids['NotificationScreen_notificationScrollView']
        notification_scrollview.clear_widgets()

        for data in notification_data:
            row_layout = GridLayout(cols=1)
            notif_title = str(data["notif_title"])
            notif_message = str(data["notif_message"])
            notification_card = ImageButton(source=data["image_src"], allow_stretch=True, keep_ratio=False, on_release=partial(self.on_NotificationScreen_card_BTN, notif_title=notif_title, notif_message=notif_message))

            row_layout.add_widget(notification_card)
            notification_scrollview.add_widget(row_layout)

    
    def populate_sales_scroll_view(self, transactions):
        """
        This method populates the sales scroll view on the sales screen with the provided transaction data. 
        If no transactions are provided, it retrieves the latest transactions for the logged-in user from 
        the backend. It categorizes the transactions into sell and refill transactions, retrieves the price 
        list from the backend, and clears the scroll view. Then, for each sell transaction, it creates a row 
        layout containing labels for the transaction details (time, rice type, weight, total) and a remove 
        button. The row layout is added to the scroll view, and the size hint properties of the widgets are 
        set to control column widths.
        """
        if transactions == None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
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
        """
        This method populates the refill history scroll view on the refill history screen with the provided 
        transaction data. If no transactions are provided, it retrieves the latest transactions for the 
        logged-in user from the backend. It categorizes the transactions into sell and refill transactions 
        and clears the scroll view. Then, for each refill transaction, it creates a row layout containing 
        labels for the transaction details (time, item type, amount) and a remove button. The row layout is 
        added to the scroll view, and the size hint properties of the widgets are set to control column 
        widths.
        """
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
            row_layout.add_widget(remove_button)  # Add the remove button to the row

            # Set the size_hint property of each widget to control column widths
            time_label.size_hint_x = 0.3  # 20% of the row width
            item_type_label.size_hint_x = 0.25  # 25% of the row width
            amount_type_label.size_hint_x = 0.25  # 25% of the row width
            remove_button.size_hint_x = 0.2  # 20% of the row width

            self.root.ids['refill_history_screen'].ids["RefillHistoryScreen_refillHistoryScrollView"].add_widget(row_layout)

    def remove_transaction(self, button, date, transaction_id, transaction_type="sell"):
        """
        This method is called when the user clicks the "Remove" button for a specific transaction. 
        It retrieves the date, transaction ID, and transaction type (defaulted to "sell") from the 
        button and calls the backend method to remove the transaction. The method then refreshes the 
        respective screen (sales screen or refill history screen) by calling the appropriate 
        method (populate_sales_scroll_view or populate_refill_history_scroll_view).
        """
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
        """
        This method is responsible for confirming the removal of a transaction. It takes the row_layout 
        (widget representing the transaction row), date, transaction_id, and an optional transaction_type 
        parameter (defaults to "sell"). It removes the transaction from the backend and updates the UI 
        accordingly.
        """
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
        """
        This method is triggered when entering the "salesStatsScreen" screen. It initializes the screen if it 
        hasn't been initialized before. It sets the default value for the time spinner, retrieves the latest 
        transactions if they are not already loaded, and populates the sales stats scroll view.
        """
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
        """
        This method is triggered when entering the "refillStatsScreen" screen. It initializes the screen if 
        it hasn't been initialized before. It sets the default value for the time spinner, retrieves the 
        latest transactions if they are not already loaded, and populates the refill stats scroll view.
        """
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
        """
        This method is triggered when selecting an option from the time spinner on the salesStatsScreen. 
        It retrieves the transactions based on the selected time period and populates the sales stats 
        scroll view.
        """
        self.transactions = self.get_spinner_transactions(text)
        self.populate_salesStats_scroll_view(self.transactions)
    
    def on_refillStatsScreen_spinner_select(self, text):
        """
        This method is triggered when selecting an option from the time spinner on the refillStatsScreen. 
        It retrieves the transactions based on the selected time period and populates the refill stats 
        scroll view.
        """
        self.transactions = self.get_spinner_transactions(text)
        self.populate_refillStats_scroll_view(self.transactions)
    
    def on_SalesStatsScreen_refresh_BTN(self):
        """
        This method is triggered when the refresh button is clicked on the salesStatsScreen. It gets the 
        selected time period from the time spinner and updates the sales stats based on that period.
        """
        self.refresh_this = self.root.ids['sales_stats_screen'].ids['SalesStatsScreen_timeSpinner'].text
        self.on_salesStatsScreen_spinner_select(self.refresh_this)
    
    def on_RefillStatsScreen_refresh_BTN(self):
        """
        This method is triggered when the refresh button is clicked on the refillStatsScreen. It gets the 
        selected time period from the time spinner and updates the refill stats based on that period.
        """
        self.refresh_this = self.root.ids['refill_stats_screen'].ids['RefillStatsScreen_timeSpinner'].text
        self.on_refillStatsScreen_spinner_select(self.refresh_this)
    
    def populate_salesStats_scroll_view(self, transactions=None):
        """
        This method populates the sales stats scroll view with transaction data. If no transactions are 
        provided, it retrieves the latest transactions. It categorizes the transactions into sell and 
        refill transactions, calculates sales by product, sales by date, and total sales by date. It then 
        generates and displays pie charts, bar charts, and line charts based on the calculated data.
        """
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
        """
        Populates the refill stats scroll view with transaction data.

        Args:
            transactions (list, optional): List of transactions to populate the scroll view with.
                If not provided, the latest transactions for the logged-in user will be retrieved.
                Defaults to None.
        """
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
        """
        This method is called when the export button is clicked on the Sales Stats screen.
        It saves the sales transaction data to a CSV file and saves the generated graphs as PNG files.
        The CSV file includes the field names from the sell transactions and the data for each transaction.
        The graphs include a pie chart, a bar chart, a line chart for total sales by date, and multiple line 
        charts for sales by rice type. After saving the data and graphs, a popup message is displayed to 
        indicate the successful saving of the graphs.
        """
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
            self.show_popup("Graphs saved successfully!")
    

    def on_RefillStatsScreen_export_BTN(self):
        """
        This method is called when the export button is clicked on the Refill Stats screen.
        It saves the refill transaction data to a CSV file and saves the generated graphs as PNG files.
        The CSV file includes the field names from the refill transactions and the data for each transaction.
        The graphs include a pie chart, a bar chart, a line chart for total refill by date, and multiple 
        line charts for refill by item type. After saving the data and graphs, a popup message is displayed 
        to indicate the successful saving of the graphs.
        """
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
            self.show_popup("Graphs saved successfully!")
    

    def on_MainScreen_signout_BTN(self):
        """
        This method is called when the signout button is clicked on the Main screen.
        It clears any flags or session-related data, displays a popup message indicating successful 
        logout, and transitions the screen back to the startup screen.
        """
        self.clear_flags(True)
        self.show_popup("Succesfully logged out")
        self.root.current = "startup_screen"
        self.root.transition.direction = "right"


    def save_figure(self, fig, save_path):
        """
        This method is used to save a matplotlib figure (fig) to the specified path (save_path) as a 
        PNG image. It uses the savefig function from the matplotlib.pyplot module to save the figure.
        After saving the figure, it closes the figure to release resources.
        """
        # Save the figure to the specified path
        fig.savefig(save_path)
        plt.close(fig)


    def prevent_keypress(self, *args):
        """
        This method is an event handler that prevents certain keypress events from being processed.
        It checks if the pressed key is "enter" or "tab" and sets the focus attribute to False.
        The purpose of this method is to prevent specific keypress events from triggering actions or 
        changing the focus.
        """
        keycode = args[1] if len(args) > 1 else None
        if isinstance(keycode, tuple) and keycode[1] in ["enter", "tab"]:
            self.focus = False
     
    def try_login(self, username, password):
        """
        This method attempts to log in the user with the provided username and password.
        It calls the firebase_login2 method from the backend object, passing the username and password.
        If the login is successful, it clears the login fields and message, sets the logged-in user, 
        and transitions to the "machine_screen". If the login fails, it displays the login error message 
        and clears the password field.
        """
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
        """
        This method is similar to try_login, but it is used specifically for adding a machine.
        It attempts to log in the user with the provided username and password using the firebase_login 
        method from the backend object. If the login is successful, it clears the login fields and message, 
        retrieves the machine name from the logged-in user data, sets the machine status, and adds the 
        machine details using the add_machine_details method from the backend object. After adding the 
        machine details, it refreshes the machine screen and transitions to the "machine_screen".
        If the login fails, it displays the login error message and clears the password field.
        """
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
        """
        This method attempts to sign up the user with the provided username and password.
        It calls the firebase_signup2 method from the backend object, passing the username and password.
        If the signup is successful, it clears the signup fields and message, displays a popup message 
        indicating successful signup, and transitions to the "startup_screen". If the signup fails, 
        it displays the signup error message.
        """
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
