import os
import django
import json
import subscriber_local
from paho.mqtt import publish
from paho.mqtt.publish import single
import sender as post

os.environ["DJANGO_SETTINGS_MODULE"] = 'version2.settings'
django.setup()

from polls.serializers import AcaoSerializer, SenseInSerializer, StatusSerializer, SenseOutSerializer
from polls.models import SenseIn, SenseOut

from polls.models import Acao
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTv311

client = mqtt.Client(client_id='mqtt_run', clean_session=True, userdata=None,
                     protocol=MQTTv311, transport="websockets")

def update_sensein(client, userdata, msg):
    SenseIn.objects.latest('time').delete()	
    my_json = msg.payload.decode()
    payload = json.loads(my_json)
    print(payload)
    senseIn = SenseInSerializer(data=payload)
    if senseIn.is_valid():
        senseIn.update(payload)
        print('salvou sensein localmente')
    else:
        print(senseIn.errors)
     
def update_senseout(client, userdata, msg):
    SenseOut.objects.latest('time').delete()	
    my_json = msg.payload.decode()
    payload = json.loads(my_json)
    print(payload)
    senseOut = SenseOutSerializer(data=payload)
    if senseOut.is_valid():
        senseOut.save()
        print('salvou sensout localmente')
    else:
        print(senseOut.errors)
        
def save_status(client, userdata, msg):
    my_json = msg.payload.decode()
    payload = json.loads(my_json)
    print(payload)
    status = StatusSerializer(data=payload)
    if status.is_valid():
        status.save()
        print('salvou status localmente')
    else:
        print(status.errors)
        
def save_acao(client, userdata, msg):
    my_json = msg.payload.decode()
    print(my_json)
    
    payload = json.loads(my_json)
    print(payload)
    escrever.acao(payload.acao)
    post.acao(payload)
    acao = AcaoSerializer(data=payload)
    if acao.is_valid():
        acao.save()
        print('salvou acao localmente')
    else:
        print(acao.errors)
   
def on_connect(client, userdata ,flags, result):
    print('Conectado ao Broker')
    client.subscribe([('acao', 2), ("sensein", 2), ("senseout", 2), ('status', 2)])
    
    client.message_callback_add(sub='sensein', callback=update_sensein)
    client.message_callback_add(sub='senseout', callback=update_senseout)
    client.message_callback_add(sub='acao', callback=save_acao)
    client.message_callback_add(sub='status', callback=save_status)


def on_disconnect(cliente, userdata,flags, rc):
    print("Desconectou do Broker")

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
@receiver(post_save, sender=Acao)
def save_profile(sender, instance, **kwargs):
    print('post_save executado no heroku')
    publish.single(topic='atualizaWeb', qos=0, payload=instance.acao, hostname='165.227.28.137', port=1883)
'''


client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.will_set(topic='warning', payload=str("raspi") + " disconnect", qos=2, retain=False)

client.connect(host='127.0.0.1', port=1880, keepalive=300, bind_address='')
client.loop_forever()
