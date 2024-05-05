#!C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_results.db'
db = SQLAlchemy(app)

# Define the QuizResult model
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    score = db.Column(db.Integer)

# Create the database tables
with app.app_context():
    # Create the database tables
    db.create_all()

# Route for quiz start page
@app.route('/')
def quiz_start():
    return render_template('quiz_start.html')


@app.route('/quiz', methods=['POST'])
def quiz():
    stname = request.form['name']
    stemail = request.form['email']
    if stname =="" or stemail =="":
        return redirect(url_for('quiz_start'))
    if stname != "" and stemail !="": 
        session["stname"] = stname
        session["stemail"] = stemail
        session["score"] = 0
        return redirect(url_for('quiz1')) 
    # Save name and email to session or pass them as hidden fields in subsequent requests
    return render_template('quiz_start.html')

# Routes for quiz questions
@app.route('/quiz1', methods=['GET', 'POST'])
def quiz1():
    session["score"] = 0;
    if request.method == 'POST':
        response1 = request.form['question1']
        # Check if the response is correct
        if response1 == 'C':
            session["score"] += 1
        return redirect(url_for('quiz2'))
    return render_template('quiz1.html')

@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    if request.method == 'POST':
        responses2 = request.form.getlist('question2')
        correct_answers2 = ['A', 'C', 'D']
        for response in responses2:
            if response in correct_answers2:
                session["score"] += 1
        return redirect(url_for('quiz3'))
    return render_template('quiz2.html')

@app.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if request.method == 'POST':
        response3 = request.form['question3']
        # Check if the response is correct
        if response3 == 'C':
            session["score"] += 1
        return redirect(url_for('quiz4'))
    return render_template('quiz3.html')

@app.route('/quiz4', methods=['GET', 'POST'])
def quiz4():
    if request.method == 'POST':
        response4 = request.form['question4']
        # Check if the response is correct
        if response4 == 'C':
            session["score"] += 1
        return redirect(url_for('quiz5'))
    return render_template('quiz4.html')

@app.route('/quiz5', methods=['GET', 'POST'])
def quiz5():
    if request.method == 'POST':
        responses5 = request.form.getlist('question5')
        correct_answers5 = ['A', 'C', 'D']
        for response in responses5:
            if response in correct_answers5:
                session["score"] += 1
        return redirect(url_for('quiz6'))
    return render_template('quiz5.html')

@app.route('/quiz6', methods=['GET', 'POST'])
def quiz6():
    if request.method == 'POST':
        response6 = request.form['question6']
        # Check if the response is correct
        if response6 == 'C':
            session["score"] += 1
        return redirect(url_for('quiz7'))
    return render_template('quiz6.html')

@app.route('/quiz7', methods=['GET', 'POST'])
def quiz7():
    if request.method == 'POST':
        response71 = request.form['question71']
        # Check if the response is correct
        if response71 == 'True':
            session["score"] += 1
        response72 = request.form['question72']
        # Check if the response is correct
        if response72 == 'False':
            session["score"] += 1
        response73 = request.form['question73']
        # Check if the response is correct
        if response73 == 'True':
            session["score"] += 1
        return redirect(url_for('quiz8'))
    return render_template('quiz7.html')

@app.route('/quiz8', methods=['GET', 'POST'])
def quiz8():
    if request.method == 'POST':
        # Process form submission
        stname = session['stname']
        stemail = session['stemail']
        # Calculate total score
        total_score = int(session['score'])
        # Save quiz result to database
        new_result = QuizResult(name=stname, email=stemail, score=total_score)
        db.session.add(new_result)
        db.session.commit()
        return redirect(url_for('show_result'))
    return render_template('quiz8.html')

# Route to show quiz result
@app.route('/show_result')
def show_result():
    # Retrieve and display quiz result from the database
    # For simplicity, let's assume we're displaying the latest result
    latest_result = QuizResult.query.order_by(QuizResult.id.desc()).first()
    return render_template('quiz_result.html', score=latest_result.score)

if __name__ == '__main__':
    app.run(debug=True)