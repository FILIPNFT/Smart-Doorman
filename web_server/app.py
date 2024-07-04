from flask import Flask, render_template, request, jsonify, redirect, url_for
import netifaces as ni
import random
import datetime

app = Flask(__name__)

def get_mac_address(interface='eth0'):
    try:
        return ni.ifaddresses(interface)[ni.AF_LINK][0]['addr']
    except (ValueError, KeyError, IndexError):
        return "No MAC Address found"

@app.route('/')
def home():
    return redirect(url_for('register_device'))

@app.route('/register', methods=['GET', 'POST'])
def register_device():
    mac_address = get_mac_address()
    if request.method == 'POST':
        device_id = request.form.get('device_id')
        location = request.form.get('location')
        description = request.form.get('description')
        
        print(f"Device ID: {device_id}, Location: {location}, Description: {description}")
        return render_template('registration_success.html', device_id=device_id)
        
    return render_template('register.html', device_id=mac_address)

@app.route('/rfid')
def rfid():
    return render_template('rfid.html')

@app.route('/face')
def face():
    return render_template('face.html')
    
@app.route('/data/rfid')
def data_rfid():
    hours = [(datetime.datetime.now() - datetime.timedelta(hours=i)).strftime('%H:%M') for i in range(24)]
    counts = [random.randint(0, 20) for _ in range(24)]
    return jsonify({'timestamps': hours[::-1], 'counts': counts[::-1]})

@app.route('/data/face')
def data_face():
    hours = [(datetime.datetime.now() - datetime.timedelta(hours=i)).strftime('%H:%M') for i in range(24)]
    counts = [random.randint(0, 50) for _ in range(24)]
    return jsonify({'timestamps': hours[::-1], 'counts': counts[::-1]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
