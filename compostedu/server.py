from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Changed from 'template/index.html'

@app.route('/basics')
def basics():
    return render_template('basics.html')  # Changed from 'template/basics.html'

@app.route('/home')
def home():
    return render_template('home.html')  # Changed from 'template/home.html'

@app.route('/backyard')
def backyard():
    return render_template('backyard.html')  # Changed from 'template/backyard.html'

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')  # Changed from 'template/quiz.html'

if __name__ == '__main__':
    app.run(debug=True)
