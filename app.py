from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
#surveys = {"satisfaction: satisfaction_survey",
# "personality" : personality_quiz
# }


@app.get("/")
def show_start_page():
    """ Generates title of survey, its instructions, and the start button """

    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template("survey_start.html",
                           title = survey_title,
                           instructions = survey_instructions)

@app.post("/begin")
def redirect_to_survey():
    """ Click the start button to redirect to survey questions """

    return redirect("/questions/0")

@app.get("/questions/<int:num>")
def load_questions(num):
    """ Load questions from the survey """

    # self.prompt = prompt
    # self.choices = choices
    # self.allow_text = allow_text
    print(f"\n \n This is num : {num} \n \n")

    survey_question = survey.questions[num]

    return render_template("question.html",
                           prompt = survey_question.prompt,
                           choices = survey_question.choices,
                           allow_text = survey_question.allow_text)



@app.post("/questions/<num>")
def submit_questions():
    """Submit survey response, load next question."""

    curr_answer = request.form["answer"]
    responses.append(curr_answer)
    redirect("/answer")


@app.get('/answer')
def receive_answer():
    """When submitting an answer, grab from request.form, append to response,
    then send them to the next question."""

    if len(responses) >= len(survey.questions):
        redirect_url = "/completed"
    else:
        redirect_url = f"/questions/{len(responses)}"

    redirect(redirect_url)


@app.get('/completed')
def show_survey_finish():
    """Provide a bulleted list of question + response"""

    return render_template('completion.html',
                           questions= survey.questions, #actually want prompt
                           answers = responses)