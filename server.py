from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)


FAN_SPEED = 0
LIGHT_STATUS = True

# Serve HTML file
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for adding two numbers
@app.route('/get_values', methods=['POST'])
def add_numbers():
    try:
        values_file_path = os.path.join(os.path.dirname(__file__), 'value.json')
        with open(values_file_path) as json_file:
            data = json.load(json_file)
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'values.json file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
