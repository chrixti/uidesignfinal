from flask import Flask, render_template, request, redirect, url_for, jsonify, session, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_results.db'
db = SQLAlchemy(app)


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/why-compost')
def why_compost():
    return render_template('why.html')

@app.route('/what-to-compost')
def what_to_compost():
    return render_template('what.html')

@app.route('/what-to-compost2')
def what_to_compost2():
    return render_template('what2.html')


@app.route('/how-to-compost')
def how_to_compost():
    return render_template('how.html')

# Route for quiz start page
@app.route('/quiz')
def quiz_start():
    return render_template('quiz.html')


@app.route('/quiz', methods=['POST'])
def quiz():
    stname = request.form['name']
    stemail = request.form['email']
    if stname =="" or stemail =="":
        return redirect(url_for('quiz'))
    if stname != "" and stemail !="": 
        session["stname"] = stname
        session["stemail"] = stemail
        session["score"] = 0
        return redirect(url_for('quiz1')) 
    # Save name and email to session or pass them as hidden fields in subsequent requests
    return render_template('quiz.html')

# Routes for quiz questions
@app.route('/quiz1', methods=['GET', 'POST'])
def quiz1():
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz'))
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
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))
    if request.method == 'POST':
        tempscore = 0
        responses2 = request.form.getlist('question2')
        correct_answers2 = ['A', 'D']
        for response in responses2:
            if response in correct_answers2:
                tempscore += 1
        if tempscore == 2:
            session["score"] += 1           
        return redirect(url_for('quiz3'))
    return render_template('quiz2.html')

@app.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))
    if request.method == 'POST':
        response3 = request.form['question3']
        # Check if the response is correct
        if response3 == 'A':
            session["score"] += 1
        return redirect(url_for('quiz4'))
    return render_template('quiz3.html')

@app.route('/quiz4', methods=['GET', 'POST'])
def quiz4():
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))
    if request.method == 'POST':
        response4 = request.form['question4']
        # Check if the response is correct
        if response4 == 'C':
            session["score"] += 1
        return redirect(url_for('quiz6'))
    return render_template('quiz4.html')


@app.route('/quiz6', methods=['GET', 'POST'])
def quiz6():
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))
    if request.method == 'POST':
        response6 = request.form['question6']
        # Check if the response is correct
        if response6 == 'B':
            session["score"] += 1
        return redirect(url_for('quiz7'))
    return render_template('quiz6.html')

@app.route('/quiz7', methods=['GET', 'POST'])
def quiz7():
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))
    if request.method == 'POST':
        response71 = request.form['question71']
        # Check if the response is correct
        if response71 == 'False':
            session["score"] += 1
        response72 = request.form['question72']
        # Check if the response is correct
        if response72 == 'True':
            session["score"] += 1
        response73 = request.form['question73']
        # Check if the response is correct
        if response73 == 'True':
            session["score"] += 1
        return redirect(url_for('quiz8'))
    return render_template('quiz7.html')

@app.route('/quiz8', methods=['GET', 'POST'])
def quiz8():
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))
    if request.method == 'POST':
        correct_compost_items = {'Banana peel', 'Grass clippings', 'Tea bag (without staples)'}
        correct_do_not_compost_items = {'Plastic bottle', 'Dairy product', 'Glass jar'}

        # Extract compost and do-not-compost items from the data
        compost_items = set(json.loads(request.form.get('hcompost')))
        do_not_compost_items = set(json.loads(request.form.get('hdonotcompost')))

        # Check if submitted items are correct
        if compost_items == correct_compost_items and do_not_compost_items == correct_do_not_compost_items:
            session["score"] += 1
        
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
    if ('score' not in session) or ('stname' not in session) or ('stemail' not in session):
        return redirect(url_for('quiz_start'))

    # Retrieve and display quiz result from the database
    # For simplicity, let's assume we're displaying the latest result
    if session['score'] >= 8:
        description = "Excellent! You have a deep understanding of composting."
    elif session['score'] >= 5:
        description = "Good job! You have a decent understanding of composting."
    else:
        description = "Keep learning! You may need to review some composting concepts."

    session.pop('stname', None)
    session.pop('stemail', None)
    session.pop('score', None)
    latest_result = QuizResult.query.order_by(QuizResult.id.desc()).first()
    return render_template('quiz_result.html', score=latest_result.score, description=description)


if __name__ == '__main__':
    app.run(debug=True)
