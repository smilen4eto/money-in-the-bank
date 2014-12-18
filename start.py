import sql_manager

import hashlib

import getpass


def main_menu():
    print("Welcome to our bank service. You are not logged in. \nPlease type register or login")

    while True:
        command = input("$$$>")

        if command == 'register':
            username = input("Enter your username: ")
            while 1:
                errors = []
                pas = getpass.getpass("Enter your password: ")
                if not any(x.isupper() for x in pas):
                    errors.append('Your password needs at least 1 capital letter.')
                if not any(x.islower() for x in pas):
                    errors.append('Your password needs at least 1 lower letter.')
                if not any(x.isdigit() for x in pas):
                    errors.append('Your password needs at least 1 digit.')
                if not len(pas) > 8:
                    errors.append('Your password is too short. Enter one with/more than 8 digits')
                if errors:
                    print("".join(errors))
                elif len(errors) == 0:
                    password = pas
                    break
            hexpass = hashlib.sha1()
            hexpass.update(password.encode())
            hexpassword = hexpass.hexdigest()
            #print(hexpassword)

            sql_manager.register(username, hexpassword)

            print("Registration Successfull")

        elif command == 'login':
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            hexpass = hashlib.sha1()
            hexpass.update(password.encode())
            hexpassword = hexpass.hexdigest()

            logged_user = sql_manager.login(username, hexpassword)

            if logged_user:
                logged_menu(logged_user)
            else:
                print("Login failed")

        elif command == 'help':
            print("login - for logging in!")
            print("register - for creating new account!")
            print("exit - for closing program!")

        elif command == 'exit':
            break
        else:
            print("Not a valid command")


def logged_menu(logged_user):
    print("Welcome you are logged in as: " + logged_user.get_username())
    while True:
        command = input("Logged>>")

        if command == 'info':
            print("You are: " + logged_user.get_username())
            print("Your id is: " + str(logged_user.get_id()))
            print("Your balance is:" + str(logged_user.get_balance()) + '$')

        elif command == 'changepass':
            new_pass = input("Enter your new password: ")
            sql_manager.change_pass(new_pass, logged_user)

        elif command == 'change-message':
            new_message = input("Enter your new message: ")
            sql_manager.change_message(new_message, logged_user)

        elif command == 'show-message':
            print(logged_user.get_message())

        elif command == 'help':
            print("info - for showing account info")
            print("changepass - for changing passowrd")
            print("change-message - for changing users message")
            print("show-message - for showing users message")

        elif command == 'signout':
            print("Goodbye!")
            break

def main():
    sql_manager.create_clients_table()
    main_menu()

if __name__ == '__main__':
    main()
