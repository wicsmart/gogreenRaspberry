import time
import json
import datetime
import urllib.request
from urllib import error

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
dato = {'temperatura': 52, 'umidade': 55, 'luz': '0', 'time': st}
print(dato)
req = urllib.request.Request('http://localhost:8000/sensein/')
req.add_header('Content-Type', 'application/json')
try:
    response = urllib.urlopen(req, json.dumps(dato))
    response.read()
    print(response.read())
    print(response.getcode())

except urllib.error.HTTPError as e:
    print('HTTP error code= '+str(e.code))
    print('HTTP error reason= '+str(e.read()))

except Exception:
    import traceback
    print('Generic exception: Falha de conexao')