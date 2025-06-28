import connexion
import flask_cors

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 4789

host = DEFAULT_HOST
port = DEFAULT_PORT

def run():
    app = connexion.FlaskApp(__name__)
    app.add_api("./openapi.yaml", pythonic_params=True)
    flask_cors.CORS(app.app)
    app.run(host=host, port=port)


if __name__ == "__main__": run()
