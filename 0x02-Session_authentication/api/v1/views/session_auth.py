#!/usr/bin/env python3
"""
New view for Session Authentication
"""
from flask import request, jsonify, make_response, abort
import os
from api.v1.views import app_views
from models.base import DATA
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Auntheticates a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    if len(DATA) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    users_list = User.search({'email': email})
    if len(users_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users_list[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Log out a user.
    """
    from api.v1.app import auth
    session_destroyed = auth.destroy_session(request)
    if not session_destroyed:
        abort(404)
    return jsonify({}), 200
