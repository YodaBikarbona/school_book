from flask_cors import CORS
from flask import jsonify
from school_book.api.config import app
from school_book.config import main
from school_book.config import init_db
from school_book.api.views.login import login
from school_book.api.views.user import get_all_users_func
from school_book.api.views.user import get_all_roles_func
from school_book.api.views.user import get_user_by_user_id
from flask import request
from flask import url_for, send_from_directory, request
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from school_book.api.views.user import upload_image
from school_book.api.views.user import addUser
from school_book.api.views.user import activate_user_func
from school_book.api.views.user import deactivate_user_func
from school_book.api.views.user import delete_user_func
from school_book.api.views.school import get_all_school_years_func
from school_book.api.views.school import add_school_year_func
from school_book.api.views.school import get_classes_func
from school_book.api.views.school import get_subjects_func
from werkzeug.routing import Rule
import logging
import os
log = logging.getLogger(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/get_status', methods=['GET'])
def get_status_list():
    variable = 'hello Yoda!'
    return jsonify({"msg": variable})


@app.route('/login', methods=['POST'])
def login_endpoint():

    return login(request.json['username'], request.json['password'])


@app.route('/users/<string:role_name>', methods=['GET'])
def get_all_users(role_name):

    return get_all_users_func(request.headers['Authorization'], role_name)


@app.route('/roles', methods=['GET'])
def get_all_roles():

    return get_all_roles_func(request.headers['Authorization'])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    return get_user_by_user_id(request.headers['Authorization'], user_id)


@app.route('/upload', methods=['POST'])
def upload():

    return upload_image(request)


@app.route('/users/add', methods=['POST'])
def add_new_user():

    return addUser(request.headers['Authorization'], request)


@app.route('/users/activate', methods=['POST'])
def activate_user():

    return activate_user_func(request.headers['Authorization'], request.json['user_id'])


@app.route('/users/deactivate', methods=['POST'])
def deactivate_user():

    return deactivate_user_func(request.headers['Authorization'], request.json['user_id'])


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    return delete_user_func(request.headers['Authorization'], user_id)


@app.route('/school_year', methods=['GET'])
def get_school_years():

    return get_all_school_years_func(request.headers['Authorization'])


@app.route('/school_year/add', methods=['POST'])
def add_school_years():

    return add_school_year_func(request.headers['Authorization'], request)


@app.route('/school_year/<int:school_year_id>', methods=['GET'])
def get_school_classes(school_year_id):

    return get_classes_func(request.headers['Authorization'], school_year_id)


@app.route('/school_subjects/add', methods=['POST'])
def add_school_subject():

    return get_subjects_func(request.headers['Authorization'], request)


"""@app.route('/upload', methods=['POST'])
def upload_file():
    print (request.data)

    return ("aaa")
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['POST'])
def upload():
    import pdb;pdb.set_trace()
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return ('Yes')"""



init_db()
if __name__ == '__main__':
    app.run(debug=True, port=6543)
