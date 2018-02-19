from flask import request
from flask import jsonify
from school_book.api.config import db
from school_book.api.model.model.school import SchoolYear
from school_book.api.views.helper.helper import check_security_token
from school_book.api.views.messages import messages
from school_book.api.views.messages import error_messages
from school_book.api.views.helper.helper import error_handler
from school_book.api.model.providers.user import UserProvider
from school_book.api.views.constants.constants import ADMIN
from school_book.api.views.constants.constants import PROFESSOR
from school_book.api.views.constants.constants import STUDENT
from school_book.api.model.providers.school import SchoolProvider
from school_book.api.views.helper.helper import now
from school_book.api.model.serializers.serializer import SchoolYearSerializer


def add_school_year_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if request.json['start'] and request.json['end']:
            check_school_year = SchoolProvider.get_school_year(start=request.json['start'], end=request.json['end'])

            if check_school_year:
                return error_handler(error_status=400, message=error_messages.SCHOOL_YEAR_ALREADY_EXIST)

            new_school_year = SchoolYear()
            new_school_year.start = int(request.json['start'])
            new_school_year.end = int(request.json['end'])
            db.session.add(new_school_year)
            db.session.commit()

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_YEAR_SUCCESSFULLY_ADDED,
                    'school_year_obj': SchoolYearSerializer(many=False).dump(new_school_year).data
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_all_school_years_func(security_token):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    school_year_list = SchoolProvider.get_all_school_years()

    return jsonify(
        {
            'status': 'OK',
            'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': 200,
            'school_year_list': SchoolYearSerializer(many=True).dump(school_year_list).data
        }
    )
