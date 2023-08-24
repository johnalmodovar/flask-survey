from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
#from surveys import satisfaction_survey as survey
from surveys import surveys as survey_list

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# session = []

surveys = {"satisfaction": satisfaction_survey,
"personality" : personality_quiz
}

#FIXME: we had a mistake in trying to jsonify a class instance
#the PROPER way to do this is have the class spit out a JSON object
#the current janky fix is to hard code it, and have survey_choice target surveys

#FIXME: every survey["choice"] should be switched back to survey.

@app.get("/")
def show_select_page():
    """ Generates title of survey, its instructions, and the start button """

    #send in survey_list here (so that we can access keys)

    return render_template("survey_select.html",
                           options = survey_list.keys())


@app.post("/start")
def show_start_page():
    """ Generates title of survey, its instructions, and the start button """

    #send in survey_list here (so that we can access keys)
    survey_choice = request.form["survey"]
    session["survey"] = survey_list[survey_choice]
    breakpoint()

    print(f"\n\n\n session survey is: {session['survey']} \n\n\n")
    # breakpoint()
    return render_template("survey_start.html",
                            survey = jsonify(session["survey"]) )


@app.post("/begin")
def redirect_to_survey():
    """ Click the start button to redirect to survey questions,
    initialize session responses"""

    #set survey on session["survey"] ??
    #curr_survey = request.form[]
    session["responses"] = []

    return redirect("/questions/0")


@app.get("/questions/<int:num>")
def load_questions(num):
    """ Load questions from the survey """

    # self.prompt = prompt
    # self.choices = choices
    # self.allow_text = allow_text
    # print(f"\n \n This is num : {num} \n \n")

    if isinstance(session.get("responses"), list):
        if len(session["responses"]) < num:
            flash("Please don't skip around questions")
            return redirect(f'/questions/{len(session["responses"])}')
        elif len(session["responses"]) == session["survey"].questions:
            return redirect("/completed")

        return render_template("question.html",
                            question = session["survey"].questions[num])
    else:
        flash("click the start button! don't skip")
        return redirect('/')


@app.post("/answer")
def submit_questions():
    """Submit survey response, load next question."""

    #curr_answer = request.form["answer"]
    curr_answer = request.form.get("answer") #should return None rather than an error.

    if curr_answer:
        responses = session["responses"]
        responses.append(curr_answer)
        session["responses"] = responses

        # print(f"\n \n \n response list: {responses} \n \n \n")
        if len(session["responses"]) >= len(session["survey"].questions):
            return redirect("/completed")
        else:
            return redirect(f"/questions/{len(session['responses'])}")
    else:
        return render_template("question.html",
                           question = session["survey"].questions[len(session["responses"])],
                           error = "Need to choose something!")




@app.get('/completed')
def show_survey_finish():
    """Provide a bulleted list of question + response"""

    return render_template('completion.html',
                           answers = session["responses"],
                           questions = session["survey"].questions)
