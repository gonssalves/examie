from flask import Blueprint, render_template

error = Blueprint('error', __name__)

#custom page for client-side error
@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#custom page for server-side error
@error.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500