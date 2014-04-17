# Cambrionix API #
Provides a high-level api for the Cambrionix charger
using pySerial.

**This project is in a very early stage and may be buggy or change completely.**

## Prerequisites ##
basically pyserial, just install via pip:

`sudo pip install pyserial`

## Usage ##
Simply create a Cambrionix object by passing the path to the serial device (e.g. '/dev/ttyUSB1').
For each port, an instance of CambrionixPort is created and updated whenever you poll the state. 

A separate thread can be started (and is, by default) which re-polls the state from the charger, updating all CambrionixPorts.

## Troubleshooting ##
SerialException with 'permission denied':
change the permissions via chmod (e.g. chmod 666 <device>) 


