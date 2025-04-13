from flask import Flask, request, render_template, jsonify
from compensation_logic import calculate_compensation

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    result = calculate_compensation(data)
    return jsonify({'compensation': result})

if __name__ == '__main__':
    app.run(debug=True)
