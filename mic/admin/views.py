from flask import Blueprint, flash, render_template, request

from mic.admin.forms import AdminForm
from mic.admin.models import Admin
from mic.extensions import db

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates')

# TODO: views: add admin :by name:, whitelist :by id:, add/delete/modify fits, add/delete structures

ids = []
fits = []
structs = []


@admin.route('/', methods=['GET', 'POST'])
def index():
    form = AdminForm()
    if form.validate_on_submit():
        record = Admin(character_id=form.data["character_id"])
        db.session.add(record)
        db.session.commit()
        flash(f'{form.data["character_id"]} added as admin')
        admins = Admin.query.all()
        return render_template('admin/index.html', form=form, admins=admins)
    admins = Admin.query.all()
    return render_template('admin/index.html', form=form, admins=admins)


@admin.route('/whitelist', methods=['GET', 'POST'])
def whitelist():
    if request.method == 'GET':
        return render_template('admin/whitelist.html', ids=ids)
    else:
        new_id = request.form.get('whitelist-id')
        ids.append(new_id)
        flash(f'{new_id} added to whitelist')
        return render_template('admin/whitelist.html', ids=ids)


@admin.route('/fits')
def fits():
    return render_template('admin/fits.html')


@admin.route('/structures')
def structures():
    if request.method == 'GET':
        return render_template('admin/structures.html')
    else:
        new_id = request.form.get('structure-id')
        structs.append(new_id)
        flash(f'{new_id} added as new market')
        return render_template('admin/structures.html', structures=structs)
