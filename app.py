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
            # Basic Vocabulary
            Vocabulary(english="apple", vietnamese="quả táo", example="I eat an apple every day."),
            Vocabulary(english="book", vietnamese="quyển sách", example="I read a good book."),
            Vocabulary(english="cat", vietnamese="con mèo", example="The cat sleeps on the bed."),
            Vocabulary(english="dog", vietnamese="con chó", example="My dog likes to play fetch."),
            
            # Family Members
            Vocabulary(english="mother", vietnamese="mẹ", example="My mother cooks delicious food."),
            Vocabulary(english="father", vietnamese="cha", example="My father works hard."),
            Vocabulary(english="sister", vietnamese="chị/em gái", example="I have two sisters."),
            Vocabulary(english="brother", vietnamese="anh/em trai", example="My brother plays soccer."),
            Vocabulary(english="grandmother", vietnamese="bà", example="Grandmother bakes cookies."),
            Vocabulary(english="grandfather", vietnamese="ông", example="Grandfather tells great stories."),
            
            # Colors
            Vocabulary(english="red", vietnamese="màu đỏ", example="The rose is red."),
            Vocabulary(english="blue", vietnamese="màu xanh dương", example="The sky is blue."),
            Vocabulary(english="green", vietnamese="màu xanh lá", example="The grass is green."),
            Vocabulary(english="yellow", vietnamese="màu vàng", example="The sun is yellow."),
            Vocabulary(english="purple", vietnamese="màu tím", example="She likes purple flowers."),
            Vocabulary(english="orange", vietnamese="màu cam", example="The orange is orange."),
            Vocabulary(english="pink", vietnamese="màu hồng", example="Her dress is pink."),
            Vocabulary(english="brown", vietnamese="màu nâu", example="The table is brown."),
            Vocabulary(english="black", vietnamese="màu đen", example="The night is black."),
            Vocabulary(english="white", vietnamese="màu trắng", example="The clouds are white."),
            
            # Numbers
            Vocabulary(english="one", vietnamese="một", example="I have one cat."),
            Vocabulary(english="two", vietnamese="hai", example="Two plus two equals four."),
            Vocabulary(english="three", vietnamese="ba", example="I have three brothers."),
            Vocabulary(english="four", vietnamese="bốn", example="There are four seasons."),
            Vocabulary(english="five", vietnamese="năm", example="I work five days a week."),
            
            # Food and Drinks
            Vocabulary(english="rice", vietnamese="cơm", example="We eat rice for lunch."),
            Vocabulary(english="bread", vietnamese="bánh mì", example="I like fresh bread."),
            Vocabulary(english="milk", vietnamese="sữa", example="I drink milk every morning."),
            Vocabulary(english="coffee", vietnamese="cà phê", example="He drinks coffee."),
            Vocabulary(english="tea", vietnamese="trà", example="Would you like some tea?"),
            
            # Clothing
            Vocabulary(english="shirt", vietnamese="áo sơ mi", example="He wears a blue shirt."),
            Vocabulary(english="pants", vietnamese="quần", example="These pants are too long."),
            Vocabulary(english="shoes", vietnamese="giày", example="My shoes are black."),
            Vocabulary(english="hat", vietnamese="mũ", example="She wears a hat in summer."),
            Vocabulary(english="dress", vietnamese="váy", example="She bought a new dress."),
            
            # Weather
            Vocabulary(english="sunny", vietnamese="nắng", example="It's sunny today."),
            Vocabulary(english="rainy", vietnamese="mưa", example="It's a rainy day."),
            Vocabulary(english="cloudy", vietnamese="nhiều mây", example="The sky is cloudy."),
            Vocabulary(english="windy", vietnamese="gió", example="It's very windy outside."),
            Vocabulary(english="hot", vietnamese="nóng", example="Summer is hot."),
            
            # Time
            Vocabulary(english="minute", vietnamese="phút", example="Wait a minute."),
            Vocabulary(english="hour", vietnamese="giờ", example="One hour has passed."),
            Vocabulary(english="day", vietnamese="ngày", example="Have a nice day."),
            Vocabulary(english="week", vietnamese="tuần", example="See you next week."),
            Vocabulary(english="month", vietnamese="tháng", example="January is the first month."),
            
            # School
            Vocabulary(english="teacher", vietnamese="giáo viên", example="Our teacher is kind."),
            Vocabulary(english="student", vietnamese="học sinh", example="He is a good student."),
            Vocabulary(english="classroom", vietnamese="lớp học", example="The classroom is big."),
            Vocabulary(english="homework", vietnamese="bài tập về nhà", example="I have homework to do."),
            Vocabulary(english="exam", vietnamese="kỳ thi", example="The exam is next week."),
            
            # Transportation
            Vocabulary(english="car", vietnamese="xe hơi", example="I drive a car."),
            Vocabulary(english="bus", vietnamese="xe buýt", example="I take the bus to work."),
            Vocabulary(english="train", vietnamese="tàu hỏa", example="The train is fast."),
            Vocabulary(english="bicycle", vietnamese="xe đạp", example="I ride my bicycle."),
            Vocabulary(english="airplane", vietnamese="máy bay", example="We travel by airplane."),
            
            # Jobs
            Vocabulary(english="doctor", vietnamese="bác sĩ", example="She is a doctor."),
            Vocabulary(english="nurse", vietnamese="y tá", example="The nurse helps patients."),
            Vocabulary(english="engineer", vietnamese="kỹ sư", example="He works as an engineer."),
            Vocabulary(english="chef", vietnamese="đầu bếp", example="The chef cooks well."),
            Vocabulary(english="driver", vietnamese="tài xế", example="He is a taxi driver."),
            
            # Animals
            Vocabulary(english="bird", vietnamese="chim", example="Birds can fly."),
            Vocabulary(english="fish", vietnamese="cá", example="Fish swim in water."),
            Vocabulary(english="elephant", vietnamese="voi", example="The elephant is big."),
            Vocabulary(english="tiger", vietnamese="hổ", example="The tiger is dangerous."),
            Vocabulary(english="rabbit", vietnamese="thỏ", example="The rabbit hops."),
            
            # Sports
            Vocabulary(english="football", vietnamese="bóng đá", example="I play football."),
            Vocabulary(english="basketball", vietnamese="bóng rổ", example="He likes basketball."),
            Vocabulary(english="tennis", vietnamese="quần vợt", example="They play tennis."),
            Vocabulary(english="swimming", vietnamese="bơi lội", example="Swimming is good exercise."),
            Vocabulary(english="volleyball", vietnamese="bóng chuyền", example="Let's play volleyball."),
            
            # Emotions
            Vocabulary(english="happy", vietnamese="vui vẻ", example="I am happy today."),
            Vocabulary(english="sad", vietnamese="buồn", example="She feels sad."),
            Vocabulary(english="angry", vietnamese="giận dữ", example="Don't be angry."),
            Vocabulary(english="tired", vietnamese="mệt mỏi", example="I am tired now."),
            Vocabulary(english="excited", vietnamese="phấn khích", example="We are excited."),
            
            # Places
            Vocabulary(english="house", vietnamese="nhà", example="This is my house."),
            Vocabulary(english="hospital", vietnamese="bệnh viện", example="The hospital is nearby."),
            Vocabulary(english="bank", vietnamese="ngân hàng", example="I went to the bank."),
            Vocabulary(english="park", vietnamese="công viên", example="We play in the park."),
            Vocabulary(english="airport", vietnamese="sân bay", example="The airport is big."),
            
            # Furniture
            Vocabulary(english="table", vietnamese="bàn", example="Put it on the table."),
            Vocabulary(english="chair", vietnamese="ghế", example="Sit on the chair."),
            Vocabulary(english="bed", vietnamese="giường", example="I sleep in my bed."),
            Vocabulary(english="lamp", vietnamese="đèn", example="Turn on the lamp."),
            Vocabulary(english="sofa", vietnamese="ghế sofa", example="The sofa is comfortable."),
            
            # Body Parts
            Vocabulary(english="head", vietnamese="đầu", example="My head hurts."),
            Vocabulary(english="hand", vietnamese="tay", example="Wash your hands."),
            Vocabulary(english="foot", vietnamese="chân", example="My foot is sore."),
            Vocabulary(english="eye", vietnamese="mắt", example="She has blue eyes."),
            Vocabulary(english="nose", vietnamese="mũi", example="The nose smells."),
            
            # Nature
            Vocabulary(english="tree", vietnamese="cây", example="The tree is tall."),
            Vocabulary(english="flower", vietnamese="hoa", example="She likes flowers."),
            Vocabulary(english="mountain", vietnamese="núi", example="The mountain is high."),
            Vocabulary(english="river", vietnamese="sông", example="The river flows."),
            Vocabulary(english="ocean", vietnamese="đại dương", example="The ocean is vast."),
            
            # Technology
            Vocabulary(english="computer", vietnamese="máy tính", example="I use a computer."),
            Vocabulary(english="phone", vietnamese="điện thoại", example="Call my phone."),
            Vocabulary(english="internet", vietnamese="mạng internet", example="The internet is fast."),
            Vocabulary(english="email", vietnamese="thư điện tử", example="Send me an email."),
            Vocabulary(english="website", vietnamese="trang web", example="Visit our website."),
            
            # Directions
            Vocabulary(english="left", vietnamese="trái", example="Turn left here."),
            Vocabulary(english="right", vietnamese="phải", example="The store is on the right."),
            Vocabulary(english="up", vietnamese="lên", example="Go up the stairs."),
            Vocabulary(english="down", vietnamese="xuống", example="Walk down slowly."),
            Vocabulary(english="straight", vietnamese="thẳng", example="Go straight ahead."),
            
            # Subjects
            Vocabulary(english="math", vietnamese="toán học", example="I study math."),
            Vocabulary(english="science", vietnamese="khoa học", example="Science is interesting."),
            Vocabulary(english="history", vietnamese="lịch sử", example="I like history class."),
            Vocabulary(english="art", vietnamese="nghệ thuật", example="She teaches art."),
            Vocabulary(english="music", vietnamese="âm nhạc", example="I love music."),
            
            # Fruits
            Vocabulary(english="banana", vietnamese="chuối", example="I eat a banana."),
            Vocabulary(english="orange", vietnamese="cam", example="The orange is sweet."),
            Vocabulary(english="grape", vietnamese="nho", example="I like grapes."),
            Vocabulary(english="mango", vietnamese="xoài", example="Mangoes are delicious."),
            Vocabulary(english="strawberry", vietnamese="dâu tây", example="Red strawberries."),
            
            # Vegetables
            Vocabulary(english="carrot", vietnamese="cà rốt", example="Eat your carrots."),
            Vocabulary(english="potato", vietnamese="khoai tây", example="Baked potatoes."),
            Vocabulary(english="tomato", vietnamese="cà chua", example="Fresh tomatoes."),
            Vocabulary(english="cucumber", vietnamese="dưa chuột", example="Slice the cucumber."),
            Vocabulary(english="onion", vietnamese="hành tây", example="Cut the onion."),
            
            # Common Actions
            Vocabulary(english="sing", vietnamese="hát", example="She sings well."),
            Vocabulary(english="dance", vietnamese="nhảy", example="Let's dance together."),
            Vocabulary(english="jump", vietnamese="nhảy", example="The children jump."),
            Vocabulary(english="run", vietnamese="chạy", example="He runs fast."),
            Vocabulary(english="sleep", vietnamese="ngủ", example="Time to sleep."),
            # Common Verbs
            Vocabulary(english="walk", vietnamese="đi bộ", example="I walk to school every day."),
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
            Exercise(question="Choose the correct time: 'It's half ____ ten.'", answer="past", options="past,to,at,in"),
            Exercise(question="Select the correct preposition: 'He is waiting ____ the bus.'", answer="for", options="for,at,in,on"),
            Exercise(question="Choose the correct adjective: 'The elephant is ____.'", answer="big", options="big,bigger,biggest,biggly"),
            Exercise(question="Fill in: 'She ____ her homework yesterday.'", answer="did", options="did,do,done,doing"),
            Exercise(question="Complete: 'They ____ to the movies last week.'", answer="went", options="went,go,gone,going"),
            Exercise(question="Select the correct form: '____ she like pizza?'", answer="Does", options="Does,Do,Did,Done"),
            Exercise(question="Choose the correct word: 'I have ____ cats.'", answer="two", options="two,second,twice,double"),
            Exercise(question="Fill in: 'The sun ____ in the east.'", answer="rises", options="rises,rise,rising,risen"),
            Exercise(question="Complete: '____ book is very interesting.'", answer="This", options="This,These,That,Those"),
            Exercise(question="Select the correct word: 'She is ____ than me.'", answer="taller", options="taller,tall,tallest,tally"),
            Exercise(question="Choose the right answer: 'We ____ lunch at noon.'", answer="have", options="have,has,had,having")
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
            Quiz(question="Choose the correct sport for 'bơi lội':", answer="swimming", options="swimming,running,walking,flying"),
            Quiz(question="What is 'quả táo' in English?", answer="apple", options="apple,orange,banana,grape"),
            Quiz(question="Select the translation for 'màu đỏ':", answer="red", options="red,blue,green,yellow"),
            Quiz(question="'Mèo' translates to which animal?", answer="cat", options="cat,dog,bird,fish"),
            Quiz(question="What does 'xe đạp' mean?", answer="bicycle", options="bicycle,car,bus,train"),
            Quiz(question="Choose the word for 'điện thoại':", answer="phone", options="phone,computer,tablet,laptop"),
            Quiz(question="'Quần áo' means which item?", answer="clothes", options="clothes,shoes,hat,bag"),
            Quiz(question="What is 'bút chì' in English?", answer="pencil", options="pencil,pen,book,paper"),
            Quiz(question="Select the meaning of 'cửa sổ':", answer="window", options="window,door,wall,roof"),
            Quiz(question="'Bàn' translates to which furniture?", answer="table", options="table,chair,bed,desk"),
            Quiz(question="What does 'sách' mean?", answer="book", options="book,notebook,magazine,newspaper")
        ]
        db.session.add_all(initial_quizzes)
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vocabulary')
def vocabulary():
    try:
        # Get all vocabulary items from the database
        vocab_items = models.Vocabulary.query.all()
        app.logger.info(f"Found {len(vocab_items)} vocabulary items")
        return render_template('vocabulary.html', vocab_items=vocab_items)
    except Exception as e:
        app.logger.error(f"Error fetching vocabulary: {str(e)}")
        return render_template('vocabulary.html', vocab_items=[], error="Không thể tải từ vựng")

@app.route('/exercises')
def exercises():
    # Get all exercises from the database
    all_exercises = models.Exercise.query.all()
    # Select 10 random exercises to display
    if len(all_exercises) > 10:
        selected_exercises = random.sample(all_exercises, 10)
    else:
        selected_exercises = all_exercises
        
    for exercise in selected_exercises:
        exercise.options_list = exercise.options.split(',')
    
    return render_template('exercises.html', exercises=selected_exercises)

@app.route('/quiz')
def quiz():
    # Get all quizzes from the database
    all_quizzes = models.Quiz.query.all()
    # Select 10 random quizzes to display
    if len(all_quizzes) > 10:
        selected_quizzes = random.sample(all_quizzes, 10)
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
