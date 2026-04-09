import sqlite3

def save_booking_to_sql(details):
    conn = sqlite3.connect("bookings_db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    c.execute("""
        INSERT INTO booking (name, email, date, time)
        VALUES(?, ?, ?, ?)
    """,(
        details.name,
        details.email,
        details.date,
        details.time
    ))
    conn.commit()
    conn.close()

