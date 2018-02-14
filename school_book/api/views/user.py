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


def upload_image(request):
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        new_image = Image()
        new_image.type = img_name.split('.')[1]
        new_image.name = img_name
        new_image.file_name = img_name
        db.session.add(new_image)
        db.session.commit()
        return ('Saved')
        #return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:
    	return "Where is the image?"
