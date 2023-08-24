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
    """Displays survey start page"""
    # need title and instructions
    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)


@app.get("/questions/<question_number>")
def show_question(question_number):
    """Displays current survey question"""

    return render_template("question.html",
                           question_number=int(question_number),
                           question=survey.questions[int(question_number)])


@app.post("/answer/<question_number>")
def handle_answer(question_number):
    """Processes question answer and redirects to next question"""

    responses.append(request.form[f"{question_number}"])
    print("responses", responses)

    if int(question_number) + 1 >= len(survey.questions):
        return redirect("/thank-you")

    return redirect(f"/questions/{int(question_number) + 1}")


@app.get("/thank-you")
def show_thankyou():
    """Shows thank you page"""

    return render_template("completion.html",
                           responses=responses,
                           questions=survey.questions)
