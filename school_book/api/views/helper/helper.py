from hashlib import sha512
from random import choice
from jose import jwt
from school_book.api.views.constants.constants import BACKEND_SECRET_WORD
import json
import logging
from datetime import datetime
from flask import Response
import os


log = logging.getLogger(__name__)


MALE = 0
FEMALE = 1


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


def now():
    return datetime.now()


def date_format(date):
    temp_date = '{0}'.format(date).split('T')
    string = '{0} '.format(temp_date[0]) + temp_date[1].split('Z')[0]
    date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')
    return date


def birth_date_format(date):
    date = '{0} '.format(date).split('T')[0]
    return date


"""def ok_response(message, additional_data=None):
    
    #Utility for building response.
    #If response needs additional data it must be supplied as dict.

    #Example::

    #    additional_data = {
     #                  'dataname' : 'data value'
     #                  }
    
    if additional_data is None:
        additional_data = {}
    if not isinstance(additional_data, dict):
        log.error(u'Unsupported additional data: {0}'.format(additional_data))
        additional_data = {}
    status = {
        'status': 'OK',
        'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
        'code': 200,
        'message': message
    }
    status.update(additional_data)
    return status"""


def ok_response(message, additional_data=None):
    data={
        'status': 'OK',
        'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
        'code': 200,
        'message': message,
        'data': additional_data if additional_data else {}
    }
    response = Response(json.dumps(data),
                        mimetype='application/json',
                        status=200)

    return response


def error_handler(error_status, message):
    data = {
        'error': {
            'status': 'ERROR',
            'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': error_status,
            'message': message
        }
    }
    response = Response(json.dumps(data),
                        mimetype='application/json',
                        status=error_status)
    return response


def date_format_to_string(date):
    date = '{0}'.format(date).split('T')
    date = '{0} '.format(date[0]) + '{0}'.format(date[1].split('+')[0])
    return date


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


def calculate_age(born):
    born = datetime.strptime(born, "%Y-%m-%d")
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
