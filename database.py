import sqlite3
import os

DATABASE = "database.db"


def get_connection():

    db_path = os.path.abspath(DATABASE)

    print(f"Using Database: {db_path}")

    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row

    return conn


def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    conn.close()


def register_student(

    full_name,
    email,
    password

):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            INSERT INTO students(

                full_name,
                email,
                password

            )

            VALUES(?,?,?)

        """, (

            full_name,
            email,
            password

        ))

        conn.commit()

        print("✅ User inserted successfully.")

        return True

    except sqlite3.IntegrityError as e:

        print("❌ Integrity Error:", e)

        return False

    except Exception as e:

        print("❌ Database Error:", e)

        return False

    finally:

        conn.close()


def get_student_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM students WHERE email=?",

        (email,)

    )

    student = cursor.fetchone()

    conn.close()

    return student


if __name__ == "__main__":

    create_table()

    print()
    print("===================================")
    print("Database Created Successfully")
    print("students table created.")
    print("===================================")
    print()