import sqlite3
import random
import string
from database import get_connection


def generate_transaction_id():
    return "TXN" + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )


def make_payment(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.registration_id, e.event_id, e.name, e.fee
        FROM registrations r
        JOIN events e ON r.event_id = e.event_id
        WHERE r.participant_id = ?
        AND r.registration_status = 'Interested'
    """, (participant_id,))

    registrations = cursor.fetchall()

    if not registrations:
        print("\nYou have no pending registrations.")
        conn.close()
        return

    print("\n========== PENDING PAYMENTS ==========")

    for r in registrations:
        print(
            f"Registration ID: {r[0]} | "
            f"Event: {r[2]} | Fee: ₹{r[3]}"
        )

    try:
        registration_id = int(input("\nEnter Registration ID: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return

    selected = None

    for r in registrations:
        if r[0] == registration_id:
            selected = r
            break

    if not selected:
        print("Invalid registration.")
        conn.close()
        return

    transaction_id = generate_transaction_id()

    cursor.execute("""
        INSERT INTO payments
        (registration_id, amount, payment_status, transaction_id)
        VALUES (?, ?, 'Successful', ?)
    """, (registration_id, selected[3], transaction_id))

    cursor.execute("""
        UPDATE registrations
        SET registration_status = 'Paid'
        WHERE registration_id = ?
    """, (registration_id,))

    conn.commit()

    print("\nPayment successful!")
    print(f"Amount       : ₹{selected[3]}")
    print(f"Transaction  : {transaction_id}")

    conn.close()


def view_all_payments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.payment_id,
            u.name,
            e.name,
            p.amount,
            p.payment_status,
            p.transaction_id
        FROM payments p
        JOIN registrations r
            ON p.registration_id = r.registration_id
        JOIN users u
            ON r.participant_id = u.user_id
        JOIN events e
            ON r.event_id = e.event_id
    """)

    payments = cursor.fetchall()

    print("\n========== ALL PAYMENTS ==========")

    if not payments:
        print("No payments available.")
    else:
        for p in payments:
            print(
                f"Payment ID: {p[0]} | "
                f"Participant: {p[1]} | "
                f"Event: {p[2]} | "
                f"Amount: ₹{p[3]} | "
                f"Status: {p[4]} | "
                f"Transaction: {p[5]}"
            )

    conn.close()