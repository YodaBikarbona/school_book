from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from flaskext.mysql import MySQL

app = Flask(__name__)
#mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Mihael0110.'
app.config['MYSQL_DATABASE_DB'] = 'school_book'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mihael0110.@localhost/school_book?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#def main():
#    if __name__ == '__main__':
#        app.run(debug=True, port=8080)
        #conn = mysql.connect()
        #cursor = conn.cursor()
        #mysql.init_app(app)