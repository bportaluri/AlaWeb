from flask import Flask, render_template, request

import serial, serial.tools.list_ports
import sys
import time
import socket

'''
global arduino
global currLevel
global currColor
global currAnim
global currPal
'''
app = Flask(__name__)

#serial_port = 'COM5'
#serial_port = '/dev/ttyACM1'

currLevel = 0.4
currColor = ""
currAnim = ""
currPal = ""

@app.route("/")
def hello():
    templateData = {
      'currAnim': currAnim,
      'currPal': currPal,
      'currLevel': currLevel,
      'currColor': currColor
    };
    return render_template('main.html', **templateData);



@app.route("/brightness/", methods=['POST'])
def brightness():
    btn_name = get_btn_name(request)
    print ("Brightness:", btn_name )
    sendCmd("B="+str(btn_name))
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/duration/", methods=['POST'])
def duration():
    duration = request.form['duration']
    print ("Duration:", duration)
    sendCmd("D="+str(duration))
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/color/", methods=['POST'])
def color():
    btn_name = get_btn_name(request)
    print ("Color:", btn_name )
    sendCmd("C="+str(btn_name))
    
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
    sendCmd("P="+str(btn_name))
    
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/anim/", methods=['POST'])
def anim():
    btn_name = get_btn_name(request)
    print ("Animation code:", btn_name)
    sendCmd("A="+str(btn_name))
    templateData = {}
    return render_template('main.html', **templateData);


@app.route("/pal/", methods=['POST'])
def pal():
    global currLevel
    global currColor
    global currAnim
    global currPal

    if 'btnRgb' in request.form:
        sendCmd("a");
        currPal = "RGB";
    elif 'btnRainbow' in request.form:
        sendCmd("b");
        currPal = "Rainbow";
    elif 'btnParty' in request.form:
        sendCmd("d");
        currPal = "Party";
    elif 'btnFire' in request.form:
        sendCmd("f");
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



def get_resp(s):
    time.sleep(.1);
    while (s.in_waiting > 0):
        print(s.readline().decode(), end="");

def sendCmd(s):
    arduino.flush();
    s = s+'\n'
    arduino.write(s.encode());
    get_resp(arduino);
    time.sleep(.1);
    arduino.flush()


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

def get_arduino_port():
    port = None
    ports = serial.tools.list_ports.comports()
    for p in ports:
        print(p)
        if "Arduino" in p[1]:
            port = p[0]

    return port



arduino=None

if __name__ == "__main__":

    print("main")
    
    
    print (">>>>", arduino)
    #print (">>>>", port)
    port = None
    while(port==None):
        port = get_arduino_port()

        if port:
            print("Arduino detected on port", port)
        else:
            print("Arduino not found. Retrying...")
            time.sleep(5);
    
    #serial.Serial(serial_port).close();
    arduino = serial.Serial(port, 9600, timeout=1)

    time.sleep(.5);
    
    print("Port", arduino)
    print("Current IP is", get_ip())
    print()

    #app.run()
    #app.run(host='0.0.0.0', port=80, debug=True)
    app.run(host='0.0.0.0', port=80)


