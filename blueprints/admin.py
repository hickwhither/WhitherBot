from flask import *
from flask_login import *
import markdown, markupsafe
import os, json, dotenv, io

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

@bp.route('/database_upload/<password>', methods=['GET', 'POST'])
def database_upload(password):
    if password != current_app.password: return redirect(url_for('views.home'))

    if request.method == 'POST':
        print(request.files)
        print(request.form)
        if 'file' in request.files:
            file = request.files['file']
            from models import SessionLocal
            current_app.db.close()
            current_app.bot.economy_db.close()
            if file: file.save('db/economy.db')
            current_app.db = SessionLocal()
            current_app.bot.economy_db = SessionLocal()
        
        return redirect(url_for('admin.database_upload', password=password))
    else:
        return render_template('admin/database.html')

@bp.route('/database_download/<password>', methods=['GET', 'POST'])
def database_download(password):
    if password != current_app.password: return redirect(url_for('views.home'))
    
    with open('db/economy.db', 'rb') as file: file_data = file.read()
    return send_file(
        io.BytesIO(file_data),
        download_name='economy.db',
        as_attachment=True
    )