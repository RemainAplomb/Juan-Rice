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

from kivy.core.window import Window, Keyboard
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, CardTransition

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty

import kivy.utils
from kivy.utils import platform
from kivy.factory import Factory

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
        self.loggedInUser = "test_acc"

        # Get the current working directory
        self.current_directory = os.getcwd()

        # TRANSACTION RELATED
        self.transactions = None
        self.sell_transactions = None
        self.refill_transactions = None

        # INITIALIZE
        self.salesScreen_initialized = False
        self.salesStatsScreen_initialized = False
        self.riceStatusScreen_initialized = False

        self.figure = plt.figure()
        pass

    def on_resize(self, *args):
        try:
            self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)
        except ValueError:
            self.font_scaling = 1
        #print(f"font_scaling: {self.font_scaling*24}")
    
    def show_popup(self, message):
        popup = Popup(title=message,
                      title_size=self.font_scaling*14,
                      separator_height=0,
                      title_align="center",
                      size_hint=(None, None),
                      size=(self.font_scaling*280, self.font_scaling*100))
        popup.open()
    
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
            if self.transactions == None:
                self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
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
    
    def on_SalesScreen_refresh_BTN(self):
        self.refresh_this = self.root.ids['sales_screen'].ids['SalesScreen_timeSpinner'].text
        self.on_salesScreen_spinner_select(self.refresh_this)

    
    def populate_sales_scroll_view(self, transactions):
        if transactions == None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
            #self.transactions2 = self.backend.get_transactions_in_range(username="test_acc", start_date="2023-05-08", end_date="2023-05-08")
        else:
            self.transactions = transactions
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
            #remove_button.bind(on_release=self.remove_transaction)  # Add a method reference to handle the button click event
            # remove_button.bind(on_release=partial(self.remove_transaction, self.backend.convert_timestamp(transaction['timestamp'], "%y-%m-%d"), transaction_id=transaction["transaction_id"]))
            remove_button.bind(
                on_release=partial(
                    self.remove_transaction,
                    date=self.backend.convert_timestamp(transaction['timestamp'], "%Y-%m-%d"),
                    transaction_id=transaction["transaction_id"]
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

    def remove_transaction(self, button, date, transaction_id):
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
        # confirm_button = Button(text='Confirm', on_release=lambda button: self.confirm_remove_transaction(row_layout, date, transaction_id))
        # cancel_button = Button(text='Cancel', on_release=self.confirmation_popup.dismiss)

        # Create buttons for confirmation popup
        confirm_button = Button(text='Confirm', on_release=lambda button: self.confirm_remove_transaction(row_layout, date, transaction_id),
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

    def confirm_remove_transaction(self, row_layout, date, transaction_id):
        # Close the confirmation popup
        self.confirmation_popup.dismiss()

        remove_status = self.backend.remove_transaction(self.loggedInUser, date, transaction_id)
        if remove_status:
            # Get the reference to the scroll view
            scroll_view = self.root.ids['sales_screen'].ids["SalesScreen_salesScrollView"]

            # Remove the parent widget (row layout) from the scroll view
            scroll_view.remove_widget(row_layout)

    
    def on_enter_salesStatsScreen(self):
        if self.salesStatsScreen_initialized == False:
            self.root.ids['sales_stats_screen'].ids['SalesStatsScreen_timeSpinner'].text = "Latest"
            if self.loggedInUser == "":
                self.loggedInUser = "test_acc"
            if self.transactions == None:
                self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
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
        if transactions is None:
            self.transactions = self.backend.get_latest_transactions(self.loggedInUser)
        else:
            self.transactions = transactions

        self.sell_transactions, self.refill_transactions = self.backend.categorize_transactions(self.transactions)
        self.sales_by_product, self.sales_by_date, self.total_sales_by_date = self.backend.get_sales(self.sell_transactions)

        print("Sales by Product: ", self.sales_by_product)
        print("Sales by Date: ", self.sales_by_date)
        print("Total sales by Date: ", self.total_sales_by_date)
        print("Transactions: ", self.transactions)

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
            print(" Sorted Dates: ", sorted_dates)
            print(" Dates: ", dates)
            print(" Sales: ", sales)
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

        self.user, self.try_login_message = self.backend.firebase_login(self.try_login_username, self.try_login_password)

        if self.user is not None:
            self.root.ids['login_screen'].ids['login_username'].text = ""
            self.root.ids['login_screen'].ids['login_password'].text = ""
            self.root.ids['login_screen'].ids['login_message'].text = ""

            self.loggedInUser = self.try_login_username
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
