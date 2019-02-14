import serial
from time import sleep

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

temp = None
umid = None
status = None
man_auto = None
local_rem = None
acao = None
temp_sup = None
temp_inf = None

ctr = 0
msg="none"

while(True):
    print('\n\nEscolha o que enviar\n')
    print('1 - Medida estufa\n')
    print('2 - Status')
    print('3 - Pedir status')
    print('4 - Pedir medida')
    print('5 - Limpar serial')
    ctr = int(input('...\n'))
    if(ctr == 2):
        entrada = input('Status...(1 casa decimal)\nRecolhida = 0\nEsetndida = 1\n'+
                           'Transisção = 2\nIndefinido = 3:\n')
        if(len(entrada)>0):
            status=entrada;
            
        entrada = input('Temperatura Superior: (3 bytes)\n')
        if(len(entrada)>0):
            temp_sup=entrada;
            
        entrada= input('Temperatura Inferior: (3 bytes)\n')
        if(len(entrada)>0):
            temp_inf=entrada
        
        entrada = input('Manual = 0 / Automatico = 1:\n')
        if(len(entrada)>0):
            man_auto=entrada
            
        entrada = input('Local/Remoto = Local = 0 / Remoto = 1:\n')
        if(len(entrada)>0):
            local_rem=entrada
        
        msg = '*E'+status+'0'+temp_sup+temp_inf+man_auto+local_rem+'0230#'
        
    if(ctr == 1):
        entrada = input('Temperatura (se positivo 2 casas decimais, senao 1 casa):\n')
        if(len(entrada)>0):
            temp=entrada
            
        entrada = input('Umidade:\n')
        if(len(entrada)>0):
            umid=entrada
            
        msg = '*'+temp+umid+'0000230#'
    if(ctr == 4):
        msg = '9990000000000000'
    if(ctr == 3):
        msg = '7770000000000000'
    if(ctr == 5):
        msg = '0000000000000000'
        
    print('Mensagem enviado para a raspi')
    print(msg)
    ser.write(msg.encode())
    '''  
    if(ctr == 4 or ctr == 3):
        sleep(7)
        limpar ='0000000000000000' 
        ser.write(limpar.encode())
        print(limpar)
    '''
    

