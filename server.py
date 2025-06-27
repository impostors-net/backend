import connexion

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 4789

host = DEFAULT_HOST
port = DEFAULT_PORT

app = connexion.App(__name__)
app.add_api("./openapi.yaml")


def run():
    app.run(host=host, port=port)


if __name__ == "__main__": run()
