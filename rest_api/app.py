from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask REST API is running 🚀"


# In-memory "database"
users = {}

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# GET one user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# POST create user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user_id = len(users) + 1
    users[user_id] = data
    return jsonify({"id": user_id, "user": data}), 201

# PUT update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    users[user_id] = data
    return jsonify({"message": "User updated", "user": data})

# DELETE user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    deleted = users.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted})

if __name__ == "__main__":
    app.run(debug=True)
