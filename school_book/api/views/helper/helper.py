from hashlib import sha512
from random import choice
from jose import jwt
from school_book.api.views.constants.constants import BACKEND_SECRET_WORD


def new_salt():
    source = [chr(x) for x in range(32, 127)]
    salt = u''.join(choice(source) for x in range(0, 32))

    return salt


def new_psw(salt, password):
    password = str(sha512(u'{0}{1}'.format(password, salt)
                          .encode('utf-8', 'ignore')).hexdigest())

    return password


def check_psw(psw, salt, password):
    password = new_psw(salt=salt, password=password)
    if '{0}'.format(psw) == '{0}'.format(password):
        return True
    else:
        return False


def security_token(username, role_name):
    signed = jwt.encode(
        {'userName': '{0}'.format(username),
         'role': '{0}'.format(role_name)
         }, BACKEND_SECRET_WORD, algorithm='HS256')

    return signed


def check_security_token(token):
    try:
        decode = jwt.decode(token, BACKEND_SECRET_WORD, algorithms='HS256')
    except Exception as ex:
        print(ex)
        return False
    return decode
