import sqlite3
from database import get_connection


def add_event():
    print("\n========== ADD NEW EVENT ==========")

    name = input("Event name: ")
    description = input("Description: ")
    date = input("Date (DD-MM-YYYY): ")
    time = input("Time: ")
    venue = input("Venue: ")

    try:
        fee = float(input("Registration fee: "))
    except ValueError:
        print("Invalid fee.")
        return

    poster = input("Poster filename/link (optional): ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events
        (name, description, date, time, venue, fee, poster)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, date, time, venue, fee, poster))

    conn.commit()
    conn.close()

    print("\nEvent added successfully!")


def view_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_id, name, date, time, venue, fee, status
        FROM events
        ORDER BY event_id
    """)

    events = cursor.fetchall()
    conn.close()

    print("\n================ ALL EVENTS ================")

    if not events:
        print("No events available.")
        return

    for event in events:
        print(f"""
Event ID   : {event[0]}
Name       : {event[1]}
Date       : {event[2]}
Time       : {event[3]}
Venue      : {event[4]}
Fee        : ₹{event[5]}
Status     : {event[6]}
----------------------------------------------
""")


def view_event_details(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM events
        WHERE event_id = ?
    """, (event_id,))

    event = cursor.fetchone()

    if not event:
        print("Event not found.")
        conn.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM registrations
        WHERE event_id = ?
    """, (event_id,))

    participants = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM registrations
        WHERE event_id = ? AND registration_status = 'Paid'
    """, (event_id,))

    paid = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM volunteer_schedule
        WHERE event_id = ?
    """, (event_id,))

    volunteers = cursor.fetchone()[0]

    print("\n========== EVENT DETAILS ==========")
    print(f"Event ID       : {event[0]}")
    print(f"Name           : {event[1]}")
    print(f"Description    : {event[2]}")
    print(f"Date           : {event[3]}")
    print(f"Time           : {event[4]}")
    print(f"Venue          : {event[5]}")
    print(f"Fee            : ₹{event[6]}")
    print(f"Poster         : {event[7]}")
    print(f"Status         : {event[8]}")
    print(f"Participants   : {participants}")
    print(f"Paid           : {paid}")
    print(f"Volunteers     : {volunteers}")

    conn.close()


def cancel_event():
    view_events()

    try:
        event_id = int(input("Enter Event ID to cancel: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE events
        SET status = 'Cancelled'
        WHERE event_id = ?
    """, (event_id,))

    conn.commit()

    if cursor.rowcount == 0:
        print("Event not found.")
    else:
        print("Event cancelled successfully.")

    conn.close()