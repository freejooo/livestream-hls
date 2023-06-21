import random
import string
from flask import Flask, send_from_directory, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit
from captcha.image import ImageCaptcha

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Change this to your desired secret key
socketio = SocketIO(app)
captcha = ImageCaptcha(fonts=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'])  # Change the font path if necessary

# Generate a random CAPTCHA text
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Generate CAPTCHA image
def generate_captcha_image(text):
    image_data = captcha.generate(text)
    return image_data.getvalue()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hls/<path:filename>')
def hls(filename):
    return send_from_directory('stream', filename)

@app.route('/hls/play/<path:filename>')
def hls_segments(filename):
    return send_from_directory('stream/play', filename)

@app.route('/captcha')
def captcha_route():
    text = generate_captcha_text()
    image = generate_captcha_image(text)
    session['captcha_text'] = text
    return image, 200, {'Content-Type': 'image/png'}

@app.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    captcha_text = session.get('captcha_text')
    if captcha_text and request.form['captcha_text'] == captcha_text:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

# SocketIO events
@socketio.on('chat_message')
def handle_chat_message(message):
    username = session.get('username', 'Anonymous')
    emit('chat_message', f'{username}: {message}', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8080)