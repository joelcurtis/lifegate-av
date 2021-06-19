from flask import Flask, render_template
import paramiko
import RPi.GPIO as GPIO
from time import sleep



app = Flask(__name__)

# Establish SSH connection with TesiraFORTÉ
transport = None
tesira = None

def establishConnection():
    global transport
    global tesira
    transport = paramiko.Transport(('192.168.0.49', 22))
    transport.connect(username = 'default', password = 'default')
    tesira = transport.open_channel('session')
    tesira.get_pty()
    tesira.invoke_shell()

# Set GPIO pins to output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)



# --- HOME SCREEN ---

@app.route('/')
def index():
    return render_template('index.html')



# --- POWER ---

# Power On
@app.route('/on')
def on():
    # Turn on system
    if not GPIO.input(11):
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        sleep(180)

    establishConnection()

    # Mute inputs and turn on amps
    tesira.send('Level2 set mute 1 true'+'\n')
    tesira.send('Level1 set mute 1 true'+'\n')
    tesira.send('Level4 set mute 1 true'+'\n')
    tesira.send('LGAmp1 set ampPower true'+'\n')
    tesira.send('LGAmp2 set ampPower true'+'\n')

    return render_template('index.html')

# Power Off
@app.route('/off')
def off():
    # Turn off amps and close SSH connection
    tesira.send('LGAmp1 set ampPower false'+'\n')
    tesira.send('LGAmp2 set ampPower false'+'\n')
    sleep(3)
    transport.close()
    
    # Turn off system
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)

    return render_template('index.html')



# --- AUDIO ---

# Audio Control
@app.route('/audio')
def audio():
    # Unmute inputs
    tesira.send('Level2 set mute 1 false'+'\n')
    tesira.send('Level1 set mute 1 false'+'\n')
    tesira.send('Level4 set mute 1 false'+'\n')

    return render_template('audio.html')

# Level Up
@app.route('/levelUp/<channel>')
def levelUp(channel):
    if channel == 'hh':
        tesira.send('Level2 increment level 1 4'+'\n')
    elif channel == 'pc':
        tesira.send('Level1 increment level 1 4'+'\n')
    elif channel == 'bt':
        tesira.send('Level4 increment level 1 4'+'\n')
    
    return render_template('audio.html')

# Level Down
@app.route('/levelDown/<channel>')
def levelDown(channel):
    if channel == 'hh':
        tesira.send('Level2 decrement level 1 4'+'\n')
    elif channel == 'pc':
        tesira.send('Level1 decrement level 1 4'+'\n')
    elif channel == 'bt':
        tesira.send('Level4 decrement level 1 4'+'\n')
    
    return render_template('audio.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')