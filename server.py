import flask

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 4789

host = DEFAULT_HOST
port = DEFAULT_PORT

app = flask.Flask(__name__)



if __name__ == "__main__":
    app.run(host, port)