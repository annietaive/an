import os
import logging
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "annie_default_secret_key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///annie.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Import models and initialize the database with the app
import models
models.db.init_app(app)

with app.app_context():
    models.db.create_all()
    
    # Initialize database with some initial vocabulary if it's empty
    from models import Vocabulary, Exercise, Quiz
    
    if not Vocabulary.query.first():
        initial_vocabulary = [
            # BASIC LEVEL
            Vocabulary(english="sun", vietnamese="mặt trời", example="The sun is bright today."),
            Vocabulary(english="moon", vietnamese="mặt trăng", example="The moon shines at night."),
            Vocabulary(english="star", vietnamese="ngôi sao", example="I can see many stars."),
            Vocabulary(english="cloud", vietnamese="mây", example="The clouds are white."),
            Vocabulary(english="rain", vietnamese="mưa", example="It's raining outside."),
            # ... (các mục khác)
        ]
        models.db.session.add_all(initial_vocabulary)
        models.db.session.commit()
    
    if not Exercise.query.first():
        initial_exercises = [
            Exercise(question="Complete: 'Hello, ____ are you?'", answer="how", options="how,what,where,why", difficulty="basic"),
            Exercise(question="Choose the correct verb: 'She ____ to school.'", answer="goes", options="goes,go,going,gone", difficulty="basic"),
            # ... (các mục khác)
        ]
        models.db.session.add_all(initial_exercises)
        models.db.session.commit()
    
    if not Quiz.query.first():
        initial_quizzes = [
            Quiz(question="What time expression means 'ngày mai'?", answer="tomorrow", options="tomorrow,today,yesterday,next week", difficulty="basic"),
            Quiz(question="Which word means 'thức ăn'?", answer="food", options="food,drink,water,meal", difficulty="basic"),
            # ... (các mục khác)
        ]
        models.db.session.add_all(initial_quizzes)
        models.db.session.commit()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vocabulary')
def vocabulary():
    try:
        vocab_items = models.Vocabulary.query.all()
        app.logger.info(f"Found {len(vocab_items)} vocabulary items")
        return render_template('vocabulary.html', vocab_items=vocab_items)
    except Exception as e:
        app.logger.error(f"Error fetching vocabulary: {str(e)}")
        return render_template('vocabulary.html', vocab_items=[], error="Không thể tải từ vựng")

@app.route('/exercises')
def exercises():
    all_exercises = models.Exercise.query.all()
    if len(all_exercises) > 10:
        selected_exercises = random.sample(all_exercises, 10)
    else:
        selected_exercises = all_exercises.copy()
        random.shuffle(selected_exercises)
        
    for exercise in selected_exercises:
        options_list = exercise.options.split(',')
        random.shuffle(options_list)
        exercise.options_list = options_list
    
    return render_template('exercises.html', exercises=selected_exercises)

@app.route('/quiz')
def quiz():
    all_quizzes = models.Quiz.query.all()
    if len(all_quizzes) > 10:
        selected_quizzes = random.sample(all_quizzes, 10)
    else:
        selected_quizzes = all_quizzes.copy()
        random.shuffle(selected_quizzes)
        
    for quiz in selected_quizzes:
        options_list = quiz.options.split(',')
        random.shuffle(options_list)
        quiz.options_list = options_list
    
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
        
        return redirect(url_for('progress'))
    
    return redirect(url_for('quiz'))

@app.route('/progress')
def progress():
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
    
    total_correct = exercise_results.get('correct', 0) + quiz_results.get('correct', 0)
    total_questions = exercise_results.get('total', 0) + quiz_results.get('total', 0)
    overall_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    return render_template('progress.html', 
                           exercise_results=exercise_results,
                           quiz_results=quiz_results,
                           overall_percentage=overall_percentage)

@app.route('/pronunciation')
def pronunciation():
    words = models.Vocabulary.query.all()
    current_word = random.choice(words).english if words else "Hello"
    if len(words) >= 5:
        daily_words = random.sample(words, 5)
    else:
        daily_words = words
    
    return render_template('pronunciation.html', 
                           current_word=current_word,
                           daily_words=daily_words)

@app.route('/resources')
def resources():
    return render_template('resources.html')

if __name__ == "__main__":
    app.run(debug=True)