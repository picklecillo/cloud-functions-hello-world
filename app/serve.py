from flask import Flask
from flask import request

from function.main import hello_world


app = Flask(__name__)


@app.route('/hello_world')
def hello():
    return hello_world(request)


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
