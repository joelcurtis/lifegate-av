# Lifegate AV System

A simple web server running on Flask, that enables a Raspberry Pi to power on/off the Lifegate Padstow AV system, and control the TesiraFORTÉ device.

## Installation Instructions

1. Log in to your Raspberry Pi (default username and password is `pi` and `raspberry`, respectively).
2. Navigate to the root directory and install dependencies.

	```
	cd ~
	pip3 install flask
	pip3 install RPi.GPIO
	pip3 install paramiko
	```

3. Clone the repository.

	```
	git clone https://github.com/joelcurtis/lifegate-av.git
	```

4. To start the program on boot, edit `rc.local` by typing `sudo nano /etc/rc.local` and adding the below line just before `exit 0`.

	```
	sudo python3 /home/pi/lifegate-av/app.py &
	```
	
	Save the file with 'CTRL + X' and press 'Enter'
