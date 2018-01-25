from setuptools import setup
from flask import Flask

setup(
    name='school_book',
    packages=['school_book'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)

#from flaskext.mysql import MySQL


app = Flask(__name__)
#mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Mihael0110.'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mihael0110.@localhost/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def main():
    if __name__ == '__main__':
        app.run(debug=True, port=8080)
        #conn = mysql.connect()
        #cursor = conn.cursor()
        #mysql.init_app(app)
