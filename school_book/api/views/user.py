from flask import jsonify
from school_book.api.views.messages.error_messages import WRONG_TOKEN
from school_book.api.views.helper.helper import check_security_token
from school_book.api.model.providers.user import UserProvider
from school_book.api.model.serializers.serializer import UsersSerializer
from school_book.api.model.serializers.serializer import RoleSerializer
from school_book.api.views.messages.error_messages import NO_PERMISSION
from school_book.api.views.helper.helper import error_handler
from school_book.api.views.helper.helper import date_format_to_string
from school_book.api.config import PROJECT_HOME
from werkzeug.utils import secure_filename
from school_book.api.views.helper.helper import create_new_folder
from school_book.api.config import app
import os
from school_book.api.model.model.user import Image
from school_book.api.config import db
from school_book.api.views.constants.constants import ADMIN
from school_book.api.views.constants.constants import PROFESSOR
from school_book.api.views.constants.constants import STUDENT
from school_book.api.views.messages import messages
from school_book.api.views.messages import error_messages
from school_book.api.model.model.user import User
from school_book.api.model.model.user import Image
from school_book.api.model.model.user import Role
from school_book.api.views.constants.constants import MALE
from school_book.api.views.constants.constants import FEMALE
import uuid
from school_book.api.views.constants.constants import DEFAULT_IMAGE_ID
from school_book.api.views.helper.helper import now
from school_book.api.views.helper.helper import new_psw
from school_book.api.views.helper.helper import new_salt
from school_book.api.views.constants.constants import ACTIVATED
from school_book.api.views.constants.constants import DEACTIVATED
from school_book.api.views.helper.helper import date_format
from school_book.api.views.helper.helper import birth_date_format
from school_book.api.model.serializers.serializer import ImageSerializer
from school_book.api.views.helper.helper import calculate_age


def get_all_users_func(security_token, role_name):
    authorization = check_security_token(security_token)

    if authorization is False:

        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    user_list = UserProvider.get_all_users(role=authorization['role'], user_id=user.id, role_name=role_name)
    user_list = UsersSerializer(many=True).dump(user_list).data
    for user_obj in user_list:
        user_obj['last_login'] = date_format_to_string(user_obj['last_login'])
        user_obj['first_login'] = date_format_to_string(user_obj['first_login'])
        user_obj['created'] = date_format_to_string(user_obj['created'])
        user_obj['birth_date'] = birth_date_format(user_obj['birth_date'])
        user_obj['age'] = calculate_age(user_obj['birth_date'])

    return jsonify(
        {
            "user_list": user_list
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

    user = UserProvider.get_user_by_id_and_role(role=authorization['role'], user_id=user_id)

    user_obj = UsersSerializer(many=False).dump(user).data
    user_obj['last_login'] = date_format_to_string(user_obj['last_login'])
    user_obj['first_login'] = date_format_to_string(user_obj['first_login'])
    user_obj['created'] = date_format_to_string(user_obj['created'])
    user_obj['birth_date'] = birth_date_format(user_obj['birth_date'])
    user_obj['age'] = calculate_age(user_obj['birth_date'])

    return jsonify(
        {
            'user_object': user_obj
        }
    )


def addUser(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=NO_PERMISSION)

    if request.json:
        if request.json['role_name']:
            new_user = User()
            if request.json['role_name'] == ADMIN or request.json['role_name'] == PROFESSOR:
                check_existing_user = UserProvider.get_user_by_username(request.json['email'])
                if check_existing_user:
                    return error_handler(error_status=400, message=error_messages.USER_ALREADY_EXISTS)
                role = UserProvider.get_role_by_role_name(request.json['role_name'])
                new_user.role_id = role.id
                new_user.email = request.json['email']
            else:
                role = UserProvider.get_role_by_role_name(STUDENT)
                new_user.role_id = role.id
                new_user.email = ''
                new_user.unique_ID = str(uuid.uuid4().fields[-1])
                new_user.parent_one = request.json['parent_one']
                new_user.parent_two = request.json['parent_two']
            new_user.first_name = request.json['first_name']
            new_user.last_name = request.json['last_name']
            new_user.gender = MALE if int(request.json['gender']) == MALE else FEMALE
            try:
                if request.json['activated']:
                    new_user.activated = ACTIVATED
            except Exception as ex:
                print(ex)
                new_user.activated = DEACTIVATED
            try:
                city = request.json['city']
                new_user.city = city
            except Exception as ex:
                print(ex)
                new_user.city = ''
            try:
                phone = request.json['phone']
                new_user.phone = phone
            except Exception as ex:
                print(ex)
                new_user.phone = ''
            try:
                address = request.json['address']
                new_user.address = address
            except Exception as ex:
                print(ex)
                new_user.address = ''
            date = date_format(request.json['birth_date'])
            new_user.birth_date = date
            new_user.image_id = DEFAULT_IMAGE_ID
            new_user.salt = new_salt()
            new_user.password = new_psw(new_user.salt, request.json['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SUCCESSFULLY_ADDED
                }
            )

    return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def edit_user_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=NO_PERMISSION)

    if request.json:
        if request.json['role']['role_name']:
            existing_user = UserProvider.get_user_by_id(request.json['id'])
            if not existing_user:
                return error_handler(error_status=404, message=error_messages.USER_DOES_NOT_EXIST)
            if request.json['role']['role_name'] == ADMIN or request.json['role']['role_name'] == PROFESSOR:
                if existing_user.email != request.json['email']:
                    check_existing_user = UserProvider.get_user_by_username(request.json['email'])
                    if check_existing_user:
                        return error_handler(error_status=400, message=error_messages.USER_ALREADY_EXISTS)
                existing_user.email = request.json['email']
            else:
                existing_user.parent_one = request.json['parent_one']
                existing_user.parent_two = request.json['parent_two']
            existing_user.first_name = request.json['first_name']
            existing_user.last_name = request.json['last_name']
            existing_user.gender = MALE if int(request.json['gender']) == MALE else FEMALE
            try:
                if request.json['activated']:
                    existing_user.activated = ACTIVATED
            except Exception as ex:
                print(ex)
                existing_user.activated = DEACTIVATED
            try:
                city = request.json['city']
                existing_user.city = city
            except Exception as ex:
                print(ex)
                existing_user.city = ''
            try:
                phone = request.json['phone']
                existing_user.phone = phone
            except Exception as ex:
                print(ex)
                existing_user.phone = ''
            try:
                address = request.json['address']
                existing_user.address = address
            except Exception as ex:
                print(ex)
                existing_user.address = ''
            date = date_format(request.json['birth_date'])
            existing_user.birth_date = date
            existing_user.image_id = DEFAULT_IMAGE_ID
            db.session.commit()

            user_obj = UsersSerializer(many=False).dump(existing_user).data
            user_obj['last_login'] = date_format_to_string(user_obj['last_login'])
            user_obj['first_login'] = date_format_to_string(user_obj['first_login'])
            user_obj['created'] = date_format_to_string(user_obj['created'])
            user_obj['birth_date'] = birth_date_format(user_obj['birth_date'])
            user_obj['age'] = calculate_age(user_obj['birth_date'])

            return jsonify(
                {
                    'status': 'OK',
                    'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                    'code': 200,
                    'msg': messages.SUCCESSFULLY_ADDED,
                    'user_obj': user_obj
                }
            )

    return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def change_password_func(security_token, request):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=NO_PERMISSION)

    if request.json:
        existing_user = UserProvider.get_user_by_id(request.json['id'])
        if not existing_user:
            return error_handler(error_status=404, message=error_messages.USER_DOES_NOT_EXIST)
        if request.json['password'] != request.json['confirm_password']:
            return error_handler(error_status=400, message=error_messages.BAD_REQUEST)

        existing_user.salt = User.set_salt(existing_user)
        existing_user.password = request.json['password']
        existing_user.password = User.set_psw(existing_user)
        db.session.commit()

        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'msg': messages.PASSWORD_SUCCESSFULLY_CHANGED
                }
            )

    return error_handler(error_status=400, message=error_messages.BAD_REQUEST)


