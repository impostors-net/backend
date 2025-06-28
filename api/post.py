import connexion
import flask

def next_post():
    return flask.redirect("/api/v1/post/adsads", 302)

def fetch(uuid: str):
    print(uuid)

def post():
    pass

