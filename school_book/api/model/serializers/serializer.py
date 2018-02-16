from flask import Flask
from flask_marshmallow import Marshmallow


app = Flask(__name__)
ma = Marshmallow(app)


class RoleSerializer(ma.Schema):

    class Meta:
        fields = ('id', 'role_name')


class ImageSerializer(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'type', 'file_name')


class UsersSerializer(ma.Schema):
    role = ma.Nested(RoleSerializer, only=['role_name'])
    image = ma.Nested(ImageSerializer, only=['file_name'])

    class Meta:
        fields = ('id', 'unique_ID', 'first_name', 'last_name', 'email', 'parent_one',
                  'parent_two', 'activated', 'role_id', 'created', 'first_login', 'last_login',
                  'address', 'phone', 'city', 'image_id', 'gender', 'birth_date', 'role', 'image')
