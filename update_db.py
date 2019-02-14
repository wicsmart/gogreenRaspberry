import requests,json
import urllib
import time

r = requests.get('https://gogreenv2.herokuapp.com/senseinUpdate/')
dados = r.json()

for x in dados[:]:
    r = json.dumps(x)
    newData = r.replace('timestamp', 'time')
    print(newData)
    data = json.loads(newData)
    r = requests.post("http://127.0.0.1:8000/sensein/", data=data)
    print(r.status_code, r.reason)
