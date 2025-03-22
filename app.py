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
            # Common Verbs
            Vocabulary(english="walk", vietnamese="đi bộ", example="I walk to school every day."),
            Vocabulary(english="dance", vietnamese="nhảy múa", example="She loves to dance at parties."),
            Vocabulary(english="swim", vietnamese="bơi lội", example="We swim in the pool every weekend."),
            Vocabulary(english="sing", vietnamese="hát", example="He sings in a choir."),
            Vocabulary(english="cook", vietnamese="nấu ăn", example="I cook dinner every evening."),
            Vocabulary(english="paint", vietnamese="vẽ", example="The artist paints beautiful pictures."),
            Vocabulary(english="jump", vietnamese="nhảy", example="Children jump with joy."),
            Vocabulary(english="laugh", vietnamese="cười", example="We laugh at funny jokes."),
            Vocabulary(english="cry", vietnamese="khóc", example="The baby cries when hungry."),
            Vocabulary(english="sleep", vietnamese="ngủ", example="I sleep eight hours every night."),
            
            # Professions
            Vocabulary(english="engineer", vietnamese="kỹ sư", example="He works as a software engineer."),
            Vocabulary(english="nurse", vietnamese="y tá", example="The nurse takes care of patients."),
            Vocabulary(english="chef", vietnamese="đầu bếp", example="The chef creates delicious meals."),
            Vocabulary(english="pilot", vietnamese="phi công", example="The pilot flies large airplanes."),
            Vocabulary(english="artist", vietnamese="nghệ sĩ", example="She is a talented artist."),
            Vocabulary(english="dentist", vietnamese="nha sĩ", example="Visit the dentist twice a year."),
            Vocabulary(english="lawyer", vietnamese="luật sư", example="The lawyer represents her clients."),
            Vocabulary(english="architect", vietnamese="kiến trúc sư", example="The architect designs buildings."),
            
            # Colors
            Vocabulary(english="red", vietnamese="màu đỏ", example="The rose is red."),
            Vocabulary(english="blue", vietnamese="màu xanh dương", example="The sky is blue."),
            Vocabulary(english="green", vietnamese="màu xanh lá", example="The grass is green."),
            Vocabulary(english="yellow", vietnamese="màu vàng", example="The sun is yellow."),
            Vocabulary(english="purple", vietnamese="màu tím", example="She wore a purple dress."),
            Vocabulary(english="orange", vietnamese="màu cam", example="The orange fruit is orange."),
            Vocabulary(english="brown", vietnamese="màu nâu", example="The tree trunk is brown."),
            Vocabulary(english="pink", vietnamese="màu hồng", example="The flowers are pink."),
            
            # Animals
            Vocabulary(english="elephant", vietnamese="con voi", example="The elephant is very large."),
            Vocabulary(english="tiger", vietnamese="con hổ", example="The tiger is a wild cat."),
            Vocabulary(english="penguin", vietnamese="chim cánh cụt", example="Penguins live in Antarctica."),
            Vocabulary(english="dolphin", vietnamese="cá heo", example="Dolphins are intelligent animals."),
            Vocabulary(english="giraffe", vietnamese="hươu cao cổ", example="The giraffe has a long neck."),
            Vocabulary(english="monkey", vietnamese="con khỉ", example="Monkeys like bananas."),
            Vocabulary(english="rabbit", vietnamese="con thỏ", example="The rabbit hops quickly."),
            Vocabulary(english="snake", vietnamese="con rắn", example="The snake slithers on the ground."),
            
            # Food and Drinks
            Vocabulary(english="pizza", vietnamese="bánh pizza", example="We ordered a pizza for dinner."),
            Vocabulary(english="sushi", vietnamese="sushi", example="Japanese restaurants serve sushi."),
            Vocabulary(english="coffee", vietnamese="cà phê", example="I drink coffee every morning."),
            Vocabulary(english="juice", vietnamese="nước ép", example="Orange juice is healthy."),
            Vocabulary(english="bread", vietnamese="bánh mì", example="I eat bread for breakfast."),
            Vocabulary(english="rice", vietnamese="cơm", example="Rice is a staple food in Asia."),
            Vocabulary(english="soup", vietnamese="súp", example="Hot soup is good when sick."),
            Vocabulary(english="salad", vietnamese="sa lát", example="A fresh salad is healthy."),
            
            # Weather
            Vocabulary(english="sunny", vietnamese="nắng", example="It's a sunny day today."),
            Vocabulary(english="rainy", vietnamese="mưa", example="Bring an umbrella on rainy days."),
            Vocabulary(english="cloudy", vietnamese="nhiều mây", example="The sky is cloudy."),
            Vocabulary(english="windy", vietnamese="gió", example="It's very windy outside."),
            Vocabulary(english="snowy", vietnamese="tuyết rơi", example="December is often snowy."),
            Vocabulary(english="foggy", vietnamese="sương mù", example="Be careful driving in foggy weather."),
            Vocabulary(english="stormy", vietnamese="bão", example="The sea is stormy today."),
            
            # Emotions
            Vocabulary(english="excited", vietnamese="phấn khích", example="I'm excited about the party."),
            Vocabulary(english="nervous", vietnamese="lo lắng", example="Students feel nervous before exams."),
            Vocabulary(english="proud", vietnamese="tự hào", example="Parents are proud of their children."),
            Vocabulary(english="confused", vietnamese="bối rối", example="The puzzle left me confused."),
            Vocabulary(english="surprised", vietnamese="ngạc nhiên", example="I was surprised by the gift."),
            Vocabulary(english="peaceful", vietnamese="bình yên", example="The garden is peaceful."),
            
            # Transportation
            Vocabulary(english="bicycle", vietnamese="xe đạp", example="I ride my bicycle to work."),
            Vocabulary(english="train", vietnamese="tàu hỏa", example="The train arrives at 9 AM."),
            Vocabulary(english="airplane", vietnamese="máy bay", example="The airplane flies high."),
            Vocabulary(english="bus", vietnamese="xe buýt", example="I take the bus to school."),
            Vocabulary(english="taxi", vietnamese="taxi", example="Let's take a taxi home."),
            Vocabulary(english="motorcycle", vietnamese="xe máy", example="He rides a motorcycle."),
            
            # Sports
            Vocabulary(english="football", vietnamese="bóng đá", example="We play football on weekends."),
            Vocabulary(english="basketball", vietnamese="bóng rổ", example="He's good at basketball."),
            Vocabulary(english="tennis", vietnamese="quần vợt", example="Tennis is my favorite sport."),
            Vocabulary(english="volleyball", vietnamese="bóng chuyền", example="They play volleyball at the beach."),
            Vocabulary(english="baseball", vietnamese="bóng chày", example="Baseball is popular in America."),
            Vocabulary(english="golf", vietnamese="golf", example="My father plays golf."),
            
            # School Subjects
            Vocabulary(english="mathematics", vietnamese="toán học", example="I study mathematics."),
            Vocabulary(english="science", vietnamese="khoa học", example="Science is interesting."),
            Vocabulary(english="history", vietnamese="lịch sử", example="We learn history in school."),
            Vocabulary(english="geography", vietnamese="địa lý", example="Geography teaches about countries."),
            Vocabulary(english="literature", vietnamese="văn học", example="She loves literature class."),
            Vocabulary(english="physics", vietnamese="vật lý", example="Physics is challenging."),
            
            # Technology
            Vocabulary(english="internet", vietnamese="internet", example="We use the internet daily."),
            Vocabulary(english="software", vietnamese="phần mềm", example="Install the new software."),
            Vocabulary(english="website", vietnamese="trang web", example="Visit our website."),
            Vocabulary(english="password", vietnamese="mật khẩu", example="Keep your password secret."),
            Vocabulary(english="download", vietnamese="tải xuống", example="Download the file."),
            Vocabulary(english="upload", vietnamese="tải lên", example="Upload your photos."),
            
            # Body Parts
            Vocabulary(english="head", vietnamese="đầu", example="I have a headache."),
            Vocabulary(english="hand", vietnamese="tay", example="Wash your hands."),
            Vocabulary(english="foot", vietnamese="chân", example="My foot hurts."),
            Vocabulary(english="eye", vietnamese="mắt", example="She has blue eyes."),
            Vocabulary(english="nose", vietnamese="mũi", example="The nose helps us smell."),
            Vocabulary(english="mouth", vietnamese="miệng", example="Open your mouth wide."),
            
            # Furniture
            Vocabulary(english="table", vietnamese="bàn", example="Put the book on the table."),
            Vocabulary(english="chair", vietnamese="ghế", example="Sit in the chair."),
            Vocabulary(english="bed", vietnamese="giường", example="The bed is comfortable."),
            Vocabulary(english="desk", vietnamese="bàn làm việc", example="I work at my desk."),
            Vocabulary(english="sofa", vietnamese="ghế sofa", example="Relax on the sofa."),
            Vocabulary(english="closet", vietnamese="tủ quần áo", example="Hang clothes in the closet."),
            
            # Nature
            Vocabulary(english="mountain", vietnamese="núi", example="We climb mountains."),
            Vocabulary(english="river", vietnamese="sông", example="The river flows to the sea."),
            Vocabulary(english="forest", vietnamese="rừng", example="Many animals live in the forest."),
            Vocabulary(english="beach", vietnamese="bãi biển", example="We swim at the beach."),
            Vocabulary(english="flower", vietnamese="hoa", example="The flower smells sweet."),
            Vocabulary(english="tree", vietnamese="cây", example="Birds live in trees."),
            
            # Time
            Vocabulary(english="minute", vietnamese="phút", example="Wait a minute."),
            Vocabulary(english="hour", vietnamese="giờ", example="One hour has passed."),
            Vocabulary(english="day", vietnamese="ngày", example="Have a nice day."),
            Vocabulary(english="month", vietnamese="tháng", example="January is the first month."),
            Vocabulary(english="year", vietnamese="năm", example="Happy New Year."),
            Vocabulary(english="century", vietnamese="thế kỷ", example="A century is 100 years."),
            
            # Clothing
            Vocabulary(english="shirt", vietnamese="áo sơ mi", example="He wears a white shirt."),
            Vocabulary(english="pants", vietnamese="quần", example="These pants are too long."),
            Vocabulary(english="dress", vietnamese="váy", example="She wore a beautiful dress."),
            Vocabulary(english="shoes", vietnamese="giày", example="My shoes are black."),
            Vocabulary(english="hat", vietnamese="mũ", example="Wear a hat in the sun."),
            Vocabulary(english="jacket", vietnamese="áo khoác", example="It's cold, wear a jacket."),
            
            # Family
            Vocabulary(english="mother", vietnamese="mẹ", example="I love my mother."),
            Vocabulary(english="father", vietnamese="cha", example="My father works hard."),
            Vocabulary(english="sister", vietnamese="chị/em gái", example="My sister is older than me."),
            Vocabulary(english="brother", vietnamese="anh/em trai", example="I have two brothers."),
            Vocabulary(english="grandmother", vietnamese="bà", example="Visit grandmother on Sunday."),
            Vocabulary(english="grandfather", vietnamese="ông", example="Grandfather tells great stories.")
            Vocabulary(english="run", vietnamese="chạy", example="He runs every morning."),
            Vocabulary(english="write", vietnamese="viết", example="She writes beautiful poems."),
            Vocabulary(english="read", vietnamese="đọc", example="I read books before bed."),
            Vocabulary(english="speak", vietnamese="nói", example="Can you speak English?"),
            Vocabulary(english="listen", vietnamese="nghe", example="Listen to the music."),
            Vocabulary(english="watch", vietnamese="xem", example="Let's watch a movie."),
            
            # Common Nouns
            Vocabulary(english="computer", vietnamese="máy tính", example="I need a new computer."),
            Vocabulary(english="phone", vietnamese="điện thoại", example="My phone is broken."),
            Vocabulary(english="teacher", vietnamese="giáo viên", example="Our teacher is very kind."),
            Vocabulary(english="student", vietnamese="học sinh", example="She is a good student."),
            Vocabulary(english="doctor", vietnamese="bác sĩ", example="The doctor helped me."),
            
            # Adjectives
            Vocabulary(english="smart", vietnamese="thông minh", example="You are very smart."),
            Vocabulary(english="kind", vietnamese="tốt bụng", example="She is a kind person."),
            Vocabulary(english="busy", vietnamese="bận rộn", example="I'm busy today."),
            Vocabulary(english="tired", vietnamese="mệt mỏi", example="I feel tired after work."),
            
            # Time-related
            Vocabulary(english="today", vietnamese="hôm nay", example="Today is sunny."),
            Vocabulary(english="tomorrow", vietnamese="ngày mai", example="See you tomorrow."),
            Vocabulary(english="yesterday", vietnamese="hôm qua", example="I went shopping yesterday."),
            Vocabulary(english="week", vietnamese="tuần", example="See you next week."),
            
            # Places
            Vocabulary(english="market", vietnamese="chợ", example="I'm going to the market."),
            Vocabulary(english="hospital", vietnamese="bệnh viện", example="The hospital is nearby."),
            Vocabulary(english="park", vietnamese="công viên", example="Let's go to the park."),
            Vocabulary(english="restaurant", vietnamese="nhà hàng", example="This restaurant is good."),
            
            # Feelings
            Vocabulary(english="love", vietnamese="yêu", example="I love my family."),
            Vocabulary(english="hate", vietnamese="ghét", example="I hate rainy days."),
            Vocabulary(english="enjoy", vietnamese="thích thú", example="I enjoy learning English."),
            Vocabulary(english="worry", vietnamese="lo lắng", example="Don't worry about it."),
            
            # Common phrases
            Vocabulary(english="excuse me", vietnamese="xin lỗi", example="Excuse me, where is the bank?"),
            Vocabulary(english="of course", vietnamese="dĩ nhiên", example="Of course I can help you."),
            Vocabulary(english="see you", vietnamese="tạm biệt", example="See you tomorrow."),
            Vocabulary(english="take care", vietnamese="giữ gìn sức khỏe", example="Goodbye, take care!"),
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
            Exercise(question="Choose the correct verb: 'She ____ to school every day.'", answer="walks", options="walks,walking,walked,walk"),
            Exercise(question="Fill in: 'They ____ studying English.'", answer="are", options="are,is,am,be"),
            Exercise(question="Select the opposite of 'happy':", answer="sad", options="sad,angry,tired,excited"),
            Exercise(question="Complete: 'I ____ coffee every morning.'", answer="drink", options="drink,drinks,drinking,drank"),
            Exercise(question="Choose the correct plural: 'One child, two ____'", answer="children", options="children,childs,childrens,child"),
            Exercise(question="Fill in: 'The weather is ____ today.'", answer="beautiful", options="beautiful,beautifully,beauty,beautify"),
            Exercise(question="Select the past tense: 'I ____ to the park yesterday.'", answer="went", options="went,go,going,gone"),
            Exercise(question="Complete: '____ you speak English?'", answer="Can", options="Can,Do,Are,Will"),
            Exercise(question="Choose the correct time: 'It's half ____ ten.'", answer="past", options="past,to,at,in")
        ]
        db.session.add_all(initial_exercises)
        db.session.commit()
    
    if not Quiz.query.first():
        initial_quizzes = [
            Quiz(question="What time expression means 'ngày mai'?", answer="tomorrow", options="tomorrow,today,yesterday,next week"),
            Quiz(question="Which word means 'thức ăn'?", answer="food", options="food,drink,water,meal"),
            Quiz(question="Select the correct translation for 'gia đình':", answer="family", options="family,friend,house,home"),
            Quiz(question="What is 'thời tiết' in English?", answer="weather", options="weather,season,climate,temperature"),
            Quiz(question="Choose the correct word for 'công việc':", answer="work", options="work,job,task,duty"),
            Quiz(question="'Trường học' translates to which word?", answer="school", options="school,college,class,study"),
            Quiz(question="What does 'bác sĩ' mean?", answer="doctor", options="doctor,nurse,teacher,dentist"),
            Quiz(question="Select the translation for 'máy tính':", answer="computer", options="computer,phone,laptop,tablet"),
            Quiz(question="'Thư viện' means which place?", answer="library", options="library,bookstore,school,office"),
            Quiz(question="Choose the correct sport for 'bơi lội':", answer="swimming", options="swimming,running,walking,flying")
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
    # Get random word for pronunciation practice
    words = models.Vocabulary.query.all()
    current_word = random.choice(words).english if words else "Hello"
    
    # Get 5 random words for daily practice
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
