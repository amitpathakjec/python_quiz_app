import sqlite3
import os

def create_database():
    db_path = 'quiz.db'
    
    # To remove existing db file if any 
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connecting and creating db 
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Creating questions table 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_answer INTEGER NOT NULL
    )
    ''')

    # Sample questions to pre-populate
    questions = [
        (
            "What is the capital of India?", 
            "New Delhi", 
            "Mumbai", 
            "Kolkata", 
            "Chennai", 
            1
        ),
        (
            "Which is the largest country area-wise?", 
            "Canada", 
            "China", 
            "Russia", 
            "India", 
            3
        ),
        (
            "Who was the first President of India?", 
            "Dr. S RadhaKrishnan", 
            "A.P.J Abdul Kalam", 
            "Dr. Rajendra Prasad", 
            "Dr. B.R Ambedkar", 
            3
        ),
        (
            "Which data structure allows index-based accessing?", 
            "Array", 
            "Dict", 
            "Set", 
            "Linked List", 
            1
        ),
        (
            "What does HTML stand for?", 
            "HyperText Markup Language", 
            "HyperText Machine Language", 
            "Hyper Transfer Markup Language", 
            "HyperText Method Language", 
            1
        )
    ]

    # Inserting to db
    cursor.executemany('''
    INSERT INTO questions 
    (question, option1, option2, option3, option4, correct_answer) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', questions)

    # Commiting changes and closing connection
    conn.commit()
    conn.close()

    print("Database created and populated successfully!")

if __name__ == '__main__':
    create_database()