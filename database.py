import sqlite3

DATABASE_NAME = "event_management.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'participant', 'volunteer'))
        )
    """)

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            fee REAL NOT NULL,
            poster TEXT,
            status TEXT DEFAULT 'Upcoming'
        )
    """)

    # Registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            registration_status TEXT DEFAULT 'Interested',
            registration_date TEXT,
            FOREIGN KEY(participant_id) REFERENCES users(user_id),
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # Payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_status TEXT DEFAULT 'Pending',
            transaction_id TEXT,
            FOREIGN KEY(registration_id) REFERENCES registrations(registration_id)
        )
    """)

    # Volunteers assigned to events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteer_schedule (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            duty_date TEXT,
            duty_time TEXT,
            responsibility TEXT,
            FOREIGN KEY(volunteer_id) REFERENCES users(user_id),
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # Expenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT,
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # Comments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            FOREIGN KEY(participant_id) REFERENCES users(user_id),
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # Tickets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id INTEGER NOT NULL,
            ticket_code TEXT UNIQUE NOT NULL,
            FOREIGN KEY(registration_id) REFERENCES registrations(registration_id)
        )
    """)

    # Default Admin
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (user_id, name, email, password, role)
        VALUES (1, 'System Admin', 'admin@gmail.com', 'admin123', 'admin')
    """)

    # Demo participant
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (name, email, password, role)
        VALUES ('Demo Participant', 'participant@gmail.com', '1234', 'participant')
    """)

    # Demo volunteer
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (name, email, password, role)
        VALUES ('Demo Volunteer', 'volunteer@gmail.com', '1234', 'volunteer')
    """)

    conn.commit()
    conn.close()


def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, name, email, role
        FROM users
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()
    return user


def register_user(name, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password, role))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()