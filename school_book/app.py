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
from school_book.api.views.school import add_subjects_func
from school_book.api.views.school import get_subjects_func
from school_book.api.views.school import add_class_func
from school_book.api.views.school import add_student_to_class_func
from school_book.api.views.user import edit_user_func
from school_book.api.views.user import change_password_func
from school_book.api.views.school import add_subjects_to_class_func
from school_book.api.views.school import delete_subject_from_class_func
from school_book.api.views.school import get_subjects_from_class_func
from school_book.api.views.school import drop_students_from_class_func
from school_book.api.views.school import get_students_from_class_func
from school_book.api.views.school import get_class_func
from school_book.api.views.school import get_absences_func
from school_book.api.views.school import add_absences_func
from school_book.api.views.school import get_student_grades_func
from school_book.api.views.school import add_student_grades_func
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


@app.route('/upload/user/<int:user_id>', methods=['POST'])
def upload(user_id):

    return upload_image(request, user_id)


@app.route('/users/add', methods=['POST'])
def add_new_user():

    return addUser(request.headers['Authorization'], request)


@app.route('/users/edit', methods=['POST'])
def edit_user():

    return edit_user_func(request.headers['Authorization'], request)


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

    return add_subjects_func(request.headers['Authorization'], request)


@app.route('/school_subjects', methods=['GET'])
def get_school_subject():

    return get_subjects_func(request.headers['Authorization'])


@app.route('/school_class/add', methods=['POST'])
def add_class():

    return add_class_func(request.headers['Authorization'], request)


@app.route('/school_class/students/add', methods=['POST'])
def add_student_to_class():

    return add_student_to_class_func(request.headers['Authorization'], request)


@app.route('/users/change_password', methods=['POST'])
def change_password():

    return change_password_func(request.headers['Authorization'], request)


@app.route('/school_class/school_subjects/add', methods=['POST'])
def add_subjects_to_class():

    return add_subjects_to_class_func(request.headers['Authorization'], request)


@app.route('/school_class/school_subjects/drop', methods=['POST'])
def drop_subjects_from_class():

    return delete_subject_from_class_func(request.headers['Authorization'], request)


@app.route('/school_class/school_subjects/class/<int:class_id>', methods=['GET'])
def get_subjects_from_class(class_id):

    return get_subjects_from_class_func(request.headers['Authorization'], class_id)


@app.route('/school_class/students/drop', methods=['POST'])
def drop_students_from_class():

    return drop_students_from_class_func(request.headers['Authorization'], request)


@app.route('/school_class/students/class/<int:class_id>', methods=['GET'])
def get_students_from_class(class_id):

    return get_students_from_class_func(request.headers['Authorization'], class_id)


@app.route('/school_class/class/<int:class_id>', methods=['GET'])
def get_class(class_id):

    return get_class_func(request.headers['Authorization'], class_id)


@app.route('/absence/class/<int:class_id>', methods=['POST'])
def get_absence(class_id):

    return get_absences_func(request.headers['Authorization'], class_id)


@app.route('/absence/add/class/<int:class_id>', methods=['POST'])
def add_absence(class_id):

    return add_absences_func(request.headers['Authorization'], class_id)


@app.route('/grades/class/<int:class_id>', methods=['POST'])
def get_student_grades(class_id):

    return get_student_grades_func(request.headers['Authorization'], class_id)


@app.route('/grades/add/class/<int:class_id>', methods=['POST'])
def add_student_grades(class_id):

    return add_student_grades_func(request.headers['Authorization'], class_id)


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
    #app.run(host="192.168.0.17", debug=True, port=6543)
    app.run(debug=True, port=6543)

