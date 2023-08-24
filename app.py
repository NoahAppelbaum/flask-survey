from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def start_survey():
    # need title and instructions
    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)


@app.post("/questions/<question_number>")
def show_question(question_number):
    return render_template("question.html",
                           question_number=int(question_number),
                           question=survey.questions[int(question_number)])
