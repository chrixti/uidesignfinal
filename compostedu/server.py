from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html')  

@app.route('/welcome')
def welcome():
   return render_template('welcome.html')  

@app.route('/basics')
def basics():
    return render_template('basics.html')  

@app.route('/home')
def home():
    return render_template('home.html')  

@app.route('/backyard')
def backyard():
    return render_template('backyard.html')  

@app.route('/quiz')
def quiz():
    return render_template('quiz.html') 

if __name__ == '__main__':
    app.run(debug=True)
