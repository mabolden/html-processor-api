from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all routes

@app.route('/process', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify({"message": "CORS Preflight Passed"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

@app.route('/process', methods=['POST'])
def process_html():
    data = request.get_json()
    html_content = data.get('html', '')

    headings = re.findall(r"<h[12]>(.*?)</h[12]>", html_content, re.IGNORECASE)
    num_headings = len(headings)

    TEMPLATE_MAPPING = {
        5: ["Intro", "3 Section Hover Box", "Outro"],
        6: ["Intro", "3 Section Hover Box", "Penultimate", "Outro"],
        7: ["Intro", "3 Section Hover Box", "2 Section Hover Box", "Outro"],
        8: ["Intro", "3 Section Hover Box", "3 Section Hover Box", "Outro"]
    }

    if num_headings in TEMPLATE_MAPPING:
        structured_output = "\n\n".join(TEMPLATE_MAPPING[num_headings])
        response = jsonify({"structured_html": structured_output})
        response.headers.add("Access-Control-Allow-Origin", "*")  # Allow CORS
        return response
    else:
        response = jsonify({"error": "No predefined template found for this number of headings."})
        response.headers.add("Access-Control-Allow-Origin", "*")  # Allow CORS
        return response, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
