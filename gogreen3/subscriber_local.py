import os
import django
import json
import escrever_serial as escrever
from paho.mqtt import publish
from paho.mqtt.publish import single
from datetime import datetime
import sender as post


os.environ["DJANGO_SETTINGS_MODULE"] = 'version2.settings'
django.setup()

from polls.serializers import AcaoSerializer, SenseInSerializer, StatusSerializer, SenseOutSerializer, SetupSerializer, LogSerializer
from polls.models import SenseIn, SenseOut, Setup, Acao

from polls.models import Acao
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTv311

client = mqtt.Client(client_id='subscribe_pag', clean_session=True, userdata=None,
                     protocol=MQTTv311, transport="websockets")

host = '165.227.28.137'
port = 1883
keepalive= 300
       
def save_acao(client, userdata, msg):
    my_json = msg.payload.decode()    
    payload = json.loads(my_json)
    print(payload)
    
    escrever.acao(payload)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    objAcao = {'acao': payload, 'created':timestamp}
    objLog = {'status': 'null', 'acao': payload, 'created':timestamp}
    post.log_acao(objLog)
    log = LogSerializer(data=objLog)
    if log.is_valid():
        log.save()
        print('salvou log localmente')
    else:
        print(log.errors)
        
    objAcaoStr = json.dumps(objAcao)
    post.acao(objAcao)
    acao = AcaoSerializer(data=objAcao)
    if acao.is_valid():
        acao.save()
        print('salvou acao localmente')
    else:
        print(acao.errors)

def save_setup(client, userdata, msg):
    my_json = msg.payload.decode()    
    p = json.loads(my_json)
    print(p)
    p = str(p)
    escrever.setup(p)
    temp_max = str(p[:2])+'.'+str(p[2])
    temp_min = str(p[3:5])+'.'+str(p[5])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    objSetup = {'temp_max':temp_max, 'temp_min':temp_min, 'created':timestamp}
    objSetupStr = json.dumps(objSetup)
    post.setup(objSetup)
    setup = SetupSerializer(data=objSetup)
    if setup.is_valid():
        setup.save()
        print('salvou setup localmente')
    else:
        print(setup.errors)


def pedir_acao(client, userdata, msg):
    my_json = msg.payload.decode()    
    payload = json.loads(my_json)
    escrever.manual(payload)
    print(payload)

def on_connect(client, userdata ,flags, result):
    print('Conectado ao Broker')
    client.subscribe([('acao', 2), ("setup", 2), ("manual", 2)])
    
    client.message_callback_add(sub='setup', callback=save_setup)
    client.message_callback_add(sub='manual', callback=pedir_acao)
    client.message_callback_add(sub='acao', callback=save_acao)
   

def on_disconnect(cliente, userdata,flags, rc):
    print("Desconectou do Broker")


client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.will_set(topic='warning', payload=str("raspi") + " disconnect", qos=2, retain=False)

client.connect(host='127.0.0.1', port=9001, keepalive=300, bind_address='')
client.loop_forever()
