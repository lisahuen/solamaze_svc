from flask import Flask, request, jsonify
from flask_cors import CORS
from maze_run import job_start
import general
import threading

app = Flask(__name__)
CORS(app)
CORS(app, origins='http://localhost:3000')



# Create a separate thread for the background task
background_thread = threading.Thread(target=job_start)
# Set the thread as a daemon so that it automatically stops when the main thread (Flask app) stops
background_thread.daemon = True
# Start the thread
background_thread.start()

@app.route('/api/data', methods=['GET'])
def get_data():
    # Handle the request and return data
    # maze_id, tran_id = general.getStartDisplayTransID()
    message = 100
    a = '1234'
    return jsonify({'message': str(message), 'a': a})

@app.route('/api/getStartTranID', methods=['POST'])
def api_get_start_tran_id():

    response = general.getStartDisplayTransID()

    return response


@app.route('/api/getTran', methods=['POST'])
def api_get_tran():
    # Access the data sent in the request body

    data = request.get_json()
    maze_id = data.get('maze_id')
    tran_id = data.get('tran_id')
    response = general.getTransByID(maze_id,tran_id)

    return response

if __name__ == '__main__':
    app.run()