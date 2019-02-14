from django.db import models
from paho.mqtt.publish import single


class SenseIn(models.Model):
    temperatura = models.FloatField('Temperatura', blank=False)
    umidade = models.FloatField('Umidade', blank=False)
    luz = models.IntegerField('Luz', blank=False)
    time = models.DateTimeField('Time', blank=False)

    def __str__(self):
        return "Temperatura: " + str(self.temperatura) + " Umidade: " + str(self.umidade) + " Time: " + str(self.time)

    class Meta:
        ordering = ['time']

class SenseOut(models.Model):

    temperatura = models.FloatField('Temperatura', blank=False)
    umidade = models.FloatField('Umidade', blank=False)
    luz = models.IntegerField('Luz', blank=False)
    time = models.DateTimeField('Time', blank=False)

    def __str__(self):
        return "Temperatura: " + str(self.temperatura) + " Umidade: " + str(self.umidade) + " Time: " + str(self.time)

    class Meta:
        ordering = ['time']

class Monitor(models.Model):
    log = models.TextField('Log', blank=False)
    created = models.DateTimeField('Criado', blank=False)

    class Meta:
        ordering = ['created']


class Acao(models.Model):
    acao = models.IntegerField('Acao', blank=False)
    created = models.DateTimeField('Criado', blank=False)

    class Meta:
        ordering = ['created']


class Status(models.Model):
    status = models.IntegerField('Status', blank=True)
    manual = models.IntegerField('Manual', default=0, blank=True)
    local = models.IntegerField('Local', default=0, blank=True)
    created = models.DateTimeField('Criado', blank=False)

    class Meta:
        ordering = ['created']
        
class Log(models.Model):
    status = models.TextField('Status', blank=False)
    acao = models.TextField('Acao',blank=False)
    created = models.DateTimeField('Created', blank=False)

    class Meta:
        ordering = ['created']
    
class Setup(models.Model):
    temp_max = models.FloatField('Temp_Max', blank=False)
    temp_min = models.FloatField('Temp_Min', blank=False)
    created = models.DateTimeField('Criado', blank=False)
    
    class Meta:
        ordering = ['created']
