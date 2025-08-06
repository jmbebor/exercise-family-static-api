"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

member1 = {
    "first_name": "Jhon",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

member2={
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

member3={
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(member1)
jackson_family.add_member(member2)
jackson_family.add_member(member3)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"family": members}
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404
    

@app.route('/member', methods=['POST'])
def add_member():
    member = request.json

    if not member:
        return jsonify({"error": "Request body is required"}), 400

    if 'first_name' not in member or 'age' not in member or 'lucky_numbers' not in member:
        return jsonify({"error": "Some key fields are missing"}), 400

    jackson_family.add_member(member)
    return jsonify({"message": "Member added"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member=jackson_family.get_member(id)

    if member:
        jackson_family.delete_member(id)
        return jsonify({"message": f"Member {member['first_name']} deleted"}), 200
    else:
        return jsonify({"error": f"Member {id} not found"}), 404



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
