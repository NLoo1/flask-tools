from flask import Flask, request, render_template, redirect, flash, jsonify
from flask import session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

def helper(num):
    title = surveys.get("satisfaction").title
    question = surveys.get("satisfaction").questions[int(num)]
    return render_template("questions.html", num=num, title=title, question=question.question, choices= question.choices)

@app.route('/questions', methods=["POST"])
def start_questions():
    return redirect('/questions/' + str(session['question_num']))

@app.route("/")
def home():
    session['question_num'] = 0
    session['responses'] = []
    survey = surveys.get("satisfaction")
    return render_template("home.html", title=survey.title, instructions=survey.instructions)

# Displays next question. Should be accessed after redirection to /answer
@app.route("/questions/<num>", methods=["GET", "POST"])
def next_question(num):
    if session['question_num'] < int(num):
        flash("Please complete questions in order. ")
        return redirect("/questions/" + str(session['question_num']))
    # If question_num exceeds number of questions, redirect to thank you
    elif session['question_num'] > len(surveys.get("satisfaction").questions): 
        return redirect("/thankyou")
    else:
        try:
           return helper(num)   
        except:
            session['question_num'] = 1000000
            return redirect("/thankyou")        
        
# From a submitted response, go to answer and append response. Then, redirect to next question        
@app.route("/answer")
def add_response():
    data=list(request.args.items())
    session["responses"].append(data[0][0])
    session['question_num'] +=1
    return redirect("/questions/" + str(session['question_num']))

@app.route("/thankyou")
def show_thanks():
    return render_template("thankyou.html")

