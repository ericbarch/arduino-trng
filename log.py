import serial
import sys

addr  = '/dev/tty.usbserial-A6008jsU'
baud  = 9600
fname = 'rand.dat'
fmode = 'ab'

with serial.Serial(addr,baud) as port, open(fname,fmode) as outf:
    while True:
        x = port.read(size=1)
        outf.write(x)
        outf.flush()