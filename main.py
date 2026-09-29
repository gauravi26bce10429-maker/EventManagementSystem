from database import create_tables, login, register_user
from admin import admin_menu
from participant import participant_menu
from volunteer import volunteer_menu


def register():

    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Create password: ")

    print("\nChoose account type:")
    print("1. Participant")
    print("2. Volunteer")

    role_choice = input("Enter choice: ")

    if role_choice == "1":
        role = "participant"

    elif role_choice == "2":
        role = "volunteer"

    else:
        print("Invalid choice.")
        return

    success = register_user(name, email, password, role)

    if success:
        print("\nAccount created successfully!")
    else:
        print("\nThis email is already registered.")


def login_user():

    print("\n========== LOGIN ==========")

    email = input("Email: ")
    password = input("Password: ")

    user = login(email, password)

    if not user:
        print("\nInvalid email or password.")
        return

    user_id, name, email, role = user

    print(f"\nWelcome, {name}!")

    if role == "admin":
        admin_menu(name)

    elif role == "participant":
        participant_menu(user_id, name)

    elif role == "volunteer":
        volunteer_menu(user_id, name)


def main():

    create_tables()

    while True:

        print("""
==================================================
       EVENT MANAGEMENT SYSTEM
==================================================

1. Login
2. Create Participant/Volunteer Account
3. Exit
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            login_user()

        elif choice == "2":
            register()

        elif choice == "3":
            print("\nThank you for using Event Management System!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()