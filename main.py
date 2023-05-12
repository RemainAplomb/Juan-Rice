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
class MainApp(App):
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
        # Window.bind(on_resize=self.on_window_resize)
        pass

    def on_resize(self, *args):
        self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)
        #print(f"font_scaling: {self.font_scaling*24}")

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
