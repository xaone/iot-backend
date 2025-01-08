from flask import Blueprint, request, jsonify
from .db import get_database
import base64
from .email_alert import process_base64_image

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
def alert_switch():
    """
    Endpoint to publish a alert_switch message.
    """
    print("Entering alert_switch function")
    try:
        db = get_database()
        print("Database connection established")
        alert_status_collection = db['alert_data']

        alert_status = alert_status_collection.find_one()
        print("alter status retrieved")

        if alert_status is None:
            return jsonify({"error": "alert status not found"}), 404

        new_value = not alert_status['value']

        alert_status_collection.update_one({}, {"$set": {"value": new_value}})

        return jsonify({"status": "Alert status switched", "new_value": new_value}), 200
    except Exception as e:
        print(f"Error switching alert status: {e}")
        return jsonify({"error": "Failed to switch alert status"}), 500

@api_blueprint.route('/sensor/status', methods=['GET'])
def get_status():
    """
    Endpoint to get the current sensor status.
    """
    print("Entering get_status function")
    try:
        db = get_database()
        print("Database connection established")
        sensor_status_collection = db['sensor_data']

        sensor_status = sensor_status_collection.find_one()
        print("Sensor status retrieved")

        if sensor_status is None:
            return jsonify({"error": "Sensor status not found"}), 404

        return jsonify({"status": sensor_status['value']}), 200
    except Exception as e:
        print(f"Error retrieving sensor status: {e}")
        return jsonify({"error": "Failed to retrieve sensor status"}), 500

@api_blueprint.route('/sensor/switch', methods=['POST'])
def switch_status():
    """
    Endpoint to publish a switch status message.
    """
    print("Entering switch_status function")
    try:
        db = get_database()
        print("Database connection established")
        sensor_status_collection = db['sensor_data']

        sensor_status = sensor_status_collection.find_one()
        print("Sensor status retrieved")

        if sensor_status is None:
            return jsonify({"error": "Sensor status not found"}), 404

        new_value = not sensor_status['value']

        sensor_status_collection.update_one({}, {"$set": {"value": new_value}})
        print("Sensor status updated")

        return jsonify({"status": "Sensor status switched", "new_value": new_value}), 200
    except Exception as e:
        print(f"Error switching sensor status: {e}")
        return jsonify({"error": "Failed to switch sensor status"}), 500

@api_blueprint.route('/image/display', methods=['GET'])
def get_all_images():
    """
    Endpoint to get all images from the MongoDB collection.
    """
    print("Entering get_all_images function")
    try:
        db = get_database()
        print("Database connection established")
        images_collection = db['images']
        images = images_collection.find({}, {"_id": 0, "image_data": 1})
        print("Images retrieved")

        image_list = []
        for image in images:
            image_data_base64 = base64.b64encode(image['image_data']).decode('utf-8')
            image_list.append({"image_data": image_data_base64})

        return jsonify(image_list), 200
    except Exception as e:
        print(f"Error retrieving images: {e}")
        return jsonify({"error": "Failed to retrieve images"}), 500

from flask import request, jsonify

@api_blueprint.route('/alert/email', methods=['POST'])
def email_alert():
    """
    Endpoint to receive a base64 image and process it.
    # """
    # if request.content_type != 'application/json':
    #     return jsonify({"error": "Unsupported Media Type, expected application/json"}), 415
    
    try:
        data = request.json
        base64_image = data.get('image')
        distance = data.get('distance')

        if not base64_image:
            return jsonify({"error": "No image provided"}), 400

        result = process_base64_image(base64_image, distance)

        if result:
            return jsonify({"status": "Image processed successfully"}), 200
        else:
            return jsonify({"error": "Failed to process image"}), 500
    except Exception as e:
        print(f"Error in email_alert endpoint: {e}")
        return jsonify({"error": "Failed to process request"}), 500



@api_blueprint.route('/')
def hello_world():
    """
    A simple hello world endpoint.
    """
    return "Hello World", 200
