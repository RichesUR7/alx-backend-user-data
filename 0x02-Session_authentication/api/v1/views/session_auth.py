#!/usr/bin/env python3
"""Flask view that handles all routes for the Session authentication."""

from os import getenv
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """Handles the POST request for the '/auth_session/login' route."""
    email = request.form.get('email')
    password = request.form.get('password')

    for field, value in {"email": email, "password": password}.items():
        if not value:
            return jsonify({"error": f"{field} missing"}), 400

    curr_user = User.search({"email": email})
    if not curr_user or curr_user == []:
        return jsonify({"error": "no user found for this email"}), 404

    if curr_user[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(curr_user[0].id)
        response = jsonify(curr_user[0].to_json())
        session_name = getenv('SESSION_NAME')
        response.set_cookie(session_name, session_id)
        return response
    else:
        return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """Handle user logout, Destroy the session."""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
