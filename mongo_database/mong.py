from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from decouple import config


#MongoDB connection
app = Flask(__name__)
CORS(app, resources={r"/upload_report": {"origins": "*"}})
app.config['MONGO_URI'] = config('MONGO_URI')
mongo = PyMongo(app)

print('Connection to MongoDB established successfully.') if mongo else print('Error connecting to MongoDB.')

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/upload_report', methods=['POST'])
def upload_report():
    #Data sent from Streamlit is received.
    data = request.json

    video_and_detections_report = mongo.db.detections.insert_one(data)

    if video_and_detections_report:
        return 'Data successfully saved in MongoDB.', 200
    else:
        return 'Error while saving data.', 500


if __name__ == "__main__":
    app.run(debug=True)



