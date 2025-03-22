import os
import logging

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import random


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "annie_default_secret_key")

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///annie.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()
    
    # Initialize database with some initial vocabulary if it's empty
    from models import Vocabulary, Exercise, Quiz
    
    if not Vocabulary.query.first():
        initial_vocabulary = [
            Vocabulary(english="hello", vietnamese="xin chào", example="Hello, how are you?"),
            Vocabulary(english="goodbye", vietnamese="tạm biệt", example="Goodbye, see you tomorrow."),
            Vocabulary(english="thank you", vietnamese="cảm ơn", example="Thank you for your help."),
            Vocabulary(english="please", vietnamese="làm ơn", example="Please help me."),
            Vocabulary(english="sorry", vietnamese="xin lỗi", example="I'm sorry for the delay."),
            Vocabulary(english="yes", vietnamese="vâng/có", example="Yes, I agree."),
            Vocabulary(english="no", vietnamese="không", example="No, I don't understand."),
            Vocabulary(english="good", vietnamese="tốt", example="The weather is good today."),
            Vocabulary(english="bad", vietnamese="tồi", example="I had a bad day."),
            Vocabulary(english="friend", vietnamese="bạn bè", example="She is my best friend."),
            Vocabulary(english="family", vietnamese="gia đình", example="I love my family."),
            Vocabulary(english="happy", vietnamese="vui vẻ", example="I am happy to see you."),
            Vocabulary(english="sad", vietnamese="buồn", example="She feels sad today."),
            Vocabulary(english="food", vietnamese="thức ăn", example="The food is delicious."),
            Vocabulary(english="water", vietnamese="nước", example="I need some water."),
            Vocabulary(english="book", vietnamese="sách", example="I'm reading a good book."),
            Vocabulary(english="school", vietnamese="trường học", example="The school is closed today."),
            Vocabulary(english="house", vietnamese="nhà", example="This is my house."),
            Vocabulary(english="car", vietnamese="xe hơi", example="He drives a new car."),
            Vocabulary(english="time", vietnamese="thời gian", example="What time is it?"),
            Vocabulary(english="weather", vietnamese="thời tiết", example="The weather is nice today."),
            Vocabulary(english="beautiful", vietnamese="đẹp", example="She has a beautiful smile."),
            Vocabulary(english="difficult", vietnamese="khó khăn", example="This problem is difficult."),
            Vocabulary(english="easy", vietnamese="dễ dàng", example="The test was easy."),
            Vocabulary(english="work", vietnamese="công việc", example="I have work to do."),
            Vocabulary(english="study", vietnamese="học tập", example="I study English every day."),
            Vocabulary(english="sleep", vietnamese="ngủ", example="I need to sleep early tonight."),
            Vocabulary(english="eat", vietnamese="ăn", example="Let's eat lunch together."),
            Vocabulary(english="drink", vietnamese="uống", example="Would you like to drink coffee?"),
            Vocabulary(english="morning", vietnamese="buổi sáng", example="Good morning!")
        ]
        db.session.add_all(initial_vocabulary)
        db.session.commit()
    
    if not Exercise.query.first():
        initial_exercises = [
            Exercise(question="Complete: 'Hello, ____ are you?'", answer="how", options="how,what,where,why"),
            Exercise(question="Translate: 'Xin chào'", answer="hello", options="hello,hi,hey,good"),
            Exercise(question="Fill in: 'I want to ____ you.'", answer="thank", options="thank,help,meet,see"),
            Exercise(question="Choose the correct word: 'I am ____ for being late.'", answer="sorry", options="sorry,sad,happy,angry"),
            Exercise(question="Complete: '_____ help me, please.'", answer="Please", options="Please,Can,Will,Should")
        ]
        db.session.add_all(initial_exercises)
        db.session.commit()
    
    if not Quiz.query.first():
        initial_quizzes = [
            Quiz(question="What is 'xin chào' in English?", answer="hello", options="hello,goodbye,thank you,please"),
            Quiz(question="Which word means 'cảm ơn' in English?", answer="thank you", options="thank you,sorry,please,excuse me"),
            Quiz(question="Select the correct translation for 'tạm biệt':", answer="goodbye", options="goodbye,hello,yes,no"),
            Quiz(question="'Xin lỗi' translates to which English word?", answer="sorry", options="sorry,thank you,please,excuse me"),
            Quiz(question="What does 'làm ơn' mean in English?", answer="please", options="please,thank you,excuse me,sorry")
        ]
        db.session.add_all(initial_quizzes)
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vocabulary')
def vocabulary():
    # Get all vocabulary items from the database
    vocab_items = models.Vocabulary.query.all()
    return render_template('vocabulary.html', vocab_items=vocab_items)

