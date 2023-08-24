from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def show_start_page():
    """ Generates title of survey, its instructions, and the start button """

    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions

    return render_template("survey_start.html",
                           title = survey_title,
                           instructions = survey_instructions)

@app.post("/")
def redirect_to_survey():
    """ Click the start button to redirect to survey questions """

    return redirect("/questions/0")

@app.get("/questions/<num>")
def load_questions():
    """ Load questions from the survey """

    survey_question = satisfaction_survey.questions["num"]




responses = []