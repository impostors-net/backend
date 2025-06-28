from flask import make_response

def post_next_options():
    """Handle CORS preflight for /post/next"""
    return _cors_response()

def post_uuid_options(uuid):
    """Handle CORS preflight for /post/{uuid}"""
    return _cors_response()

def post_options():
    """Handle CORS preflight for /post"""
    return _cors_response()

def user_uuid_options(uuid):
    """Handle CORS preflight for /user/{uuid}"""
    return _cors_response()

def user_handle_options(handle):
    """Handle CORS preflight for /user/{uuid}"""
    return _cors_response()

def post_comment_options(uuid):
    """Handle CORS preflight for /post/{uuid}/comment"""
    return _cors_response()

def comment_uuid_options(uuid):
    """Handle CORS preflight for /comment/{uuid}"""
    return _cors_response()

def comment_vote_options(uuid):
    """Handle CORS preflight for /comment/{uuid}/vote"""
    return _cors_response()

def auth_signup_options():
    """Handle CORS preflight for /auth/signup"""
    return _cors_response()

def _cors_response():
    """Helper function to create CORS response"""
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,displayName,handle,passwordHash'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response