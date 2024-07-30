from flask import Flask, request, jsonify, send_from_directory
import random
import string
import json

app = Flask(__name__)

# In-memory store
users = {}

def generate_unique_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/addUser', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')

    if not name or not phone or len(phone) != 10 or not phone.isdigit():
        return jsonify({'error': 'Invalid input'}), 400

    unique_id = generate_unique_id()
    users[unique_id] = {'name': name, 'phone': phone}
    return jsonify({'id': unique_id})

@app.route('/getUser/<unique_id>', methods=['GET'])
def get_user(unique_id):
    user = users.get(unique_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'ID not found'}), 404

@app.route('/adminLogin', methods=['POST'])
def admin_login():
    credentials = json.load(open('credentials.json'))
    data = request.json
    admin_id = data.get('id')
    admin_password = data.get('password')

    if (credentials.get('admin', {}).get('id') == admin_id and
        credentials.get('admin', {}).get('password') == admin_password):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 401

@app.route('/admin')
def admin():
    # Serve the admin page
    return send_from_directory('.', 'admin.html')

@app.route('/listUsers', methods=['GET'])
def list_users():
    return jsonify(users)

@app.route('/deleteUser/<unique_id>', methods=['DELETE'])
def delete_user(unique_id):
    if unique_id in users:
        del users[unique_id]
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
