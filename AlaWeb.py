from flask import Flask, render_template, request

import serial, serial.tools.list_ports
import sys
import time
import socket

app = Flask(__name__)

arduino = None

currLevel = 0.4
currColor = ""
currAnim = ""
currPal = ""


@app.route("/")
def home():
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/brightness/", methods=['POST'])
def brightness():
    btn_name = get_btn_name(request)
    print ("Brightness:", btn_name )
    arduino_send_cmd("B="+str(btn_name))
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/duration/", methods=['POST'])
def duration():
    duration = request.form['duration']
    print ("Duration:", duration)
    arduino_send_cmd("D="+str(duration))
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/color/", methods=['POST'])
def color():
    btn_name = get_btn_name(request)
    print ("Color:", btn_name )
    arduino_send_cmd("C="+str(btn_name))
    
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/palette/", methods=['POST'])
def palette():
    global currLevel
    global currColor
    global currAnim
    global currPal

    btn_name = get_btn_name(request)
    print ("Palette:", btn_name)
    arduino_send_cmd("P="+str(btn_name))
    
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/anim/", methods=['POST'])
def anim():
    btn_name = get_btn_name(request)
    print ("Animation code:", btn_name)
    arduino_send_cmd("A="+str(btn_name))
    templateData = {}
    return render_template('main.html', **templateData);


@app.route("/pal/", methods=['POST'])
def pal():
    global currLevel
    global currColor
    global currAnim
    global currPal

    if 'btnRgb' in request.form:
        arduino_send_cmd("a");
        currPal = "RGB";
    elif 'btnRainbow' in request.form:
        arduino_send_cmd("b");
        currPal = "Rainbow";
    elif 'btnParty' in request.form:
        arduino_send_cmd("d");
        currPal = "Party";
    elif 'btnFire' in request.form:
        arduino_send_cmd("f");
        currPal = "Fire";
    
    templateData = {
      'currAnim': currAnim,
      'currPal': currPal,
      'currLevel': currLevel,
      'currColor': currColor
    };

    return render_template('main.html', **templateData);


def get_btn_name(request):
    btn_name=""
    for key in request.form.keys():
        #print ("Button pressed:", key)
        btn_name = key
    return btn_name


def arduino_get_resp(s):
    time.sleep(.1);
    while (s.in_waiting > 0):
        print(s.readline().decode(), end="");

def arduino_send_cmd(s):
    arduino.flush();
    s = s+'\n'
    arduino.write(s.encode());
    arduino_get_resp(arduino);
    time.sleep(.1);
    arduino.flush()

# try to detect the USB port where Arduino is connected
def arduino_get_port():
    print("Listing ports")
    port = None
    ports = serial.tools.list_ports.comports()
    for p in ports:
        print(p)
        if "Arduino" in p[1]:
            port = p[0]
            print("Arduino detected on port", port)

    return port


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip



if __name__ == "__main__":

    port = None
    
    # use the USB port name if passed
    if len(sys.argv)>1:
        port = sys.argv[1]
        print("Arduino port: " + port)

    # otherwise tries to detect the port
    # this seems to work only on Windows if Arduino USB driver is installed
    while(port==None):
        port = arduino_get_port()
        if port==None:
            print("Arduino not found. Retrying...")
            time.sleep(5);
    
    # open the serial interface
    arduino = serial.Serial(port, 9600, timeout=1)
    time.sleep(.5);
    
    print("Port", arduino)
    print("Current IP is", get_ip())
    print("Point your browser to http://", get_ip(), sep="")
    print()

    #app.run(host='0.0.0.0', port=80, debug=True)
    app.run(host='0.0.0.0', port=80)

