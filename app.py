from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask server is running on Render!"

@app.route('/print', methods=['POST'])
def print_data():
    data = request.json
    print("Dữ liệu nhận được:", data)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run()
