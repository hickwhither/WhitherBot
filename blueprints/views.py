from flask import *
from flask_login import *
import markdown, markupsafe

bp = Blueprint('views', __name__, url_prefix='/')

@bp.app_errorhandler(404)
def _404(e):
    return render_template("404.html", err='hello em')

@bp.route('/')
def home():
    latency = round(current_app.bot.latency * 1000)
    uptime = int(current_app.bot.start_time)
    return render_template('index.html', latency=latency, uptime=uptime)

# @bp.route('/u/')
# @bp.route('/u/<string:username>')
# def user(username=None):
#     user: User
#     if username: user = User.query.filter_by(username=username).first()
#     else: user = current_user
#     about = markdown.markdown(markupsafe.escape(user.about)) if user else ''
#     return render_template('user/profile.html', user=user, about=about)

# @bp.route('/edit_profile', methods=['GET', 'POST'])
# def edit_profile():
#     if not current_user.is_active: return redirect(url_for('auth.login'))
    
#     if request.method == 'POST':
#         avatar = request.form.get('avatar')
#         about = request.form.get('about')
#         current_user.avatar = avatar
#         current_user.about = about
#         db.session.commit()
#         return redirect(url_for('views.user'))

#     return render_template("user/edit_profile.html")

# request.data Contains the incoming request data as string in case it came with a mimetype Flask does not handle.
# request.args: the key/value pairs in the URL query string
# request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded
# request.files: the files in the body, which Flask keeps separate from form. HTML forms must use enctype=multipart/form-data or files will not be uploaded.
# request.values: combined args and form, preferring args if keys overlap
# request.json: parsed JSON data. The request must have the application/json content type, or use request.get_json(force=True) to ignore the content type.

# @bp.route('/standing')
# def standing():
#     standing = User.query.all()
#     standing.sort(key=lambda x: x.points, reverse=True)
#     return render_template("user/standing.html", standing=standing)


# @bp.before_app_request
# def bar():
#     User.query.filter(User.points<1, time.time()-User.created>180).delete()
#     db.session.commit()
