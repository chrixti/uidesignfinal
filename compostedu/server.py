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



# Define the QuizResult model
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    score = db.Column(db.Integer)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables
with app.app_context():
    # Create the database tables
    db.create_all()


@app.route('/admlist')
def quiz_results():
    # Retrieve quiz results from the database
    quiz_results = QuizResult.query.all()
    return render_template('admlist.html', quiz_results=quiz_results)


@app.route('/quiz')
def quiz_start():
    return render_template('quiz_start.html')


@app.route('/quiz', methods=['POST'])
def quiz():
    session["score"] = 0  # Initialize score
    session["responses"] = []  # Initialize list to store responses
    return redirect(url_for('quiz1'))

@app.route('/feedback')
def feedback():
    if 'current_question' not in session:
        return redirect(url_for('quiz_start'))
    next_question = {
        'quiz1': 'quiz2',
        'quiz2': 'quiz3',
        'quiz3': 'quiz4',
        'quiz4': 'quiz5',
        'quiz5': 'quiz6',
        'quiz6': 'quiz7',
        'quiz7': 'quiz8',
        'quiz8': 'quiz_result',
    }
    question = session['current_question']
    return render_template('feedback.html', feedback=session['feedback'], next_question=next_question[question])

# Routes for quiz questions
@app.route('/quiz1', methods=['GET', 'POST'])
def quiz1():
    if request.method == 'POST':
        user_response = request.form.get('question1')
        if not user_response:  # Checks if the response is empty
            error_message = "Please select an option before moving forward."
            return render_template('quiz1.html', error=error_message)

        correct_answer = 'C'
        is_correct = user_response == correct_answer
        session["responses"].append({
            'user_response': user_response,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answer is {correct_answer}."
        session['current_question'] = 'quiz1'
        return redirect(url_for('feedback'))
    return render_template('quiz1.html')


@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    if request.method == 'POST':
        user_responses = request.form.getlist('question2')
        if not user_responses:  # Checks if any option is selected
            error_message = "Please select at least one option before moving forward."
            return render_template('quiz2.html', error=error_message)

        correct_answers = ['A', 'D']
        is_correct = all(resp in correct_answers for resp in user_responses) and len(user_responses) == len(correct_answers)
        session["responses"].append({
            'user_response': user_responses,
            'correct_answer': correct_answers,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answers are {correct_answers}."
        session['current_question'] = 'quiz2'
        return redirect(url_for('feedback'))
    return render_template('quiz2.html')

@app.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if request.method == 'POST':
        user_response = request.form.get('question3')
        if not user_response:  # Check if the response is empty
            return render_template('quiz3.html', error="Please select an option.")
        correct_answer = 'A'
        is_correct = user_response == correct_answer
        session["responses"].append({
            'user_response': user_response,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answer is {correct_answer}."
        session['current_question'] = 'quiz3'
        return redirect(url_for('feedback'))
    return render_template('quiz3.html')

@app.route('/quiz4', methods=['GET', 'POST'])
def quiz4():
    if request.method == 'POST':
        user_response = request.form.get('question4')
        if not user_response:  # Check if the response is empty
            return render_template('quiz4.html', error="Please select an option.")
        correct_answer = 'C'
        is_correct = user_response == correct_answer
        session["responses"].append({
            'user_response': user_response,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answer is {correct_answer}."
        session['current_question'] = 'quiz4'
        return redirect(url_for('feedback'))
    return render_template('quiz4.html')

@app.route('/quiz5', methods=['GET', 'POST'])
def quiz5():
    if request.method == 'POST':
        user_responses = request.form.getlist('question5')
        if not user_responses:  # Check if any options are selected
            return render_template('quiz5.html', error="Please select at least one option.")
        correct_answers = ['A', 'C', 'D']
        is_correct = all(resp in correct_answers for resp in user_responses) and len(user_responses) == len(correct_answers)
        session["responses"].append({
            'user_response': user_responses,
            'correct_answer': correct_answers,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answers are {correct_answers}."
        session['current_question'] = 'quiz5'
        return redirect(url_for('feedback'))
    return render_template('quiz5.html')

@app.route('/quiz6', methods=['GET', 'POST'])
def quiz6():
    if request.method == 'POST':
        user_response = request.form.get('question6')
        if not user_response:  # Check if the response is empty
            return render_template('quiz6.html', error="Please select an option.")
        correct_answer = 'B'
        is_correct = user_response == correct_answer
        session["responses"].append({
            'user_response': user_response,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answer is {correct_answer}."
        session['current_question'] = 'quiz6'
        return redirect(url_for('feedback'))
    return render_template('quiz6.html')

@app.route('/quiz7', methods=['GET', 'POST'])
def quiz7():
    if request.method == 'POST':
        user_responses = [request.form.get('question71'), request.form.get('question72'), request.form.get('question73')]
        if not all(user_responses):  # Check if any required response is empty
            return render_template('quiz7.html', error="Please answer all parts of the question.")
        correct_answers = ['False', 'True', 'True']
        is_correct = all(user_response == correct_answer for user_response, correct_answer in zip(user_responses, correct_answers))
        session["responses"].append({
            'user_response': user_responses,
            'correct_answer': correct_answers,
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else f"Incorrect. The right answers are {correct_answers}."
        session['current_question'] = 'quiz7'
        return redirect(url_for('feedback'))
    return render_template('quiz7.html')

@app.route('/quiz8', methods=['GET', 'POST'])
def quiz8():
    if request.method == 'POST':
        compost_items = set(json.loads(request.form.get('hcompost', '[]')))
        do_not_compost_items = set(json.loads(request.form.get('hdonotcompost', '[]')))
        if not compost_items or not do_not_compost_items:
            return render_template('quiz8.html', error="Please categorize all items correctly.")
        correct_compost_items = {'Banana peel', 'Grass clippings', 'Tea bag (without staples)'}
        correct_do_not_compost_items = {'Plastic bottle', 'Dairy product', 'Glass jar'}
        is_correct_compost = compost_items == correct_compost_items
        is_correct_do_not_compost = do_not_compost_items == correct_do_not_compost_items
        is_correct = is_correct_compost and is_correct_do_not_compost
        session["responses"].append({
            'user_response': {
                'compost': list(compost_items),
                'do_not_compost': list(do_not_compost_items)
            },
            'correct_answer': {
                'compost': list(correct_compost_items),
                'do_not_compost': list(correct_do_not_compost_items)
            },
            'is_correct': is_correct
        })
        if is_correct:
            session["score"] += 1
        session['feedback'] = "Correct!" if is_correct else "Incorrect. Check the correct items for both composting and non-composting."
        session['current_question'] = 'quiz8'
        return redirect(url_for('feedback'))
    return render_template('quiz8.html')


@app.route('/quiz_result')
def quiz_result():
    if 'score' not in session:
        return redirect(url_for('quiz_start'))

    score = session.get('score', 0)
    responses = session.get('responses', [])

    # Construct a result object that includes responses, if it's needed based on your template
    result = {
        'responses': responses
    }

    description = "Keep learning! You may need to review some composting concepts."
    if score >= 8:
        description = "Excellent! You have a deep understanding of composting."
    elif score >= 5:
        description = "Good job! You have a decent understanding of composting."

    # Clear session after use
    session.pop('score', None)
    session.pop('responses', None)

    return render_template('quiz_result.html', score=score, description=description, result=result)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
