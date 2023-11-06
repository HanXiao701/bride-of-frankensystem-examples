import datetime
from flask import Blueprint, render_template
from BOFS.util import *
from BOFS.globals import db
from BOFS.admin.util import verify_admin

# The name of this variable must match the folder's name.
my_blueprint = Blueprint('my_blueprint', __name__,
                         static_url_path='/my_blueprint',
                         template_folder='templates',
                         static_folder='static')


@my_blueprint.route("/task", methods=['POST', 'GET'])
@verify_correct_page
@verify_session_valid
def task():
    return redirect("http://localhost:3000/study_assets/digital-stress-test-published", code=302)
    # run following redirect on the React.js app to redirect back to BOFS and proceed to questionnaire part.
    # return redirect("/redirect_next_page") 
    incorrect = True
    incorrect = None

    if request.method == 'POST':
        log = db.answers()  # This database table was defined in /advanced_example/tables/answers.json
        log.participantID = session['participantID']
        log.answer = request.form['answer']

        db.session.add(log)
        db.session.commit()

        if log.answer.lower() == "linux":
            return redirect("/redirect_next_page")
        incorrect = True

    return render_template("task.html", example="This is example text.", incorrect=incorrect)


@my_blueprint.route("/analysis")
@verify_admin
def analysis():
    results = db.session.query(
            db.Participant.participantID,
            db.func.count(db.MyTable.ID).label('tries')
        ).\
        join(db.MyTable, db.MyTable.participantID == db.Participant.participantID).\
        filter(db.Participant.finished).\
        group_by(db.MyTable.participantID)

    return render_template("templates/analysis.html", results=results)
