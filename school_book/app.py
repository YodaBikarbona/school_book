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
import logging
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


init_db()
if __name__ == '__main__':
    app.run(debug=True, port=6543)
