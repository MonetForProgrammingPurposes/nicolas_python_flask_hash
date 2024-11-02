from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Simulated database for registered users
users_db = {}

# POST endpoint to register user and store hashed password
@app.route('/sethash', methods=['POST'])
def set_hash():
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password
    return jsonify({"message": f"User {username} registered successfully with hashed password!"}), 201

# GET endpoint to retrieve hashed password for a given user
@app.route('/gethash', methods=['GET'])
def get_hash():
    username = request.args.get('username')
    if username in users_db:
        return jsonify({"username": username, "hashed_password": users_db[username]}), 200
    return jsonify({"message": "User not found!"}), 404

# GET endpoint for registration instructions
@app.route('/register', methods=['GET'])
def register():
    return jsonify({"message": "Please use POST /sethash with a username and password to register."})

# GET endpoint to verify user login by checking hashed password
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username in users_db and check_password_hash(users_db[username], password):
        return jsonify({"message": f"Welcome, {username}!"}), 200
    return jsonify({"message": "Invalid username or password!"}), 401

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5001)
