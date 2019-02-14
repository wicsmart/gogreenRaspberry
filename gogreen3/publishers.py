from paho.mqtt.publish import single
import paho.mqtt.client as mqtt
import os
import django
import json

os.environ["DJANGO_SETTINGS_MODULE"] = 'version2.settings'
django.setup()

from polls.serializers import AcaoSerializer, SenseInSerializer, StatusSerializer, SenseOutSerializer, LogSerializer, SetupSerializer
from polls.models import SenseIn, SenseOut

host = '165.227.28.137'
port = 1883
keepalive= 300
topicAcao = 'acao'
topicStatus = 'status'

# Salvar localmente
def save_log_local(status):
    ret = json.loads(status)
    logger = {'status': ret['estado']['status'], 'acao':'null', 'created': ret['estado']['created']}
    log = LogSerializer(data=logger)
    if log.is_valid():
        log.save()
        print('salvou log localmente')
    else:
        print(log.errors)

def save_sensein(sense): # OK
    senseIn = SenseInSerializer(data=sense)
    if senseIn.is_valid():
        senseIn.save()
        print('salvou sensein localmente')
    else:
        print(senseIn.errors)

def save_senseout(sense): # OK
    senseOut = SenseOutSerializer(data=sense)
    if senseOut.is_valid():
        senseOut.save()
        print('salvou senseout localmente')
    else:
        print(senseOut.errors)

def save_status_local(status): # OK
    ret = json.loads(status)
    st = ret['estado']
    status = StatusSerializer(data=st)
    if status.is_valid():
        status.save()
        print('salvou status localmente')
    else:
        print(status.errors)
        
def save_setup_local(status): # OK
    ret = json.loads(status)
    st = ret['setup']
    setup = SetupSerializer(data=st)
    if setup.is_valid():
        setup.save()
        print('salvou setup localmente')
    else:
        print(setup.errors)
        

'''
client = mqtt.Client(client_id='gateway', clean_session=True, userdata=None,
                    transport="tcp")
'''        
         
#   Mensagens para banco de dados web

'''
def salvar_sense_heroku(msg): # OK
    ret = json.loads(msg)
    sense = json.dumps(ret['sense'])
    if ret['end'] == "241":
        #single(topic='sensein', qos=2, payload=sense, hostname=host, port=port)
    if ret['end'] == "240":
        #single(topic='senseout', qos=2, payload=sense, hostname=host, port=port)
    print('Acao enviada para o heroku')
                         
def status_to_heroku(msg): # OK
    ret = json.loads(msg)
    status = json.dumps(ret['estado'])
    #client.publish(topic='status', qos=2, payload=status)
    print('Status para o heroku')
   
def acao_db_heroku(msg):
    single(topic='acao', qos=2, payload=msg, hostname=host, port=port)
    print('Acao enviada para o heroku')
'''    


def salvar_sense_local(msg): # OK
    ret = json.loads(msg)
    if ret['end'] == "230":
        #single(topic='sensein', qos=2, payload=msg, hostname=host, port=port)
        save_sensein(ret['sense'])

    if ret['end'] == "001":
        #single(topic='senseout', qos=2, payload=msg, hostname=host, port=port)
        save_senseout(ret['sense'])

#   Mensagens para pagina local


def publicar_sense_local(msg): # OK
    single(topic='status', qos=1, payload=msg, hostname='127.0.0.1', port=9001, transport='websockets')
    print('Publicou sense/stautus para pagina local')

def acao_db_local(msg):
    single(topic='acao', qos=2, payload=msg, hostname='127.0.0.1', port=9001, transport='websockets')



def on_connect(client, userdata, flags, rc):
    print('Conectado ao Broker Local')
    client.publish(topic='status', qos=0, payload='ligado', retain=False)
    #client.message_callback_add(sub='acao', callback=save)


def on_disconnect(client, userdata, flags, rc):
    print("Desconectou do Broker")
    
'''
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(host=host, port=1883, keepalive=300, bind_address='')
'''
