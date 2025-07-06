from flask import Flask, render_template, request, redirect, flash, url_for, session
from models import *
import json 
import os
from datetime import datetime,time 


app = Flask(__name__)
app.secret_key = "mahith-23f3001517"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master_mahith1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from datetime import timedelta




db.init_app(app)
with app.app_context():
    db.create_all()


def recreate_database():
    if not os.path.exists("instance"):
        os.makedirs("instance")  
    
    db_path = "instance/quiz_master_mahith.db"
    if os.path.exists(db_path):  
        os.remove(db_path)  
        print("✅ Old database deleted.")

    with app.app_context():
        db.create_all()
        print("✅ New database created.")

recreate_database()

@app.route('/')
def welcome():
    return render_template('main.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
       
        if email == "admin@gmail.com" and password == "admin123":
            session["user_id"] = "198092"
            session["username"] = "admin"
            session["role"] = "admin"
            return redirect(url_for('admin')) 
        
        
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session["user_id"] = user.id
            session["username"] = user.full_name
            session["role"] = "user"
            return redirect(url_for("user"))  
        
        

    return render_template("login.html")










@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        dob = request.form.get('dob', '').strip()
        password = request.form.get('password', '').strip()

        if not all([full_name, email,  dob, password]):
            return redirect(url_for('register'))

        try:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()  
        except ValueError:
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('register'))

        new_user = User(full_name=full_name, password=password,email=email, dob=dob)
        db.session.add(new_user)
        db.session.commit()

        
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for('login'))  

    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    questions = Questions.query.all()
    quizzes = Quiz.query.all()

    return render_template('admin.html', subjects=subjects, chapters=chapters, questions=questions, quizzes=quizzes)


@app.route('/user', methods=['GET', 'POST'])
def user():
    
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for('login'))  

    quizzes = Quiz.query.all()
    return render_template('user.html', quizzes=quizzes)







@app.route('/user/quiz_details/<int:quiz_id>')
def quiz_details(quiz_id):
    quiz=Quiz.query.get(quiz_id)
    subject_name=quiz.chapter.subject.name
    num_questions=Questions.query.filter_by(quiz_id=quiz_id).count()
    return render_template('quiz_details.html',quiz=quiz,subject_name=subject_name,num_questions=num_questions)






@app.route('/admin/add_subject', methods=['GET', 'POST'])
def add_subject():
    subjects = Subject.query.all()  
    if request.method == 'POST':
        name = request.form.get('name').strip()
        description = request.form.get('description').strip()

        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('add_subject.html', subjects=subjects)

@app.route('/admin/add_chapter', methods=['GET', 'POST'])
def add_chapter():
    subjects = Subject.query.all()  
    
    if request.method == 'POST':
        name = request.form.get('name').strip()
        description = request.form.get('description').strip()
        subject_id = request.form.get('subject_id')  

        if not name or not subject_id:
            return redirect(url_for('add_chapter'))

        try:
            subject_id = int(subject_id) 
            new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            return redirect(url_for('admin'))
        except ValueError:
            return redirect(url_for('add_chapter'))

    return render_template('add_chapter.html', subjects=subjects)


