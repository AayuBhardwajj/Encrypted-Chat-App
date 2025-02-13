from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")


key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypted')
def encrypted():
    return render_template('encrypted.html')

@socketio.on('send_message')
def handle_message(data):
    name = data['name']
    message = data['message']
    
    encrypted_message = encrypt_message(message)
    print(f"🔹 Received: {message} | Encrypted: {encrypted_message}")  # Debugging print

    emit('receive_message', {'name': name, 'message': message}, broadcast=True)

    socketio.emit('receive_encrypted_message', {'name': name, 'encrypted': encrypted_message})  

if __name__ == '__main__':
    socketio.run(app, debug=True)
