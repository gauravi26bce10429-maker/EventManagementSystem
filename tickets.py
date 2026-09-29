import sqlite3
import random
import string
from database import get_connection


def generate_ticket_code():
    return "EVT-" + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )


def generate_ticket(registration_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticket_id
        FROM tickets
        WHERE registration_id = ?
    """, (registration_id,))

    existing = cursor.fetchone()

    if existing:
        print("Ticket already exists.")
        conn.close()
        return

    ticket_code = generate_ticket_code()

    cursor.execute("""
        INSERT INTO tickets
        (registration_id, ticket_code)
        VALUES (?, ?)
    """, (registration_id, ticket_code))

    conn.commit()

    print("\n========== TICKET ==========")
    print(f"Registration ID : {registration_id}")
    print(f"Ticket Code     : {ticket_code}")
    print("============================")

    conn.close()


def view_my_tickets(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.ticket_code,
            e.name,
            e.date,
            e.time,
            e.venue
        FROM tickets t
        JOIN registrations r
            ON t.registration_id = r.registration_id
        JOIN events e
            ON r.event_id = e.event_id
        WHERE r.participant_id = ?
    """, (participant_id,))

    tickets = cursor.fetchall()

    print("\n========== MY TICKETS ==========")

    if not tickets:
        print("No tickets available.")
    else:
        for ticket in tickets:
            print(f"""
Ticket Code : {ticket[0]}
Event       : {ticket[1]}
Date        : {ticket[2]}
Time        : {ticket[3]}
Venue       : {ticket[4]}
----------------------------------
""")

    conn.close()