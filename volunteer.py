import sqlite3
from database import get_connection


def view_volunteer_schedule(volunteer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            e.name,
            e.date,
            e.time,
            e.venue,
            vs.duty_date,
            vs.duty_time,
            vs.responsibility
        FROM volunteer_schedule vs
        JOIN events e
            ON vs.event_id = e.event_id
        WHERE vs.volunteer_id = ?
    """, (volunteer_id,))

    schedules = cursor.fetchall()

    print("\n========== MY VOLUNTEER SCHEDULE ==========")

    if not schedules:
        print("No schedule assigned yet.")
    else:
        for s in schedules:
            print(f"""
Event          : {s[0]}
Event Date     : {s[1]}
Event Time     : {s[2]}
Venue          : {s[3]}
Duty Date      : {s[4]}
Duty Time      : {s[5]}
Responsibility : {s[6]}
---------------------------------------------
""")

    conn.close()


def volunteer_menu(user_id, user_name):

    while True:

        print(f"""
========================================
        VOLUNTEER DASHBOARD
        Welcome, {user_name}
========================================

1. View My Schedule
2. View Upcoming Events
3. Logout
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_volunteer_schedule(user_id)

        elif choice == "2":
            from events import view_events
            view_events()

        elif choice == "3":
            print("Logging out...")
            break

        else:
            print("Invalid choice.")