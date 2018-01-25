from flask_cors import CORS
from flask import jsonify
from school_book.api.config import app
from school_book.config import main
from school_book.config import init_db
from school_book.api.views.login import login
from school_book.api.views.user import get_all_users_func
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
    log.debug(u"login_endpoint/POST {0}, {1}".format(
        request.json['username'],
        request.json['password']
    ))
    user = login(request.json['username'], request.json['password'])

    return user


@app.route('/users/<string:role_name>', methods=['GET'])
def get_all_users(role_name):
    user_list = get_all_users_func(request.headers['Authorization'], role_name)

    return user_list


init_db()
if __name__ == '__main__':
    app.run(debug=True, port=8080)
