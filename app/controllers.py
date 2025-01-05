from flask import Blueprint, request, jsonify
import base64

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route('/alert/status',methods=['GET'])
def get_alert():
    print("Entering get_alert function")

    try:
        db = get_database()
        print("Database connection established")
        alter_status_collection = db['alert_data']

        alter_status = alter_status_collection.find_one()
        print("Alert status retrieved")

        if alter_status is None:
            return jsonify({"error": "Alert status not found"}), 404

        return jsonify({"status": alter_status['value']}), 200

    except Exception as e:
        print(f"Error retrieving alert status: {e}")
        return jsonify({"error": "Failed to retrieve alter status"}), 500
        

@api_blueprint.route('/alert/switch', methods=['POST'])
def alter_status():
    """
    Endpoint to publish a alter status message.
    """
    print("Entering alter_status function")
    try:
        db = get_database()
        print("Database connection established")
        alert_status_collection = db['alert_data']

        alert_status = alert_status_collection.find_one()
        print("alter status retrieved")

        if alter_status is None:
            return jsonify({"error": "alert status not found"}), 404

        new_value = not alert_status['value']

        alert_status_collection.update_one({}, {"$set": {"value": new_value}})

        return jsonify({"status": "Alert status switched", "new_value": new_value}), 200
    except Exception as e:
        print(f"Error switching alert status: {e}")
        return jsonify({"error": "Failed to switch alert status"}), 500


@api_blueprint.route('/')
def hello_world():
    """
    A simple hello world endpoint.
    """
    return "Hello World", 200