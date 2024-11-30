from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

# DB connection helper function
def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initializing/reset user performance
def init_user_performance():
    session['total_questions'] = 0
    session['correct_answers'] = 0
    session['answered_question_ids'] = []

# Getting a random question:
def get_random_question():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Getting total number of questions
    cursor.execute('SELECT COUNT(*) as total FROM questions')
    total_questions = cursor.fetchone()['total']
    
    # Checking if all questions are answered
    if len(session.get('answered_question_ids', [])) >= total_questions:
        conn.close()
        return None
    
    # Selecting a random question(unanswered)
    query = '''
    SELECT * FROM questions 
    WHERE id NOT IN ({}) 
    ORDER BY RANDOM() LIMIT 1
    '''.format(','.join(map(str, session.get('answered_question_ids', []))) or '0')
    
    cursor.execute(query)
    question = cursor.fetchone()
    conn.close()
    
    return question

@app.route('/')
def dashboard():
    # Initializing performance if not already set
    if 'total_questions' not in session:
        init_user_performance()
    
    # Getting total number of questions
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total FROM questions')
    total_questions = cursor.fetchone()['total']
    conn.close()
    
    return render_template('home.html', 
                           total_questions=session.get('total_questions', 0),
                           correct_answers=session.get('correct_answers', 0),
                           total_available_questions=total_questions,
                           score=calculate_score())

@app.route('/quiz')
def quiz():
    # Getting a random que
    question = get_random_question()
    
    # Checking if no more questions are available
    if question is None:
        return render_template('no_more_questions.html', 
                               total_questions=session.get('total_questions', 0),
                               correct_answers=session.get('correct_answers', 0),
                               score=calculate_score())
    
    return render_template('quiz.html', 
                           question=question,
                           total_questions=session.get('total_questions', 0),
                           correct_answers=session.get('correct_answers', 0))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    # Incrementing total questions
    session['total_questions'] = session.get('total_questions', 0) + 1
    
    # Getting form data
    selected_answer = request.form.get('answer')
    question_id = request.form.get('question_id')
    
    # Adding the que to answered questions
    answered_ids = session.get('answered_question_ids', [])
    answered_ids.append(int(question_id))
    session['answered_question_ids'] = answered_ids
    
    # Verifing answer
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()
    conn.close()
    
    # Determining the correct answer
    correct_index = int(question['correct_answer']) if isinstance(question['correct_answer'], str) else question['correct_answer']
    options = [question['option1'], question['option2'], question['option3'], question['option4']]
    correct_answer = options[correct_index - 1]    
    is_correct = selected_answer == correct_answer
    
    # Updating correct answers if needed
    if is_correct:
        session['correct_answers'] = session.get('correct_answers', 0) + 1
    
    return render_template('quiz_result.html', 
                           is_correct=is_correct, 
                           correct_answer=correct_answer,
                           total_questions=session['total_questions'],
                           correct_answers=session['correct_answers'],
                           score=calculate_score())

def calculate_score():
    total = session.get('total_questions', 0)
    correct = session.get('correct_answers', 0)
    
    # division by zero error handling
    if total == 0:
        return 0
    
    return round((correct / total) * 100, 2)

@app.route('/reset')
def reset():
    # Reseting user performance
    init_user_performance()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)