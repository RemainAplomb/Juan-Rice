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
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, CardTransition
from kivy.uix.dropdown import DropDown
from kivy.properties import BooleanProperty
from kivy.graphics import Color, RoundedRectangle
import kivy.utils
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.clock import Clock
from functools import partial
from kivy.uix.button import ButtonBehavior
from kivy.core.window import Window, Keyboard
from kivy.properties import NumericProperty
from kivy.uix.relativelayout import RelativeLayout

from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle
from kivy.utils import get_color_from_hex

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

from kivy.properties import ListProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label


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


class MainScreen( Screen ):
    pass

class StatusScreen( Screen ):
    pass

class SalesScreen( Screen ):
    pass

class SalesStatsScreen( Screen ):
    pass

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
        
        return Builder.load_file("main.kv") # BUILD THE KIVY APP
    
    def initialize_resources(self):
        self.loggedIn_user = "test_acc"

        # TRANSACTION RELATED
        self.transactions = None
        self.sell_transactions = None
        self.refill_transactions = None

        # INITIALIZE
        self.salesScreen_initialized = False
        self.salesStatsScreen_initialized = False
        self.statusScreen_initialized = False

        self.figure = plt.figure()
        pass

    def on_resize(self, *args):
        try:
            self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)
        except ValueError:
            self.font_scaling = 1
        #print(f"font_scaling: {self.font_scaling*24}")
    
    def on_enter_statusScreen(self, storage_type="rice"):
        self.max_storage = 20
        self.rice_storage = self.backend.retrieve_storage(self.loggedIn_user, storage_type)

        if self.rice_storage:
            for key, value in self.rice_storage.items():
                self.tempBar_value = (value / self.max_storage) * 100
                if self.tempBar_value >= 100 :
                    self.tempBar_value = 100
                self.root.ids['status_screen'].ids["StatusScreen_bar_" + key].value = self.tempBar_value
                self.root.ids['status_screen'].ids["StatusScreen_riceLabel_" + key].text = key.capitalize()
        self.root.transition.direction = "left"
        self.root.current = "status_screen"
    
    def on_enter_salesScreen(self):
        if self.salesScreen_initialized == False:
            self.root.ids['sales_screen'].ids['SalesScreen_timeSpinner'].text = "Latest"
            if self.loggedIn_user == "":
                self.loggedIn_user = "test_acc"
            if self.transactions == None:
                self.transactions = self.backend.get_latest_transactions(self.loggedIn_user)
                self.populate_sales_scroll_view(self.transactions)
            else:
                self.on_SalesScreen_refresh_BTN()
            self.salesScreen_initialized = True
        self.root.current = "sales_screen"
    
    def get_spinner_transactions(self, text):
        self.today = self.backend.get_current_date()
        self.current_date = self.today.strftime("%Y-%m-%d")
        self.week_earlier = (self.today - timedelta(days=7)).strftime("%Y-%m-%d")
        self.month_earlier = (self.today - timedelta(days=30)).strftime("%Y-%m-%d")

        if text == "1-day":
            self.transactions = self.backend.get_transactions_in_range(self.loggedIn_user, self.current_date, self.current_date)
        elif text == "1-week":
            self.transactions = self.backend.get_transactions_in_range(self.loggedIn_user, self.week_earlier, self.current_date)
        elif text == "1-month":
            self.transactions = self.backend.get_transactions_in_range(self.loggedIn_user, self.month_earlier, self.current_date)
        else:
            self.transactions = self.backend.get_latest_transactions(self.loggedIn_user)
        return self.transactions
    
    def on_salesScreen_spinner_select(self, text):
        self.transactions = self.get_spinner_transactions(text)
        self.populate_sales_scroll_view(self.transactions)
    
    def on_SalesScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['sales_screen'].ids['SalesScreen_timeSpinner'].text
        self.on_salesScreen_spinner_select(self.refresh_this)

    
    def populate_sales_scroll_view(self, transactions):
        if transactions == None:
            self.transactions = self.backend.get_latest_transactions(self.loggedIn_user)
            #self.transactions2 = self.backend.get_transactions_in_range(username="test_acc", start_date="2023-05-08", end_date="2023-05-08")
        else:
            self.transactions = transactions
        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        self.price_list = self.backend.get_pricelist(self.loggedIn_user)

        # Clear the scroll view
        self.scroll_view = self.root.ids['sales_screen'].ids["SalesScreen_salesScrollView"]
        self.scroll_view.clear_widgets()

        for transaction in self.sell_transactions:
            self.temp_itemType = transaction["item_type"]
            row_layout = GridLayout(cols=4, size_hint_y=None, height=self.font_scaling * 30)
            row_layout.bind(minimum_height=row_layout.setter('height'))
            # row_layout.canvas.before.add(Color(0, 1, 0, 1)) # green color
            # row_layout.canvas.before.add(Rectangle(pos=row_layout.pos, size=row_layout.size))

            time_label = Label(text=self.backend.convert_timestamp(transaction['timestamp'], "%m-%d %H:%M"), font_size=self.font_scaling*10)
            rice_type_label = Label(text=self.temp_itemType.capitalize(), font_size=self.font_scaling*12)

            weight_type_label = Label(text=str(transaction['amount']), font_size=self.font_scaling*12)
            total_type_label = Label(text=str(transaction['amount'] * self.price_list[self.temp_itemType]), font_size=self.font_scaling*12)

            row_layout.add_widget(time_label)
            row_layout.add_widget(rice_type_label)
            row_layout.add_widget(weight_type_label)
            row_layout.add_widget(total_type_label)

            self.root.ids['sales_screen'].ids["SalesScreen_salesScrollView"].add_widget(row_layout)
    
    def on_enter_salesStatsScreen(self):
        if self.salesStatsScreen_initialized == False:
            self.root.ids['sales_stats_screen'].ids['SalesStatsScreen_timeSpinner'].text = "Latest"
            if self.loggedIn_user == "":
                self.loggedIn_user = "test_acc"
            if self.transactions == None:
                self.transactions = self.backend.get_latest_transactions(self.loggedIn_user)
                self.populate_salesStats_scroll_view(self.transactions)
            else:
                self.on_SalesStatsScreen_refresh_BTN()
            self.salesStatsScreen_initialized = True
        self.root.current = "sales_stats_screen"
    
    def on_salesStatsScreen_spinner_select(self, text):
        self.transactions = self.get_spinner_transactions(text)
        self.populate_salesStats_scroll_view(self.transactions)
    
    def on_SalesStatsScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['sales_stats_screen'].ids['SalesStatsScreen_timeSpinner'].text
        self.on_salesStatsScreen_spinner_select(self.refresh_this)
    
    def populate_salesStats_scroll_view(self, transactions=None):
        # Get the data for the pie chart from your backend
        if transactions == None:
            self.transactions = self.backend.get_latest_transactions(self.loggedIn_user)
        else:
            self.transactions = transactions
        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        self.sales_by_product, self.sales_by_date, self.total_sales_by_date = self.backend.get_sales(self.sell_transactions)

        print(" Sales by Product: ", self.sales_by_product)
        print(" Sales by Date: ", self.sales_by_date)
        print(" Total sales by Date: ", self.total_sales_by_date)
        print(" Transactions: ", self.transactions)

        self.root.ids['sales_stats_screen'].ids["SalesStatsScreen_salesScrollView"].clear_widgets()
        if self.transactions != []:
            # PIE CHART
            # Create a matplotlib figure and add a pie chart
            fig, ax = plt.subplots()
            labels = [label.capitalize() for label in self.sales_by_product.keys()]
            values = self.sales_by_product.values()
            wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%.2f%%')
            for text in texts:
                text.set_fontsize(self.font_scaling*12)
            for autotext in autotexts:
                autotext.set_fontsize(self.font_scaling*12)
            ax.set_aspect('auto')
            ax.set_title('Sales Pie Chart', fontsize=self.font_scaling*18)

            # Calculate the size of the pie chart based on the screen size
            width, height = self.root.size
            dpi = fig.get_dpi()
            fig.set_size_inches(width/dpi, height/dpi)

            # Convert the matplotlib figure to a Kivy widget
            canvas = FigureCanvasKivyAgg(fig)

            # Update the chart layout with the new chart
            self.root.ids['sales_stats_screen'].ids["SalesStatsScreen_salesScrollView"].add_widget(canvas)
            # plt.clf()  # clear the plot

            # LINE CHART
            sorted_dates = sorted(self.total_sales_by_date.keys())
            dates = [datetime.datetime.strptime(date, '%y-%m-%d').date() for date in sorted_dates]
            sales = [self.total_sales_by_date[date] for date in sorted_dates]
            print(" Sorted Dates: ", sorted_dates)
            print(" Dates: ", dates)
            print(" Sales: ", sales)
            # Create a matplotlib figure and add a line chart
            fig, ax = plt.subplots()
            line = ax.plot_date(sorted_dates, sales, linestyle='-', marker='')
            for label in ax.xaxis.get_ticklabels():
                label.set_fontsize(self.font_scaling * 8)
            for label in ax.yaxis.get_ticklabels():
                label.set_fontsize(self.font_scaling * 8)

            # Customize the chart
            ax.set_title('Sales Trend', fontsize=self.font_scaling*18)
            ax.set_xlabel('Date', fontsize=self.font_scaling*12)
            ax.set_ylabel('Total Sales', fontsize=self.font_scaling*12)

            # Calculate the size of the pie chart based on the screen size
            width, height = self.root.size
            dpi = fig.get_dpi()
            print(" Root Size: ", self.root.size)
            print(" Dpi: ", dpi)
            print(" width/dpi: ", width/dpi)
            print(" width/dpi: ", round((width/dpi) * 0.8, 1))
            # print(" width/dpi * 8: ", width/dpi * 8)
            print(" height/dpi: ", height/dpi)
            print(" height/dpi: ", round((height/dpi) * 0.8, 1))
            # print(" height/dpi * 8: ", height/dpi *8)
            # fig.set_size_inches(width/(dpi*2), height/(dpi*2))
            # fig.set_figwidth(8)
            # fig.set_figheight(6)


            # Convert the matplotlib figure to a Kivy widget
            canvas = FigureCanvasKivyAgg(fig)

            # Update the chart layout with the new chart
            self.root.ids['sales_stats_screen'].ids["SalesStatsScreen_salesScrollView"].add_widget(canvas)

    def prevent_keypress(self, *args):
        keycode = args[1] if len(args) > 1 else None
        if isinstance(keycode, tuple) and keycode[1] in ["enter", "tab"]:
            self.focus = False
     
    def try_login(self, username, password):
        self.try_login_username = str(username)
        self.try_login_password = str(password)

        self.user, self.try_login_message = self.backend.firebase_login(self.try_login_username, self.try_login_password)

        if self.user is not None:
            self.root.ids['login_screen'].ids['login_username'].text = ""
            self.root.ids['login_screen'].ids['login_password'].text = ""
            self.root.ids['login_screen'].ids['login_message'].text = ""

            self.loggedIn_user = self.try_login_username
            self.root.current = "main_screen"
            return True
        else:
            self.root.ids['login_screen'].ids['login_message'].text = self.try_login_message
            #self.root.ids['login_screen'].ids['login_username'].text = ""
            self.root.ids['login_screen'].ids['login_password'].text = ""
    
    def try_signup(self, username, password):
        self.try_signup_username = str(username)
        self.try_signup_password = str(password)

        self.user, self.try_signup_message = self.backend.firebase_signup(self.try_signup_username, self.try_signup_password)

        if self.user is not None:
            self.root.ids['signup_screen'].ids['signup_username'].text = ""
            self.root.ids['signup_screen'].ids['signup_password'].text = ""
            self.root.ids['signup_screen'].ids['signup_message'].text = ""
            self.root.current = "startup_screen"
        else:
            self.root.ids['signup_screen'].ids['signup_message'].text = self.try_signup_message
    


#===============================================================#

# THE KIVY APP WILL START/RUN.        
MainApp().run()
