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
from school_book.api.model.serializers.serializer import SchoolClassSerializer
from school_book.api.model.serializers.serializer import SchoolClassStudentSerializer
from school_book.api.model.serializers.serializer import SchoolSubjectSerializer
from school_book.api.model.model.school import SchoolSubject
from school_book.api.model.serializers.serializer import SchoolClassProfessorSerializer
from school_book.api.model.model.school import SchoolClassProfessor
from school_book.api.model.serializers.serializer import UsersSerializer
from school_book.api.model.model.school import SchoolClass
from school_book.api.model.model.school import SchoolClassStudent
from school_book.api.model.model.school import SchoolClassSubject
from school_book.api.model.model.school import Absence
from school_book.api.views.helper.helper import calendar_time_only_date
from school_book.api.model.serializers.serializer import AbsenceSerializer
from datetime import datetime, timedelta
from school_book.api.views.helper.helper import calendar_date_and_time
from school_book.api.model.serializers.serializer import GradeSerializer


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

    if user.role.role_name not in [ADMIN, PROFESSOR]:
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


def get_classes_func(security_token, school_year_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name not in [ADMIN, PROFESSOR]:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if school_year_id:
            if user.role.role_name == ADMIN:
                school_class_list = SchoolProvider.get_all_classes_by_school_year_id(school_year_id=school_year_id)
            else:
                school_class_list = SchoolProvider.get_all_classes_by_school_year_id(school_year_id=school_year_id,
                                                                                     role_id=user.role_id)
            school_class_list = SchoolClassSerializer(many=True).dump(school_class_list).data
            if school_class_list:
                for school_class in school_class_list:
                    school_class["number_of_students"] = SchoolProvider.get_number_of_students(school_class["id"])
                    school_class["students"] = UsersSerializer(many=True)\
                        .dump(SchoolProvider.get_all_students_by_class_id(school_class["id"])).data
                    school_class['professor'] = UsersSerializer(many=False)\
                        .dump(SchoolProvider.get_professor_by_class_id(school_class["id"])).data

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'school_class_list': school_class_list
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def add_subjects_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if request.json['name'] and request.json['user_id']:
            new_subject = SchoolSubject()
            new_subject.name = request.json['name']
            new_subject.professor_id = request.json['user_id']
            db.session.add(new_subject)
            db.session.commit()
            professor = '{0} {1}'.format(new_subject.user.first_name, new_subject.user.last_name)
            school_subject_obj = SchoolSubjectSerializer(many=False).dump(new_subject).data
            school_subject_obj['professor'] = professor

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_SUBJECT_SUCCESSFULLY_ADDED,
                    'school_subject_obj': school_subject_obj
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_subjects_func(security_token):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    school_subject_list = SchoolProvider.get_all_school_subjects()

    return jsonify(
        {
            'status': 'OK',
            'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': 200,
            'school_subject_list': SchoolSubjectSerializer(many=True).dump(school_subject_list).data
        }
    )


def add_class_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if request.json['name'] and request.json['user_id'] and \
                request.json['school_year_id'] and request.json['multiple_professors']:
            new_class = SchoolClass()
            new_class.name = request.json['name']
            new_class.school_year_id = request.json['school_year_id']
            db.session.add(new_class)
            db.session.commit()
            new_professor_class = SchoolClassProfessor()
            new_professor_class.classes_id = new_class.id
            new_professor_class.professor_id = request.json['user_id']
            new_professor_class.multiple_professors = request.json['multiple_professors']
            db.session.add(new_professor_class)
            db.session.commit()

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_CLASS_SUCCESSFULLY_ADDED,
                    'school_class_obj': SchoolClassSerializer(many=False).dump(new_class).data
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def add_student_to_class_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if request.json['student_list'] and request.json['class_id']:
            students_ids = SchoolProvider.get_student_ids_by_class_id(request.json['class_id'])
            for student_id in request.json['student_list']:
                if student_id not in students_ids:
                    new_student_class = SchoolClassStudent()
                    new_student_class.student_id = student_id
                    new_student_class.classes_id = request.json['class_id']
                    db.session.add(new_student_class)
                    db.session.commit()
                else:
                    return error_handler(error_status=400, message=error_messages.STUDENT_CLASS_ERROR)
            school_class_list = SchoolProvider.get_all_students_by_class_id(request.json['class_id'])

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_CLASS_STUDENT_SUCCESSFULLY_ADDED,
                    'school_class_list': UsersSerializer(many=True).dump(school_class_list).data
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def add_subjects_to_class_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if request.json['subject_list'] and request.json['class_id']:
            subjects_ids = SchoolProvider.get_subject_ids_by_class_id(request.json['class_id'])
            for subject_id in request.json['subject_list']:
                if subject_id not in subjects_ids:
                    new_subject_class = SchoolClassSubject()
                    new_subject_class.school_subject_id = subject_id
                    new_subject_class.classes_id = request.json['class_id']
                    db.session.add(new_subject_class)
                    db.session.commit()
                else:
                    return error_handler(error_status=400, message=error_messages.SUBJECT_CLASS_ERROR)
            school_class_list = SchoolProvider.get_all_subjects_by_class_id(request.json['class_id'])

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_SUBJECT_SUCCESSFULLY_ADDED,
                    'school_class_list': SchoolSubjectSerializer(many=True).dump(school_class_list).data
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def delete_subject_from_class_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if request.json['subject_id'] and request.json['class_id']:
            subject = SchoolProvider.get_class_subject_by_id(subject_id=request.json['subject_id'], class_id=request.json['class_id'])
            if not subject:
                return error_handler(error_status=404, message=error_messages.SUBJECT_CLASS_DOES_NOT_EXIST)
            db.session.delete(subject)
            db.session.commit()
            school_class_list = SchoolProvider.get_all_subjects_by_class_id(request.json['class_id'])

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_SUBJECT_SUCCESSFULLY_DELETED,
                    'school_class_list': SchoolSubjectSerializer(many=True).dump(school_class_list).data
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_subjects_from_class_func(security_token, class_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        subjects = SchoolProvider.get_class_subjects_by_class_id(class_id=class_id)

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'school_class_list': SchoolSubjectSerializer(many=True).dump(subjects).data
            }
        )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def drop_students_from_class_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)
    try:
        if request.json['student_id'] and request.json['class_id']:
            student = SchoolProvider.get_class_student_by_id(student_id=request.json['student_id'],
                                                             class_id=request.json['class_id'])
            if not student:
                return error_handler(error_status=404, message=error_messages.STUDENT_CLASS_DOES_NOT_EXIST)
            db.session.delete(student)
            db.session.commit()
            school_class_list = SchoolProvider.get_all_students_by_class_id(request.json['class_id'])

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SCHOOL_STUDENT_SUCCESSFULLY_DELETED,
                    'school_class_list': UsersSerializer(many=True).dump(school_class_list).data
                }
            )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_students_from_class_func(security_token, class_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        students = SchoolProvider.get_all_students_by_class_id(class_id=class_id)

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'school_class_list': UsersSerializer(many=True).dump(students).data
            }
        )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_class_func(security_token, class_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != PROFESSOR:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        students = SchoolProvider.get_all_students_by_class_id(class_id=class_id)
        subjects = SchoolProvider.get_all_subjects_by_class_id(class_id=class_id)

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'school_class_student_list': UsersSerializer(many=True).dump(students).data,
                'school_class_subject_list': SchoolSubjectSerializer(many=True).dump(subjects).data
            }
        )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_absences_func(security_token, class_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != PROFESSOR:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        if not request.json['date']:
            return error_handler(error_status=400, message=error_messages.BAD_REQUEST)
        date = calendar_time_only_date(request.json['date'])
        limit_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=2)
        limit_date = limit_date.isoformat()
        date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        date = date.isoformat()
        absences = SchoolProvider.get_all_absences(class_id=class_id, date=date, limit_date=limit_date)
        absences = AbsenceSerializer(many=True).dump(absences).data
        for absence in absences:
            student = UserProvider.get_user_by_id(absence['student_id'])
            student = UsersSerializer(many=False).dump(student).data
            absence['student'] = student
            absence['date'], absence['time'] = calendar_date_and_time(absence['date'])

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'absence_list': absences
            }
        )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def add_absences_func(security_token, class_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != PROFESSOR:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        #import pdb;pdb.set_trace()
        if not request.json['student_id']:
            return error_handler(error_status=400, message=error_messages.BAD_REQUEST)
        new_absence = Absence()
        new_absence.class_id = class_id
        new_absence.comment = request.json['comment'] if request.json['comment'] else None
        new_absence.professor_id = user.id
        new_absence.student_id = request.json['student_id']
        new_absence.date = datetime.now()
        school_subject = SchoolProvider.get_class_subject_by_class_id_and_professor_id(class_id=class_id,
                                                                                       professor_id=user.id)
        new_absence.school_subject_id = school_subject.school_subject_id
        db.session.add(new_absence)
        db.session.commit()

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'msg': messages.ABSENCE_SUCCESSFULLY_ADDED
            }
        )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def get_student_grades_func(security_token, class_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != PROFESSOR:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    try:
        student_class_details = {}
        #import pdb;pdb.set_trace()
        if not request.json['student_id']:
            return error_handler(error_status=400, message=error_messages.BAD_REQUEST)
        student = UserProvider.get_user_by_id(request.json['student_id'])
        if not student:
            return error_handler(error_status=404, message=error_messages.USER_DOES_NOT_EXIST)
        student_class_details['student'] = UsersSerializer(many=False).dump(student).data
        school_subjects = SchoolProvider.get_all_subjects_by_class_id(class_id=class_id)
        student_class_details['school_subjects'] = SchoolSubjectSerializer(many=True).dump(school_subjects).data
        for school_subject in student_class_details['school_subjects']:
            grades = SchoolProvider.get_student_grades(class_id=class_id,
                                                       school_subject_id=school_subject['id'],
                                                       student_id=student.id)
            school_subject['grades'] = GradeSerializer(many=True).dump(grades).data
            for grade in school_subject['grades']:
                grade['date'], grade['time'] = calendar_date_and_time(grade['date'])
            average_grade = 1
            if len(grades) > 0:
                for grade in grades:
                    average_grade += grade.grade
                average_grade = round((float(average_grade - 1)/len(grades)), 1)
                print(average_grade)
            school_subject['average_grade'] = average_grade

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'student_class_details': student_class_details
            }
        )
    except Exception as ex:
        print(ex)
        return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


