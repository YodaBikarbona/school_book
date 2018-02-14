from flask import jsonify
from school_book.api.views.messages.error_messages import WRONG_TOKEN
from school_book.api.views.helper.helper import check_security_token
from school_book.api.model.providers.user import UserProvider
from school_book.api.model.serializers.serializer import UsersSerializer
from school_book.api.model.serializers.serializer import RoleSerializer
from school_book.api.views.messages.error_messages import NO_PERMISSION
from school_book.api.views.helper.helper import error_handler
from school_book.api.views.helper.helper import date_format_to_string


def get_all_users_func(security_token, role_name):
    authorization = check_security_token(security_token)

    if authorization is False:

        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    user_list = UserProvider.get_all_users(role=authorization['role'], user_id=user.id, role_name=role_name)

    return jsonify(
        {
            "user_list": UsersSerializer(many=True).dump(user_list).data
        }
    )


def get_all_roles_func(security_token):
    authorization = check_security_token(security_token)

    if authorization is False:

        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    role_list = UserProvider.get_all_roles()

    return jsonify(
        {
            "role_list": RoleSerializer(many=True).dump(role_list).data
        }
    )


def get_user_by_user_id(security_token, user_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    user = UserProvider.get_user_by_id(role=authorization['role'], user_id=user_id)

    user_obj = UsersSerializer(many=False).dump(user).data
    user_obj['last_login'] = date_format_to_string(user_obj['last_login'])
    user_obj['first_login'] = date_format_to_string(user_obj['first_login'])
    user_obj['created'] = date_format_to_string(user_obj['created'])

    return jsonify(
        {
            'user_object': user_obj
        }
    )
