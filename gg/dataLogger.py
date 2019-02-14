from urllib2 import HTTPError
import serial
import time
import json
import urllib2
import datetime

ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

reqLocalBuffer = urllib2.Request('http://localhost:8000/buffer/')
reqLocalBuffer.add_header('Content-Type', 'application/json')

reqLocal = urllib2.Request('http://localhost:8000/medida/')
reqLocal.add_header('Content-Type', 'application/json')

reqHeroku = urllib2.Request('https://servergogreen.herokuapp.com/medida/')
reqHeroku.add_header('Content-Type', 'application/json')

reqHerokuBuffer = urllib2.Request('https://servergogreen.herokuapp.com/buffer/')
reqHerokuBuffer.add_header('Content-Type', 'application/json')

count = 0
timeout = 1
buffer = []

while True:
    response = ser.readline()
    if response and response[0] == '*':
        count = count+1
        print count
        print response
    if response and count == 20:
        print (response)
        count = 0
        m = response[3:-4]
        medida = m.split(':')
        if (len(medida) > 1):
            temp = int(medida[0])
            if temp < 50:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                dato = {'temperatura': medida[0], 'umidade': medida[1], 'luz': '0', "timestamp": st}
                print('Dado enviado: '+ str(dato))
                try:
                    response = urllib2.urlopen(reqHeroku, json.dumps(dato))
                    response.read()
                    code = response.getcode()
                    print ('Resposta do dato = ' + str(code))
                    print ('tamanho do buffer: ' + str(len(buffer)))
                    if len(buffer) > 0:
                        for idx, item in enumerate(buffer):
                            conn = urllib2.urlopen(reqHeroku, json.dumps(buffer[idx]))
                            conn.read()
                            code = conn.getcode()
                            print ('Resposta do reqBuffer = ' + str(code))
                            if code == 201:
                                buffer.pop(idx)

                except urllib2.HTTPError, e:
                    print('HTTP error code= ' + str(e.code))
                except Exception:
                    import traceback
                    buffer.append(dato)
                    print ('Tamanho do buffer: ' + str(len(buffer)))
                    print('Generic exception: Falha de conexao')
