from school_book.api.model.model.user import User
from school_book.api.model.model.user import Role
from school_book.api.views.messages.error_messages import NO_PERMISSION
from school_book.api.views.constants.constants import ADMIN
from school_book.api.views.constants.constants import PROFESSOR
from school_book.api.views.constants.constants import STUDENT


class UserProvider:

    @classmethod
    def get_user_by_username(cls, username):
        user = User.query \
            .filter(User.email == username).first()

        return user

    @classmethod
    def get_all_users(cls, role, user_id, role_name):
        if role == ADMIN or role == PROFESSOR:
            user_list = User.query\
                .join(Role, User.role_id == Role.id)
            if role == ADMIN:
                user_list = user_list\
                    .filter(User.id != user_id,
                            Role.role_name == role_name)
            if role == PROFESSOR:
                user_list = user_list\
                    .filter(Role.role_name == STUDENT)
        else:
            return NO_PERMISSION
        return user_list.all()

    @classmethod
    def get_all_roles(cls):
        return Role.query.all()

    @classmethod
    def get_user_by_id(cls, role, user_id):
        user_obj = User.query\
            .join(Role, User.role_id == Role.id)
        if role == ADMIN:
            user_obj = user_obj.filter(User.id == user_id)
        elif role == PROFESSOR:
            user_obj = user_obj.filter(User.id == user_id,
                                       Role.role_name == STUDENT)
        else:
            return NO_PERMISSION
        return user_obj.first()

    @classmethod
    def get_role_by_role_name(cls, role_name):
        return Role.query.filter(Role.role_name == role_name).first()
