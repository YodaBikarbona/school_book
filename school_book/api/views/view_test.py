from flask_cors import CORS
from flask import jsonify
from school_book.api.config import app
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/get_status', methods=['GET'])
def get_status_list():
    variable = 'hello Yoda!'
    return jsonify({"type_list": variable})


if __name__ == '__main__':
    app.run(debug=True, port=8080)