@app.route('/exercises')
def exercises():
    # Get all exercises from the database
    all_exercises = models.Exercise.query.all()
    # Select 5 random exercises to display
    if len(all_exercises) > 5:
        selected_exercises = random.sample(all_exercises, 5)
    else:
        selected_exercises = all_exercises
        
    for exercise in selected_exercises:
        exercise.options_list = exercise.options.split(',')
    
    return render_template('exercises.html', exercises=selected_exercises)

@app.route('/quiz')
def quiz():
    # Get all quizzes from the database
    all_quizzes = models.Quiz.query.all()
    # Select 5 random quizzes to display
    if len(all_quizzes) > 5:
        selected_quizzes = random.sample(all_quizzes, 5)
    else:
        selected_quizzes = all_quizzes
        
    for quiz in selected_quizzes:
        quiz.options_list = quiz.options.split(',')
    
    return render_template('quiz.html', quizzes=selected_quizzes)

@app.route('/check_exercise', methods=['POST'])
def check_exercise():
    if request.method == 'POST':
        correct_count = 0
        total = 0
        results = []
        
        for key, value in request.form.items():
            if key.startswith('exercise_'):
                exercise_id = int(key.split('_')[1])
                exercise = models.Exercise.query.get(exercise_id)
                total += 1
                
                if exercise and value.lower().strip() == exercise.answer.lower().strip():
                    correct_count += 1
                    results.append({'id': exercise_id, 'correct': True, 'answer': exercise.answer})
                else:
                    results.append({'id': exercise_id, 'correct': False, 'answer': exercise.answer if exercise else 'Unknown'})
        
        session['exercise_results'] = {
            'correct': correct_count,
            'total': total,
            'percentage': (correct_count / total * 100) if total > 0 else 0,
            'details': results
        }
        
        # Update the user's progress if they are logged in
        # For now, we'll just store it in the session
        
        return redirect(url_for('progress'))
    
    return redirect(url_for('exercises'))

@app.route('/check_quiz', methods=['POST'])
def check_quiz():
    if request.method == 'POST':
        correct_count = 0
        total = 0
        results = []
        
        for key, value in request.form.items():
            if key.startswith('quiz_'):
                quiz_id = int(key.split('_')[1])
                quiz = models.Quiz.query.get(quiz_id)
                total += 1
                
                if quiz and value.lower().strip() == quiz.answer.lower().strip():
                    correct_count += 1
                    results.append({'id': quiz_id, 'correct': True, 'answer': quiz.answer})
                else:
                    results.append({'id': quiz_id, 'correct': False, 'answer': quiz.answer if quiz else 'Unknown'})
        
        session['quiz_results'] = {
            'correct': correct_count,
            'total': total,
            'percentage': (correct_count / total * 100) if total > 0 else 0,
            'details': results
        }
        
        # Update the user's progress if they are logged in
        # For now, we'll just store it in the session
        
        return redirect(url_for('progress'))
    
    return redirect(url_for('quiz'))

@app.route('/progress')
def progress():
    # Get progress data from session
    exercise_results = session.get('exercise_results', {
        'correct': 0,
        'total': 0,
        'percentage': 0,
        'details': []
    })
    
    quiz_results = session.get('quiz_results', {
        'correct': 0,
        'total': 0,
        'percentage': 0,
        'details': []
    })
    
    # Calculate overall progress
    total_correct = exercise_results.get('correct', 0) + quiz_results.get('correct', 0)
    total_questions = exercise_results.get('total', 0) + quiz_results.get('total', 0)
    overall_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    return render_template('progress.html', 
                           exercise_results=exercise_results,
                           quiz_results=quiz_results,
                           overall_percentage=overall_percentage)

@app.route('/pronunciation')
def pronunciation():
    return render_template('pronunciation.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')
