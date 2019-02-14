from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from polls.serializers import *
from polls.models import *
from polls.models import Status as StatusModel
from polls.models import Setup as SetupModel
from rest_framework import generics
from django.views import View
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta, date

class IsAuthenticatedNotPost(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedNotPost, self).has_permission(request, view)

class JSONResponse(HttpResponse):

    """
    An HttpResponse that renders its content into JSON.
    """
    def _init_(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self)._init_(content, **kwargs)
        
def home(request):
    return render(request, 'index.html', {'html_var':'holaaa'})

def cliente(request):
    return render(request, 'cliente.html')

def lastSenseIn(request):
    sensein = SenseIn.objects.latest('time')
    serializer = SenseInSerializer(sensein)
    return JsonResponse(serializer.data)

def lastSenseOut(request):
    senseout = SenseOut.objects.latest('time')
    serializer = SenseInSerializer(senseout)
    return JsonResponse(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#*********** Medidas

class SenseInListOld(generics.ListCreateAPIView):

    #permission_classes = (IsAuthenticatedNotPost,)
    permission_classes = (AllowAny,)

    queryset = SenseIn.objects.all()
    serializer_class = SenseInSerializer

class SenseInList(generics.ListCreateAPIView):

    #permission_classes = (IsAuthenticatedNotPost,)
    permission_classes = (AllowAny,)
    inicio = datetime(2018,4,11)
    queryset = SenseIn.objects.filter(time__gte=inicio)
    serializer_class = SenseInSerializer
 

class SenseInDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = SenseIn.objects.all()
    serializer_class = SenseInSerializer


class SenseOutList(generics.ListCreateAPIView):

   # permission_classes = (IsAuthenticatedNotPost,)
    permission_classes = (AllowAny,)
    queryset = SenseOut.objects.all()
    serializer_class = SenseOutSerializer

class SenseOutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SenseOut.objects.all()
    serializer_class = SenseOutSerializer



#************* Ações/Status/Mensagens

def freshData(request):
    sensein = SenseIn.objects.latest('time')
    senseout = SenseOut.objects.latest('time')
    status = StatusModel.objects.latest('created')
    setup = SetupModel.objects.latest('created')
    
    statusSer = StatusSerializer(status)
    senseinSer = SenseInSerializer(sensein)
    senseoutSer = SenseInSerializer(senseout)
    setupSer = SetupSerializer(setup)
    data = {
        'sensein': senseinSer.data,
        'senseout': senseoutSer.data,
        'status': statusSer.data,
        'setup': setupSer.data
    }
    print(data)
    return JsonResponse(data)

def dadosPizza(request):
    tabaixo = SenseIn.objects.filter(temperatura__lte=8).count()
    tdentro = SenseIn.objects.filter(temperatura__range=(8,30)).count()
    tacima = SenseIn.objects.filter(temperatura__gt=30).count()

    uabaixo = SenseIn.objects.filter(umidade__lte=50).count()
    udentro = SenseIn.objects.filter(umidade__range=(50, 80)).count()
    uacima = SenseIn.objects.filter(umidade__gt=80).count()

    total = SenseIn.objects.all().count()

    tabaixo = round((tabaixo * 100)/total, 1)
    tacima = round((tacima * 100) / total, 1)
    tdentro = round((tdentro * 100) / total, 1)

    uabaixo = round((uabaixo * 100) / total, 1)
    udentro = round((udentro * 100) / total, 1)
    uacima = round((uacima * 100) / total, 1)

    data = {
        'tbaixo': tabaixo,
        'tdentro': tdentro,
        'tacima': tacima,
        'ubaixo': uabaixo,
        'udentro': udentro,
        'uacima': uacima,
        'total': total
    }
    return JsonResponse(data)
    
class Setup(generics.ListCreateAPIView):
	
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer

class Monitor(generics.ListCreateAPIView):
	
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

class Acao(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)

    queryset = Acao.objects.all()
    serializer_class = AcaoSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        #json = '{"acao": "' +str(instance.acao) + '"}'
		

class Status(generics.ListCreateAPIView):

    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        json = '{"status": "' + str(instance.status) + '"}'
        enviar_status_to_heroku(json)
        enviar_status_to_local(json)

class Logs(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    
    startdate = datetime.now().replace(microsecond=0)
    enddate = startdate - timedelta(days=1)
    queryset = Log.objects.filter(created__gte=enddate)
   # queryset = Log.objects.all()
    serializer_class = LogSerializer

class ClienteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "cliente.html", context='Oi')
