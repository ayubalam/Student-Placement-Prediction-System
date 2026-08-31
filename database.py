import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")


def get_connection():
    conn = sqlite3.connect(DATABASE)
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            cgpa REAL NOT NULL,
            marks REAL NOT NULL,
            internship INTEGER NOT NULL,
            tier TEXT NOT NULL,
            fullstack_projects INTEGER DEFAULT 0,
            aiml_projects INTEGER DEFAULT 0,
            android_projects INTEGER DEFAULT 0,
            uiux_projects INTEGER DEFAULT 0,
            dsa_rating INTEGER DEFAULT 0,
            certifications INTEGER DEFAULT 0,
            communication TEXT,
            prediction TEXT NOT NULL,
            probability REAL NOT NULL,
            career_recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


def register_student(full_name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students (
                full_name,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            full_name,
            email,
            password
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def get_student_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE email = ?",
        (email,)
    )

    student = cursor.fetchone()

    conn.close()

    return student


def save_prediction(
    student_id,
    cgpa,
    marks,
    internship,
    tier,
    fullstack_projects,
    aiml_projects,
    android_projects,
    uiux_projects,
    dsa_rating,
    certifications,
    communication,
    prediction,
    probability,
    career_recommendation
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            student_id,
            cgpa,
            marks,
            internship,
            tier,
            fullstack_projects,
            aiml_projects,
            android_projects,
            uiux_projects,
            dsa_rating,
            certifications,
            communication,
            prediction,
            probability,
            career_recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        cgpa,
        marks,
        internship,
        tier,
        fullstack_projects,
        aiml_projects,
        android_projects,
        uiux_projects,
        dsa_rating,
        certifications,
        communication,
        prediction,
        probability,
        career_recommendation
    ))

    conn.commit()
    conn.close()


def get_student_predictions(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE student_id = ?
        ORDER BY created_at DESC
    """, (student_id,))

    predictions = cursor.fetchall()

    conn.close()

    return predictions


if __name__ == "__main__":

    create_table()

    print()
    print("Database Created Successfully")
    print("students table created.")
    print("predictions table created.")
    print()