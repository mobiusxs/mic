from flask import Blueprint, render_template

from mic.auth.decorators import authentication_required

dashboard = Blueprint('dashboard', __name__, template_folder='../templates')


@dashboard.route('/')
@authentication_required
def index():
    return render_template('dashboard/index.html')
