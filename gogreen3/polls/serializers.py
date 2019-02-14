from django.contrib.auth.models import User, Group
from rest_framework import serializers
from polls.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SenseInSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenseIn
        fields = ('id', 'temperatura', 'umidade', 'luz', 'time')


class SenseOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenseOut
        fields = ('id', 'temperatura', 'umidade', 'luz', 'time')
        
class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ('id', 'log', 'created')
        
class AcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acao
        fields = ('id', 'acao', 'created')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'status', 'manual', 'local', 'created')
        
class LogSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = Log
        fields = ('id', 'status', 'acao', 'created')
      
class SetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setup
        fields = ('id', 'temp_max', 'temp_min', 'created')
