import dbi as db
import getpass as gp

# Asking user to input username and password
username = input("Please enter your username: ")
password = gp.getpass("Please enter your password: ")
# Returning the outputs of attempt_login function and passing params
login_success, user_id = db.attempt_login(username, password)
# If the output of this function is true
if(login_success == True):
    # Giving access to the 4 options below
    print("Authentication success!")
# Options going in loop after user selects any option
options = True
while options:
    # Printing all available options
    print("Please select from the following options:")
    print("Option 1. Add new exploit")
    print("Option 2. Check all your exploits")
    print("Option 3. Check other users exploits ")
    print("Option 4. Leave this application")
# Assigning a variable to user's input and making it integer only
    user_selection = input()
    user_selection = int(user_selection)
# User's choice based on the input
    if user_selection == 1:
        exploit_input = input("Add new exploit: ")
        # Calling functions for every user_selection from dbi file and passing params except for the 4th option exit()
        db.add_exploit(exploit_input, user_id)
        print("Your exploit has been added")
    elif user_selection == 2:
        db.list_your_exploits(user_id)
    elif user_selection == 3:
        db.list_other_exploits(user_id)
    elif user_selection == 4:
        exit()
# This will be printed if the user wants to input anything different from 1-4
    else:
        print("Invalid entry")

# This message will be printed if the user doesn't exist in the system
else:
    print("Sorry, authentication failure")
    exit()
