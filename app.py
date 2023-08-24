from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def start_survey():
    """Displays survey start page"""
    # need title and instructions
    session["responses"] = []
    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)


@app.get("/questions/<int:question_number>")
def show_question(question_number):
    """Displays current survey question"""

    if question_number is not len(session["responses"]):
        return redirect(f"/questions/{len(session['responses'])}")
    elif len(session["responses"]) >= len(survey.questions):
        return redirect("/thank-you")

    return render_template("question.html",
                           question_number=question_number,
                           question=survey.questions[question_number])


@app.post("/answer/<int:question_number>")
def handle_answer(question_number):
    """Processes question answer and redirects to next question"""

    answers = session["responses"]
    answers.append(request.form["answer"])
    session["responses"] = answers

    if question_number + 1 >= len(survey.questions):
        return redirect("/thank-you")

    return redirect(f"/questions/{question_number + 1}")


@app.get("/thank-you")
def show_thankyou():
    """Shows thank you page"""

    return render_template("completion.html",
                           responses=session["responses"],
                           questions=survey.questions)
