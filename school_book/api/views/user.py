from flask import jsonify
from school_book.api.views.messages.error_messages import WRONG_TOKEN
from school_book.api.views.helper.helper import check_security_token
from school_book.api.model.providers.user import UserProvider
from school_book.api.model.serializers.serializer import UsersSerializer
from school_book.api.model.serializers.serializer import RoleSerializer
from school_book.api.views.messages.error_messages import NO_PERMISSION


def get_all_users_func(security_token, role_name):
    authorization = check_security_token(security_token)

    if authorization is False:

        return jsonify({"err_msg": WRONG_TOKEN})

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:

        return jsonify({"err_msg": NO_PERMISSION})

    user_list = UserProvider.get_all_users(role=authorization['role'], user_id=user.id, role_name=role_name)

    return jsonify(
        {
            "user_list": UsersSerializer(many=True).dump(user_list).data
        }
    )


def get_all_roles_func(security_token):
    authorization = check_security_token(security_token)

    if authorization is False:

        return jsonify({"err_msg": WRONG_TOKEN})

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:

        return jsonify({"err_msg": NO_PERMISSION})

    role_list = UserProvider.get_all_roles()

    return jsonify(
        {
            "role_list": RoleSerializer(many=True).dump(role_list).data
        }
    )
