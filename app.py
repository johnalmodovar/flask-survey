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


    #TODO: 6. set session["responses"] = []

    survey_title = survey.title
    survey_instructions = survey.instructions

    #Refactor: send JUST the survey, rather than splitting it here.
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
    # print(f"\n \n This is num : {num} \n \n")


    #DONE: check responses length to account for 'skipping ahead'
    #DONE: if responses are 'done', just send ahead

    if len(responses) < num:
        return redirect(f'/questions/{len(responses)}')
    elif len(responses) == survey.questions:
        return redirect("/answer")

    return render_template("question.html",
                           question = survey.questions[num])


@app.post("/answer")
def submit_questions():
    """Submit survey response, load next question."""

    #curr_answer = request.form["answer"]
    curr_answer = request.form.get("answer") #should return None rather than an error.

    if curr_answer:
        responses.append(curr_answer)

        # print(f"\n \n \n response list: {responses} \n \n \n")
        if len(responses) >= len(survey.questions):
            return redirect("/completed")
        else:
            return redirect(f"/questions/{len(responses)}")
    else:
        return render_template("question.html",
                           question = survey.questions[len(responses)],
                           error = "Need to choose something!")




@app.get('/completed')
def show_survey_finish():
    """Provide a bulleted list of question + response"""

    return render_template('completion.html',
                           answers = responses,
                           questions = survey.questions)
