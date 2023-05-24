from flask import Blueprint, session, request, jsonify

countdown = Blueprint('countdown', __name__)

@countdown.route('/update_countdown', methods=['POST'])
def update_countdown():
    countdown = request.json['countdown']
    session['countdown'] = countdown
    return '', 200

@countdown.before_request
def load_countdown():
    countdown = session.get('countdown')
    if countdown is not None:
        session['countdown'] = countdown

@countdown.teardown_request
def save_countdown(exception=None):
    countdown = session.get('countdown')
    if countdown is not None:
        session['countdown'] = countdown

@countdown.route('/get_countdown')
def get_countdown():
    countdown = session.get('countdown')
    return jsonify({'countdown': countdown})

@countdown.route('/remove_countdown', methods=['POST'])
def remove_countdown():
    session.pop('countdown', None)
    return '', 200
