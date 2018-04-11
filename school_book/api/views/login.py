from school_book.api.model.model.user import User
from school_book.api.model.model.user import Role
from flask import jsonify
from school_book.api.model.serializers.serializer import UsersSerializer
from school_book.api.views.messages.error_messages import login_error
from school_book.api.views.messages.messages import successfully_logged
from school_book.api.views.helper.helper import security_token
from school_book.api.views.constants.constants import STUDENT
from school_book.api.model.providers.user import UserProvider
from school_book.api.views.helper.helper import error_handler
from school_book.api.views.helper.helper import ok_response
from school_book.api.views.helper.helper import now
from school_book.api.config import db


def login(username, password):

    user = UserProvider.get_user_by_username(username)

    print(UsersSerializer(many=False).dump(user).data)

    if user and password == user.password:

        user.last_login = now()
        db.session.commit()

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'user': UsersSerializer(many=False).dump(user).data,
                'msg': successfully_logged(user.first_name, user.last_name),
                'token': security_token(user.email, user.role.role_name) if user.role.role_name != STUDENT else
                security_token(user.unique_ID, user.role.role_name)
            }
        )

    else:
        return error_handler(error_status=403,
                             message=login_error(user.role.role_name if user else None))
