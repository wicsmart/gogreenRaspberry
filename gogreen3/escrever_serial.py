import time
import serial
import paho.mqtt.client as mqtt

ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def acao(msg):
    frame = '*C'+str(msg)+'9999999999250#'
    ser.write(frame.encode())
    print('Mensagem escrita na serial : ' + frame)

def manual(msg):
    frame = '*C99999999'+str(msg)+'99250#'
    ser.write(frame.encode())
    print('Mensagem escrita na serial : ' + frame)

def setup(msg):
    frame = 'S'+str(msg)+'999999250#'
    ser.write(frame.encode())
    print('Mensagem escrita na serial : ' + frame)
