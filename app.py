from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Define heading count to template mapping
TEMPLATE_MAPPING = {
    5: ["Intro", "3 Section Hover Box", "Outro"],
    6: ["Intro", "3 Section Hover Box", "Penultimate", "Outro"],
    7: ["Intro", "3 Section Hover Box", "2 Section Hover Box", "Outro"],
    8: ["Intro", "3 Section Hover Box", "3 Section Hover Box", "Outro"]
}

# In-memory templates
TEMPLATES = {
    "Intro": "<section><h2>Intro Section</h2><p>Welcome to our page.</p></section>",
    "3 Section Hover Box": "<section><h2>3 Section Hover Box</h2><p>Three options to explore.</p></section>",
    "2 Section Hover Box": "<section><h2>2 Section Hover Box</h2><p>Two featured options.</p></section>",
    "Penultimate": "<section><h2>Penultimate Section</h2><p>Almost at the end.</p></section>",
    "Outro": "<section><h2>Outro Section</h2><p>Thank you for visiting.</p></section>"
}

# Extract headings from HTML
def extract_headings(html_content):
    return re.findall(r"<h[12]>(.*?)</h[12]>", html_content, re.IGNORECASE)

# API route to process HTML
@app.route('/process', methods=['POST'])
def process_html():
    data = request.get_json()
    html_content = data.get('html', '')

    headings = extract_headings(html_content)
    num_headings = len(headings)

    if num_headings in TEMPLATE_MAPPING:
        template_sections = TEMPLATE_MAPPING[num_headings]
        structured_output = "\n\n".join([TEMPLATES[section] for section in template_sections])
        return jsonify({"structured_html": structured_output})
    else:
        return jsonify({"error": "No predefined template found for this number of headings."}), 400

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
