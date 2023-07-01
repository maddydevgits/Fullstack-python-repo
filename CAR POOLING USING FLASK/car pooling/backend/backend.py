from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
from json import JSONEncoder
import json
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["carpooling"]
users_collection = db["users"]
rides_collection = db["rides"]
accept_collection=db["accept"]
reject_collection=db["reject"]

class JSONEncoderWithObjectId(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

@app.route("/register", methods=["POST"])
def register():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    role = request.json["role"]

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role
    }
    users_collection.insert_one(user_data)

    return jsonify(success=True)

@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user_data = users_collection.find_one({"email": email})

    if user_data:
        if bcrypt.checkpw(password.encode("utf-8"), user_data["password"]):
            return jsonify(user_id=str(user_data["_id"]))

    return jsonify(error="Invalid email or password"), 401

@app.route("/dashboard/<user_id>")
def dashboard(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if user_data:
        return jsonify(role=user_data["role"])

    return jsonify(error="User not found"), 404

@app.route("/profile/<user_id>")
def profile(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if user_data:
        return jsonify(user=JSONEncoder().encode(user_data))

    return jsonify(error="User not found"), 404

@app.route("/submit_ride", methods=["POST"])
def submit_ride():
    user_id = request.json["user_id"]
    payment = request.json["payment"]
    duration = request.json["duration"]
    destination = request.json["destination"]
    pickup_time = request.json["pickup_time"]
    starting_point = request.json["starting_point"]

    ride_data = {
        "user_id": ObjectId(user_id),
        "payment": payment,
        "duration": duration,
        "destination": destination,
        "pickup_time": pickup_time,
        "starting_point": starting_point,
        "status":0
    }
    rides_collection.insert_one(ride_data)

    return jsonify(success=True)

@app.route('/rides')
def rides():
    rides = rides_collection.find()
    ride_data = []

    for ride in rides:
        ride_item = {
            "id": str(ride["_id"]),
            "starting_point": ride["starting_point"],
            "pickup_time": ride["pickup_time"],
            "destination": ride["destination"],
            "duration": ride["duration"],
            "payment":ride["payment"]
        }
        ride_data.append(ride_item)
    json_ride_data = json.dumps(ride_data, cls=JSONEncoderWithObjectId)
    return json_ride_data


@app.route('/accept/<id>/<id1>')
def accept(id,id1):
               document=rides_collection.find_one({"_id":ObjectId(id)})
               print(document)
               document['driverid']=id1
               if document:
                    accept_collection.insert_one(document)
                    rides_collection.delete_one({"_id": ObjectId(id)})
                    return "Document moved successfully."
               else:
                    return "Document not found in the rides collection."

 

@app.route('/reject/<id>')
def reject(id):
                document=rides_collection.find_one({"_id":ObjectId(id)})
                if document:
                     reject_collection.insert_one(document)
                     rides_collection.delete_one({"_id":ObjectId(id)})
                     return "document moved successfully"
                else:
                     return "Document not found in the rides "

@app.route('/myrides/<id>')
def myrides(id):
     query={'user_id':ObjectId(id)}
     document1=accept_collection.find(query)
     document2=rides_collection.find(query)
     ride_data = []

     for ride in document1:
        query1={'_id':ObjectId(ride['driverid'])}
        res=users_collection.find_one(query1)
        ride_item = {
            "id": str(ride["_id"]),
            "starting_point": ride["starting_point"],
            "pickup_time": ride["pickup_time"],
            "destination": ride["destination"],
            "duration": ride["duration"],
            "driver":res["name"],
            "status":1

        }
        ride_data.append(ride_item)
     for ride in document2:
        ride_item = {
            "id": str(ride["_id"]),
            "starting_point": ride["starting_point"],
            "pickup_time": ride["pickup_time"],
            "destination": ride["destination"],
            "duration": ride["duration"],
            "status":0

        }
        ride_data.append(ride_item)
     json_ride_data = json.dumps(ride_data, cls=JSONEncoderWithObjectId)
     return json_ride_data



if __name__ == "__main__":
    app.run(debug=True, port=2000)