def activate_user_func(security_token, user_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    user = UserProvider.get_user_by_id(user_id=user_id)

    if not user:
        return error_handler(error_status=404, messages=error_messages.USER_DOES_NOT_EXIST)

    user.activated = ACTIVATED
    db.session.commit()
    user_obj = UsersSerializer(many=False).dump(user).data

    return jsonify(
        {
            'status': 'OK',
            'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': 200,
            'msg': messages.SUCCESSFULLY_ACTIVATED,
            'user_object': user_obj
        }
    )


def deactivate_user_func(security_token, user_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    user = UserProvider.get_user_by_id(user_id=user_id)

    if not user:
        return error_handler(error_status=404, messages=error_messages.USER_DOES_NOT_EXIST)

    user.activated = DEACTIVATED
    db.session.commit()
    user_obj = UsersSerializer(many=False).dump(user).data

    return jsonify(
        {
            'status': 'OK',
            'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': 200,
            'msg': messages.SUCCESSFULLY_DEACTIVATED,
            'user_object': user_obj
        }
    )


def delete_user_func(security_token, user_id):
    authorization = check_security_token(security_token)

    if authorization is False:
        return error_handler(error_status=403, message=error_messages.WRONG_TOKEN)

    user = UserProvider.get_user_by_username(username=authorization['userName'])

    if not user:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    if user.role.role_name != ADMIN:
        return error_handler(error_status=403, message=error_messages.NO_PERMISSION)

    user = UserProvider.get_user_by_id(user_id=user_id)

    if not user:
        return error_handler(error_status=404, messages=error_messages.USER_DOES_NOT_EXIST)

    db.session.delete(user)
    db.session.commit()

    return jsonify(
        {
            'status': 'OK',
            'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': 200,
            'msg': messages.SUCCESSFULLY_DELETED
        }
    )



def upload_image(request, user_id):
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['file']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['file']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        new_image = Image()
        new_image.type = img_name.split('.')[1]
        new_image.name = img_name.split('.')[0]
        new_image.file_name = img_name
        db.session.add(new_image)
        db.session.commit()
        user = UserProvider.get_user_by_id(user_id=user_id)
        user.image_id = new_image.id
        db.session.commit()
        image = ImageSerializer(many=False).dump(new_image).data
        return jsonify(
            {
                'status': 'OK',
                'server_time': now().strftime("%Y-%m-%dT%H:%M:%S"),
                'code': 200,
                'msg': messages.IMAGE_SUCCESSFULLY_ADDED,
                'image_obj': image
            }
        )
        #return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:
        return "Where is the image?"
