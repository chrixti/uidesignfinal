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
            return render_template('quiz2.html', error="Please select at least one option before moving forward.")

        correct_answers = {'A', 'D'}
        user_responses_set = set(user_responses)
        correct_count = len(user_responses_set & correct_answers)
        total_possible = len(correct_answers)

        partial_score = correct_count / total_possible
        session["score"] += partial_score

        session["responses"].append({
            'user_response': user_responses,
            'correct_answer': list(correct_answers),
            'is_correct': correct_count == len(user_responses_set)
        })

        if correct_count == len(user_responses_set):
            feedback_text = "Correct!"
        elif correct_count > 0:
            feedback_text = f"Partial credit received. You selected {user_responses}. The correct answers are {list(correct_answers)}."
        else:
            feedback_text = f"Incorrect. The correct answers are {list(correct_answers)}."

        session['feedback'] = feedback_text
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

        correct_answers = {'A', 'C', 'D'}
        user_responses_set = set(user_responses)
        correct_count = len(user_responses_set & correct_answers)
        total_possible = len(correct_answers)

        partial_score = correct_count / total_possible
        session["score"] += partial_score

        session["responses"].append({
            'user_response': user_responses,
            'correct_answer': list(correct_answers),
            'is_correct': correct_count == len(user_responses_set)
        })

        if correct_count == len(user_responses_set):
            feedback_text = "Correct!"
        elif correct_count > 0:
            feedback_text = f"Partial credit received. You selected {user_responses}. The correct answers are {list(correct_answers)}."
        else:
            feedback_text = f"Incorrect. The correct answers are {list(correct_answers)}."

        session['feedback'] = feedback_text
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
        correct_answers = ['False', 'True', 'True']

        # Check if all responses are filled
        if not all(user_responses):  
            return render_template('quiz7.html', error="Please answer all parts of the question.")

        # Calculate score: 1 point per correct answer
        score = sum(1 for user_response, correct_answer in zip(user_responses, correct_answers) if user_response == correct_answer)
        session["score"] += score  # Add total points for this quiz to the session score

        # Store responses
        session["responses"].append({
            'user_response': user_responses,
            'correct_answer': correct_answers,
            'is_correct': score == len(user_responses)  # True if all are correct
        })

        # Generate feedback based on performance
        if score == len(user_responses):
            feedback_text = "Correct!"
        elif score > 0:
            feedback_text = f"Some answers were incorrect. You answered {user_responses}. The correct answers are {correct_answers}."
        else:
            feedback_text = f"Incorrect. The correct answers are {correct_answers}."

        session['feedback'] = feedback_text
        session['current_question'] = 'quiz7'
        return redirect(url_for('feedback'))
    return render_template('quiz7.html')





@app.route('/quiz8', methods=['GET', 'POST'])
def quiz8():
    if request.method == 'POST':
        compost_items = set(json.loads(request.form.get('hcompost', '[]')))
        do_not_compost_items = set(json.loads(request.form.get('hdonotcompost', '[]')))

        correct_compost_items = {'Banana peel', 'Grass clippings', 'Tea bag (without staples)'}
        correct_do_not_compost_items = {'Plastic bottle', 'Dairy product', 'Glass jar'}

        correct_compost_count = len(compost_items & correct_compost_items)
        correct_do_not_compost_count = len(do_not_compost_items & correct_do_not_compost_items)
        total_possible_compost = len(correct_compost_items)
        total_possible_do_not_compost = len(correct_do_not_compost_items)

        partial_score_compost = correct_compost_count / total_possible_compost
        partial_score_do_not_compost = correct_do_not_compost_count / total_possible_do_not_compost
        total_partial_score = (partial_score_compost + partial_score_do_not_compost) / 2

        session["score"] += total_partial_score
        session["responses"].append({
            'user_response': {
                'compost': list(compost_items),
                'do_not_compost': list(do_not_compost_items)
            },
            'correct_answer': {
                'compost': list(correct_compost_items),
                'do_not_compost': list(correct_do_not_compost_items)
            },
            'is_correct': total_partial_score == 1
        })

        if total_partial_score == 1:
            feedback_text = "Correct!"
        elif total_partial_score > 0:
            feedback_text = f"Partial credit received. You categorized as compost: {list(compost_items)}, and as do not compost: {list(do_not_compost_items)}. Correct compost items are {list(correct_compost_items)}, and correct do not compost items are {list(correct_do_not_compost_items)}."
        else:
            feedback_text = f"Incorrect. Correct compost items are {list(correct_compost_items)}, and correct do not compost items are {list(correct_do_not_compost_items)}."

        session['feedback'] = feedback_text
        session['current_question'] = 'quiz8'
        return redirect(url_for('feedback'))
    return render_template('quiz8.html')


@app.route('/quiz_result')
def quiz_result():
    if 'score' not in session:
        return redirect(url_for('quiz_start'))

    score = session.get('score', 0)
    # Round the score to the nearest hundredth
    rounded_score = round(score, 2)

    responses = session.get('responses', [])

    result = {
        'responses': responses
    }

    description = "Keep learning! You may need to review some composting concepts."
    if rounded_score >= 8:
        description = "Excellent! You have a deep understanding of composting."
    elif rounded_score >= 5:
        description = "Good job! You have a decent understanding of composting."

    # Ensure the session is cleaned up after displaying results
    session.pop('score', None)
    session.pop('responses', None)

    return render_template('quiz_result.html', score=rounded_score, description=description, result=result)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
