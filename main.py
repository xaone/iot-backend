from app import create_app
# from app.mqtt_client import start_mqtt
import threading
from flask_cors import CORS

# Initialize Flask app
app = create_app()

# Enable CORS
CORS(app)

if __name__ == "__main__":
  # Start the Flask app
    print("hello world!")
    app.run(host="0.0.0.0", port=5001, debug=True)