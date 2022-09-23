from flask import Blueprint, render_template, request, flash , jsonify
from flask_login import login_required, current_user
import json
from . import db
from .models import Feedback

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/cinema', methods=['GET', 'POST'])
@login_required
def cinema():
    return render_template("cinema.html", user=current_user)


@views.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        feedback = request.form.get('feedback')

        if len(feedback) < 10:
            flash('please give us some details 😊 !!',category='error')
        else:
            new_feedback = Feedback(data=feedback,user_id=current_user.id)
            db.session.add(new_feedback)
            db.session.commit()
            flash('Thanks for the feedback !',category='success')

    return render_template("feedback.html",user=current_user)

@views.route('/delete-feedback', methods=['POST'])
def delete_feedback():
    feedback = json.loads(request.data)
    feedbackId = feedback['feedbackId']
    feedback = feedback.query.get(feedbackId)
    if feedback:
        if feedback.user_id == current_user.id:
            db.session.delete(feedback)
            db.session.commit()

    return jsonify({})
