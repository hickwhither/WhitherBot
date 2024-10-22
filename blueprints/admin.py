from flask import *
from flask_login import *
import markdown, markupsafe
import os, json, dotenv

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/secret/<password>', methods=['GET', 'POST'])
def secret_edit(password):
    if password != current_app.password: return redirect(url_for('views.home'))

    if request.method == 'POST':
        if request.form.get('content'):
            data = json.loads(request.form.get('content'))
            with open('.secret.json', 'w', encoding='utf-8') as file:
                json.dump(data, file)
        return redirect(url_for('admin.secret_edit'))
    else:
        try:
            with open('.secret.json', 'r', encoding='utf-8') as file:
                secret_data = json.load(file)
        except: secret_data = {}
        return render_template('admin/secret.html', secret_data=json.dumps(secret_data, indent=4))