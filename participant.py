import sqlite3
from database import get_connection
from payments import make_payment
from tickets import generate_ticket, view_my_tickets


def register_for_event(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_id, name, date, time, venue, fee
        FROM events
        WHERE status = 'Upcoming'
    """)

    events = cursor.fetchall()

    if not events:
        print("\nNo upcoming events.")
        conn.close()
        return

    print("\n========== UPCOMING EVENTS ==========")

    for event in events:
        print(
            f"ID: {event[0]} | "
            f"{event[1]} | "
            f"{event[2]} | "
            f"{event[3]} | "
            f"₹{event[5]}"
        )

    try:
        event_id = int(input("\nEnter Event ID: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return

    cursor.execute("""
        SELECT *
        FROM registrations
        WHERE participant_id = ? AND event_id = ?
    """, (participant_id, event_id))

    existing = cursor.fetchone()

    if existing:
        print("You are already registered/interested in this event.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO registrations
        (participant_id, event_id, registration_status, registration_date)
        VALUES (?, ?, 'Interested', DATE('now'))
    """, (participant_id, event_id))

    conn.commit()

    print("\nSuccessfully registered as INTERESTED.")
    print("You can make the payment from the Participant Menu.")

    conn.close()


def add_comment(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_id, name
        FROM events
        WHERE status = 'Upcoming'
    """)

    events = cursor.fetchall()

    if not events:
        print("No events available.")
        conn.close()
        return

    print("\n========== EVENTS ==========")

    for event in events:
        print(f"{event[0]} - {event[1]}")

    try:
        event_id = int(input("Enter Event ID: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return

    comment = input("Write your comment/excitement: ")

    cursor.execute("""
        INSERT INTO comments
        (participant_id, event_id, comment)
        VALUES (?, ?, ?)
    """, (participant_id, event_id, comment))

    conn.commit()

    print("Comment added successfully!")

    conn.close()


def view_my_registrations(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.registration_id,
            e.name,
            e.date,
            e.time,
            e.venue,
            e.fee,
            r.registration_status
        FROM registrations r
        JOIN events e
            ON r.event_id = e.event_id
        WHERE r.participant_id = ?
    """, (participant_id,))

    registrations = cursor.fetchall()

    print("\n========== MY REGISTRATIONS ==========")

    if not registrations:
        print("No registrations found.")
    else:
        for r in registrations:
            print(f"""
Registration ID : {r[0]}
Event           : {r[1]}
Date            : {r[2]}
Time            : {r[3]}
Venue           : {r[4]}
Fee             : ₹{r[5]}
Status          : {r[6]}
----------------------------------------
""")

    conn.close()


def participant_menu(user_id, user_name):
    while True:

        print(f"""
========================================
       PARTICIPANT DASHBOARD
       Welcome, {user_name}
========================================

1. View Upcoming Events
2. Register for Event
3. Make Payment
4. Add Comment
5. View My Registrations
6. Generate Ticket
7. View My Tickets
8. Logout
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            from events import view_events
            view_events()

        elif choice == "2":
            register_for_event(user_id)

        elif choice == "3":
            make_payment(user_id)

        elif choice == "4":
            add_comment(user_id)

        elif choice == "5":
            view_my_registrations(user_id)

        elif choice == "6":
            view_my_registrations(user_id)

            try:
                registration_id = int(
                    input("Enter paid Registration ID for ticket: ")
                )
                generate_ticket(registration_id)

            except ValueError:
                print("Invalid ID.")

        elif choice == "7":
            view_my_tickets(user_id)

        elif choice == "8":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")