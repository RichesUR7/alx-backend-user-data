#!/usr/bin/env python3
"""Module contains flask application"""

from auth import Auth
from flask import Flask, abort, jsonify, redirect, request


AUTH = Auth()
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/", methods=["GET"])
def index():
    """
    The index route which returns a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    The users route which handles user registration.
    It expects 'email' and 'password' in the form data.
    """
    email = request.form["email"]
    password = request.form["password"]

    if not email or not password:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 200


@app.route("/sessions", methods=["POST"])
def login():
    """
    The sessions route which handles user login.
    It expects 'email' and 'password' in the form data.
    """
    email = request.form["email"]
    password = request.form["password"]

    # if not email or not password:
    #     abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    The sessions route which handles user logout.
    It expects a 'session_id' cookie.
    """
    session_id = request.cookies.get("session_id", None)

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """
    The profile route which returns the user's profile.
    It expects a 'session_id' cookie.
    """
    session_id = request.cookies.get("session_id", None)

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """
    The reset_password route which handles password reset requests.
    It expects 'email' in the form data.
    """
    email = request.form["email"]
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    The update_password route which handles password updates.
    It expects 'email', 'reset_token', and 'new_password' in the form data.
    """
    import uuid

    email = request.form["email"]
    reset_token = request.form["reset_token"]
    new_pwd = request.form["new_password"]

    # if not email or not reset_token or not new_pwd:
    #     abort(403)

    try:
        uuid.UUID(reset_token)
        AUTH.update_password(reset_token, new_pwd)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
