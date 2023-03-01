import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# @app.route('/')
# def index():
#     return 'hello flask'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8070, debug=True)
    # app.run(host="127.0.0.1", port=5000, debug=True)
