from flask import Flask, request, jsonify
from maze_run import maze_run
import threading

app = Flask(__name__)


# Create a separate thread for the background task
background_thread = threading.Thread(target=maze_run)
# Set the thread as a daemon so that it automatically stops when the main thread (Flask app) stops
background_thread.daemon = True
# Start the thread
background_thread.start()

@app.route('/api/data', methods=['POST'])
def get_data():
    # Handle the request and return data
    message = 100
    a = '1234'
    return jsonify({'message': str(message), 'a': a})

@app.route('/api/data', methods=['POST'])
def post_data():
    # Access the data sent in the request body
    data = request.get_json()

    # Access specific values from the data
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')

    # Handle the request and return data

    # ... process the data ...

    # Create a response dictionary
    response = {'message': 'Post created successfully'}

    # Return the response as JSON
    return jsonify(response)

if __name__ == '__main__':
    app.run()