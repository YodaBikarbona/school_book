from school_book.api.views.constants.constants import ADMIN
from school_book.api.views.constants.constants import STUDENT
from school_book.api.views.constants.constants import PROFESSOR


NO_PERMISSION = "You don\'t have permission!"


def login_error(role):
    if role == ADMIN or role == PROFESSOR:
        LOGIN_ERROR = "Password is wrong!"
    else:
        LOGIN_ERROR = "Password or username is wrong!"

    return LOGIN_ERROR


WRONG_TOKEN = "Security token is wrong!"
USER_ALREADY_EXISTS = "User with that email already exists!"
USER_DOES_NOT_EXIST = "That user does not exist!"
SCHOOL_YEAR_ALREADY_EXIST = "That school year already exist!"
BAD_REQUEST = "Data is wrong!"
