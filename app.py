from flask import Flask, request, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
question_num = 0

def helper(num):
    title = surveys.get("satisfaction").title
    question = surveys.get("satisfaction").questions[int(num)]
    return render_template("questions.html", num=num, title=title, question=question.question, choices= question.choices)

@app.route("/")
def home():
    survey = surveys.get("satisfaction")
    return render_template("home.html", title=survey.title, instructions=survey.instructions)

@app.route("/", methods=["POST"])
def submit():
    if question_num >= len(surveys.get("satisfaction").questions):
        flash("Thank you for your response.")
        redirect("/thankyou")
    else:
        redirect("/questions" + int(question_num))


# Display first question after posting from root
@app.route("/questions/<num>", methods=["POST"])
def get_question(num):
        if question_num >= len(surveys.get("satisfaction").questions):
            flash("Thank you for your response.")
            return redirect("/thankyou")
        # question_num = int(num)+1
        else:
            return helper(question_num)

# From a submitted response, go to answer and append response. Then, redirect to next question        
@app.route("/answer", methods=["POST"])
def add_response():
    global responses
    data=request.form
    for key in data.items():
        responses.append(key)
    global question_num
    # Now that the response is appended, increase question_num by 1. This means that after the first question, question_num should be 1 for the second question
    question_num = question_num+1
    return redirect("/questions/" + str(question_num))

# 
@app.route("/questions/<num>")
def next_question(num):
    global question_num
    if question_num < int(num):
        flash("Please complete questions in order. ")
        return redirect("/questions/" + str(question_num))
    # If question_num exceeds number of questions, redirect to thank you
    elif question_num > len(surveys.get("satisfaction").questions): 
        return redirect("/thankyou")
    else:
        try:
           return helper(num)   
        except:
            global responses
            question_num = 1000000
            return redirect("/thankyou")        
@app.route("/thankyou")
def show_thanks():
    return render_template("thankyou.html")

# @app.route("/questions/<int:num>")
# def show_question(num):
    # try:
    #     title = surveys.get("satisfaction").title
    #     question = surveys.get("satisfaction").questions[num].question
    #     return render_template("questions.html", num=num, title=title, question=question)
    # except IndexError:
    #     raise

# @app.route("/answer", methods=["POST"])
# def redr():
#     responses.append(request)
#     print(responses)
#     return "WOW!!"

# @app.route("/answer", methods=["POST"])
# def add_answer():
#     print(request)
#     print("THIS IS A REUQUEST")
#     responses.append(request)
#     return render_template("answer.html")