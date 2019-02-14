import json
import requests

count = 0
timeout = 1

HerokuStatus = 'https://softwaredev.herokuapp.com/status/'
HerokuIn = 'https://softwaredev.herokuapp.com/sensein/'
HerokuOut = 'https://softwaredev.herokuapp.com/senseout/'
HerokuAcao = 'https://softwaredev.herokuapp.com/acao/'
HerokuSetup = 'https://softwaredev.herokuapp.com/setup/'
HerokuLog = 'https://softwaredev.herokuapp.com/log/'

buffer_in = []
buffer_out = []
buffer_status = []
buffer_acao = []
buffer_setup = []

def medida_in(med):
    dato = json.loads(med)
    print(dato['sense'])
    try:
        response = requests.post(HerokuIn, data=dato['sense'])
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_in)))
        if len(buffer_in) > 0:
            for idx, item in enumerate(buffer_in):
                conn = requests.post(HerokuIn, (buffer_in[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_in.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_in.append(dato['sense'])
         print ('Tamanho do buffer: ' + str(len(buffer_in)))
         print('Generic exception: Falha de conexao')
         
    except KeyboardInterrupt:
         print('\nProcesso finalizado\n')
        
def medida_out(med):
    dato = json.loads(med)
    print(dato['sense'])
    try:
        response = requests.post(HerokuOut, data=dato['sense'])
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_out)))
        if len(buffer_out) > 0:
            for idx, item in enumerate(buffer_out):
                conn = requests.post(HerokuOut, (buffer_out[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_out.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_out.append(dato['sense'])				
         print ('Tamanho do buffer: ' + str(len(buffer_out)))
         print('Generic exception: Falha de conexao')

def status(med):
    dato = json.loads(med)
    print(dato['estado'])
    try:
        response = requests.post(HerokuStatus, data=dato['estado'])
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_status)))
        if len(buffer_status) > 0:
            for idx, item in enumerate(buffer_status):
                conn = requests.post(HerokuStatus, (buffer_status[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_status.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_status.append(dato['estado'])				
         print ('Tamanho do buffer: ' + str(len(buffer_status)))
         print('Generic exception: Falha de conexao')
   
def acao(dato):
    #dato = json.loads(med)
    print('post acao')
    print(dato)
    try:
        response = requests.post(HerokuAcao, data=dato)
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_acao)))
        if len(buffer_out) > 0:
            for idx, item in enumerate(buffer_acao):
                conn = requests.post(HerokuAcao, (buffer_acao[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_acao.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_acao.append(dato)				
         print ('Tamanho do buffer: ' + str(len(buffer_acao)))
         print('Generic exception: Falha de conexao')
     
def setup(dato):
    print(dato)
    try:
        response = requests.post(HerokuSetup, data=dato)
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_setup)))
        if len(buffer_out) > 0:
            for idx, item in enumerate(buffer_setup):
                conn = requests.post(HerokuSetup, (buffer_setup[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_setup.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_setup.append(dato)				
         print ('Tamanho do buffer: ' + str(len(buffer_setup)))
         print('Generic exception: Falha de conexao')
         
def log_acao(dato):
    #dato = json.loads(med)
    print('post log')
    print(dato)
    try:
        response = requests.post(HerokuLog, data=dato)
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_acao)))
        if len(buffer_out) > 0:
            for idx, item in enumerate(buffer_acao):
                conn = requests.post(HerokuLog, (buffer_acao[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_acao.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_acao.append(dato)				
         print ('Tamanho do buffer: ' + str(len(buffer_acao)))
         print('Generic exception: Falha de conexao')

def log_status(med):
    ret = json.loads(med)
    logger = {'status': ret['estado']['status'], 'acao':'null', 'created': ret['estado']['created']}    
    try:
        response = requests.post(HerokuLog, data=logger)
        print (response.status_code, response.reason)
        #print ('tamanho do buffer: ' + str(len(buffer_status)))
        if len(buffer_status) > 0:
            for idx, item in enumerate(buffer_status):
                conn = requests.post(HerokuLog, (buffer_status[idx]))
                print ('Resposta do reqBuffer = ' + str(response.reason))
                if response.status_code == 201:
                    buffer_status.pop(idx)
    except requests.exceptions.HTTPError as err:
        print ('httpError')
    except requests.exceptions.Timeout:
        print('timeout')
    except requests.exceptions.RequestException as e:
         buffer_status.append(logger)				
         print ('Tamanho do buffer: ' + str(len(buffer_status)))
         print('Generic exception: Falha de conexao')
