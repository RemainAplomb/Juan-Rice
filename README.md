# General Info
## About  Us
    Developer:
        Dibansa, Rahmani
    Designer:
        Garcia, Bhee Jay 
    
    University:
        Cavite State University - Main Campus
    Course and Section:
        BSCpE 5-2
    
    Brief description of the program:
        This program is a monitoring system for a smart vending machine, developed for an undergraduate thesis.
        This repository will contain the software developed for monitoring the smart rice vending machine


# Installations
## Create conda environment
First, you will need to create the conda environment
for this project. This will also download and install
the necessary dependencies
```
conda env create -f environment.yml
```
Btw, you can also use requirements.txt if you want.
It also contains the information about the needed 
dependencies


## Check conda environment
Check whether you have created kivy_env
```
conda env list
```

## Activate conda environment
```
conda activate kivy_env
```

# Firebase
## Download JSON files
In your firebase realtime database, you need to 
download the json files related to the database
Example filenames:
    - google-services.json
    - juan-rice-firebase-adminsdk-lqyju-c65f392acb.json


## Edit rules of your Firebase realtime database
This rules are needed so that we can properly perform
queries related to our needs
```
{
  "rules": {
    ".read": "now < 1685980800000",  // 2023-6-6
    ".write": "now < 1685980800000",  // 2023-6-6
    
    "users": {
      ".indexOn": "username",
      "$user_id": {
        "transactions": {
          ".indexOn": "timestamp"
        }
      }
    },
    
    "users2": {
      ".indexOn": "username"
    }
  }
}
```


## Needed childrens in the database
So basically our database is like this
```
https://juan-rice-default-rtdb.firebaseio.com/
|
|---> users
|  |
|  |---> $user_id
|     |---> email: ""
|     |---> password: ""
|     |---> username: ""
|     |---> price
|     |  |---> premium : ""
|     |  |---> standard : ""
|     |  |---> cheap : ""
|     |
|     |---> storage
|     |  |---> misc
|     |  |  |---> cups : 0
|     |  |  |---> coin1 : 0
|     |  |  |---> coin2 : 0
|     |  |---> rice
|     |     |---> premium : 0
|     |     |---> standard : 0
|     |     |---> cheap : 0
|     |
|     |---> transactions
|        |---> $date
|           |---> $transaction_id
|              |---> amount: 0
|              |---> item_type: ""
|              |---> timestamp: 0
|              |---> transaction_type: ""
|
|
|---> users2
|     |---> email: ""
|     |---> password: ""
|     |---> username: ""
|     |---> machines
|        |---> misc
|           |---> $machine_id
|              |---> machineName: ""
|              |---> machineStatus: ""
|              |---> machineId: ""
```

# Edit in repository (If you have your own firebase realtime database)
## Edit in Backend_Functionalities.py
Edit your credential and databaseURL. Both are available in your firebase
realtime database
```
... code ommitted ...
class Backend_Functionalities:
    def __init__( self ):
        ... code ommitted ...
        self.cred = credentials.Certificate('juan-rice-firebase-adminsdk-lqyju-c65f392acb.json')
        self.firebase_app = firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://juan-rice-default-rtdb.firebaseio.com/'
        })
    ... code ommitted ...
... code ommitted ...
```
