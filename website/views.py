from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if (request.method == 'POST') :
        note = request.form.get('note')

        if len(note) < 1:
            flash('Notes is too short', category='error')
        else :
            new_notes = Note(data=note, user_id=current_user.id)
            db.session.add(new_notes)
            db.session.commit()
            flash('Notes Added', category='success')
    return render_template("home.html", text='Testing', bool=True, user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id :
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})
