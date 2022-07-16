from flask import Blueprint, flash, render_template, request

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates')

# TODO: views: add admin :by name:, whitelist :by id:, add/delete/modify fits, add/delete structures

admins = []
ids = []
fits = []
structs = []


@admin.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('admin/index.html')
    else:
        new_id = request.form.get('admin-id')
        admins.append(new_id)
        flash(f'{new_id} added as admin')
        return render_template('admin/index.html', admins=admins)


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