@app.route('/admin/add_question', methods=['GET', 'POST'])
def add_question():
    quizzes = Quiz.query.all()  
    if request.method == 'POST':
        question_statement = request.form.get('question').strip()
        quiz_id = int(request.form.get('quiz_id').strip())
        option1 = request.form.get('option1').strip()
        option2 = request.form.get('option2').strip()
        option3 = request.form.get('option3').strip()
        option4 = request.form.get('option4').strip()
        correct_answer = request.form.get('correct_answer').strip()

        new_question = Questions(
            question_statement=question_statement,
            quiz_id=quiz_id,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('add_question.html', quizzes=quizzes)

@app.route('/admin/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    chapters = Chapter.query.all()  
    if request.method == 'POST':
        chapter_id = int(request.form.get('chapter_id', '0'))
        date_of_quiz_str = request.form.get('date_of_quiz').strip()
        time_duration_str = request.form.get('time_duration').strip()
        remarks = request.form.get('remarks').strip()
        date_of_quiz = datetime.strptime(date_of_quiz_str, "%Y-%m-%d").date()
        if time_duration_str:
            try:
                hours, minutes = map(int, time_duration_str.split(":"))
                time_duration = time(hour=hours, minute=minutes)
            except ValueError:
                return "Invalid time format! Use HH:MM format.", 400
        else:
            time_duration = None

        new_quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks
        )
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('add_quiz.html', chapters=chapters)





@app.route('/admin/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for('admin'))
    
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return redirect(url_for('admin'))
    
    chapters=Chapter.query.filter_by(subject_id=subject.id).all()
    for chapter in chapters:
        db.session.delete(chapter)
    
   
    
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete_chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        
    else:
        return("404 error")
    return redirect(url_for('admin'))

@app.route('/admin/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Questions.query.get(question_id)
    if not question:
        return redirect(url_for('admin'))
    
    db.session.delete(question)
    db.session.commit()
    
    return redirect(url_for('admin'))

@app.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_subject.html', subject=subject)

@app.route('/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_chapter.html', chapter=chapter)

@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if request.method == 'POST':
        quiz.chapter.name = request.form['chapter_name']
        date_of_quiz_str = request.form['date_of_quiz']
        quiz.date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()
        quiz.remarks = request.form['remarks']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_quiz.html', quiz=quiz)

@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Questions.query.get(question_id)
    if request.method == 'POST':
        question.question_statement = request.form['question_statement']
        question.option1 = request.form['option1']
        question.option2 = request.form['option2']
        question.option3 = request.form['option3']
        question.option4 = request.form['option4']
        question.correct_answer = request.form['correct_answer']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_question.html', question=question)



@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/user/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    questions = Questions.query.filter_by(quiz_id=quiz_id).all()
    
    if not quiz:
        return redirect(url_for('home'))

    return render_template('quiz_page.html', quiz=quiz, questions=questions)



@app.route('/user/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for('login'))

    quiz_id = request.form.get("quiz_id")  
    if not quiz_id:
        return redirect(url_for('user'))  

 
    questions = Questions.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)
    total_scored = 0  

    
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and user_answer.strip() == question.correct_answer.strip():
            total_scored += 1  

    score_entry = Scores(
        quiz_id=quiz_id,
        user_id=user.id,
        total_scored=total_scored,
        time_stamp_of_attempt=datetime.utcnow()
    )
    db.session.add(score_entry)
    db.session.commit()

    

    
    return redirect(url_for('score_page', user_id=user.id, quiz_id=quiz_id))


@app.route('/score_page', methods=['GET'])
def score_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    quiz_id = request.args.get('quiz_id')

    if not quiz_id:
        return redirect(url_for('user'))  

    user_score = Scores.query.filter_by(user_id=user_id, quiz_id=quiz_id).order_by(Scores.id.desc()).first()
    total_questions = Questions.query.filter_by(quiz_id=quiz_id).count()

    return render_template('score_page.html', score=user_score, total_questions=total_questions, quiz_id=quiz_id)








@app.route('/admin/display_users',methods=['GET','POST'])
def display_users():
    users=User.query.all()


    return render_template('display_users.html',users=users)


    

@app.route('/user/search', methods=["GET"])
def search_quiz():
    if "user_id" not in session:
        return redirect(url_for('login'))

    search_query = request.args.get("search", "").strip()
   

    if not search_query:
        return redirect(url_for('user_home')) 
    
    quizzes = Quiz.query.join(Chapter).filter(
    Chapter.name.ilike(f"%{search_query}%")
    ).all()
    


    return render_template("user_search.html", quizzes=quizzes, search_query=search_query)


@app.route('/admin/search', methods=["GET"])
def search_admin():
    
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for('login')) 

    search_query = request.args.get("search", "").strip()

    if not search_query:
        return redirect(url_for('admin'))  
    
    subjects = Subject.query.filter(Subject.name.ilike(f"%{search_query}%")).all()
    chapters = Chapter.query.join(Subject).filter(
        Chapter.name.ilike(f"%{search_query}%") | Subject.name.ilike(f"%{search_query}%")
    ).all()

    return render_template("admin_search.html", 
                           subjects=subjects, 
                           chapters=chapters, 
                           search_query=search_query)


@app.route('/summary')
def summary():
    user_id = session.get('user_id')  
    if not user_id:
        return "User not logged in", 403 

  
    results = Scores.query.filter_by(user_id=user_id).all()

   
    quiz_ids = [score.quiz_id for score in results]
    total_scores = [score.total_scored for score in results]

    return render_template('summary.html', quiz_ids=quiz_ids, total_scores=total_scores)

@app.route('/admin/summary')
def admin_summary():
    users = User.query.all()  
    return render_template('admin_summary.html', users=users)








if __name__ == "__main__":
    app.run(debug=True)
