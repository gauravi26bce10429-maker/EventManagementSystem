import sqlite3
from database import get_connection
from events import add_event, view_events, view_event_details, cancel_event
from payments import view_all_payments


def view_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE status = 'Upcoming'
    """)
    upcoming_events = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role = 'participant'
    """)
    participants = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role = 'volunteer'
    """)
    volunteers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE payment_status = 'Successful'
    """)
    money_collected = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
    """)
    expenses = cursor.fetchone()[0]

    print("""
========================================
          ADMIN DASHBOARD
========================================
""")

    print(f"Total Events        : {total_events}")
    print(f"Upcoming Events     : {upcoming_events}")
    print(f"Participants        : {participants}")
    print(f"Volunteers          : {volunteers}")
    print(f"Money Collected     : ₹{money_collected}")
    print(f"Total Expenses      : ₹{expenses}")
    print(f"Remaining Balance   : ₹{money_collected - expenses}")

    print("========================================")

    conn.close()


def view_participants():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.registration_id,
            u.name,
            u.email,
            e.name,
            r.registration_status
        FROM registrations r
        JOIN users u
            ON r.participant_id = u.user_id
        JOIN events e
            ON r.event_id = e.event_id
    """)

    participants = cursor.fetchall()

    print("\n========== PARTICIPANTS ==========")

    if not participants:
        print("No participant registrations.")

    else:
        for p in participants:
            print(
                f"Registration ID: {p[0]} | "
                f"Name: {p[1]} | "
                f"Email: {p[2]} | "
                f"Event: {p[3]} | "
                f"Status: {p[4]}"
            )

    conn.close()


def add_expense():

    view_events()

    try:
        event_id = int(input("Enter Event ID: "))
        amount = float(input("Expense amount: "))
    except ValueError:
        print("Invalid input.")
        return

    description = input("Expense description: ")
    date = input("Expense date: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (event_id, description, amount, expense_date)
        VALUES (?, ?, ?, ?)
    """, (event_id, description, amount, date))

    conn.commit()
    conn.close()

    print("Expense added successfully!")


def view_expenses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ex.expense_id,
            e.name,
            ex.description,
            ex.amount,
            ex.expense_date
        FROM expenses ex
        JOIN events e
            ON ex.event_id = e.event_id
    """)

    expenses = cursor.fetchall()

    print("\n========== EVENT EXPENSES ==========")

    if not expenses:
        print("No expenses recorded.")

    else:
        for ex in expenses:
            print(
                f"ID: {ex[0]} | "
                f"Event: {ex[1]} | "
                f"Description: {ex[2]} | "
                f"Amount: ₹{ex[3]} | "
                f"Date: {ex[4]}"
            )

    conn.close()


def assign_volunteer():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, name, email
        FROM users
        WHERE role = 'volunteer'
    """)

    volunteers = cursor.fetchall()

    if not volunteers:
        print("No volunteers available.")
        conn.close()
        return

    print("\n========== VOLUNTEERS ==========")

    for v in volunteers:
        print(f"ID: {v[0]} | Name: {v[1]} | Email: {v[2]}")

    try:
        volunteer_id = int(input("Volunteer ID: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return

    view_events()

    try:
        event_id = int(input("Event ID: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return

    duty_date = input("Duty date: ")
    duty_time = input("Duty time: ")
    responsibility = input("Responsibility: ")

    cursor.execute("""
        INSERT INTO volunteer_schedule
        (volunteer_id, event_id, duty_date, duty_time, responsibility)
        VALUES (?, ?, ?, ?, ?)
    """, (
        volunteer_id,
        event_id,
        duty_date,
        duty_time,
        responsibility
    ))

    conn.commit()
    conn.close()

    print("Volunteer assigned successfully!")


def view_volunteers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.name,
            e.name,
            vs.duty_date,
            vs.duty_time,
            vs.responsibility
        FROM volunteer_schedule vs
        JOIN users u
            ON vs.volunteer_id = u.user_id
        JOIN events e
            ON vs.event_id = e.event_id
    """)

    schedules = cursor.fetchall()

    print("\n========== VOLUNTEER SCHEDULES ==========")

    if not schedules:
        print("No schedules available.")

    else:
        for s in schedules:
            print(f"""
Volunteer      : {s[0]}
Event          : {s[1]}
Duty Date      : {s[2]}
Duty Time      : {s[3]}
Responsibility : {s[4]}
------------------------------------------
""")

    conn.close()


def view_comments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.name,
            e.name,
            c.comment
        FROM comments c
        JOIN users u
            ON c.participant_id = u.user_id
        JOIN events e
            ON c.event_id = e.event_id
    """)

    comments = cursor.fetchall()

    print("\n========== PARTICIPANT COMMENTS ==========")

    if not comments:
        print("No comments yet.")

    else:
        for c in comments:
            print(f"""
Participant : {c[0]}
Event       : {c[1]}
Comment     : {c[2]}
--------------------------------------------
""")

    conn.close()


def admin_menu(user_name):

    while True:

        print(f"""
================================================
              ADMIN DASHBOARD
              Welcome, {user_name}
================================================

1. Dashboard Summary
2. Add New Event
3. View All Events
4. View Event Details
5. Cancel Event
6. View Participants
7. View All Payments
8. Add Event Expense
9. View Event Expenses
10. Assign Volunteer
11. View Volunteer Schedules
12. View Participant Comments
13. Logout
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_dashboard()

        elif choice == "2":
            add_event()

        elif choice == "3":
            view_events()

        elif choice == "4":
            view_events()

            try:
                event_id = int(input("Enter Event ID: "))
                view_event_details(event_id)
            except ValueError:
                print("Invalid ID.")

        elif choice == "5":
            cancel_event()

        elif choice == "6":
            view_participants()

        elif choice == "7":
            view_all_payments()

        elif choice == "8":
            add_expense()

        elif choice == "9":
            view_expenses()

        elif choice == "10":
            assign_volunteer()

        elif choice == "11":
            view_volunteers()

        elif choice == "12":
            view_comments()

        elif choice == "13":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")