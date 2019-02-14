import serial
from datetime import datetime
import select
import json
import publishers as pub
import sender as post
from time import sleep

ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
limpar = '0000000000000000'
p_medida = '666'
p_status = '777'
#*010000 +231  4T  6435   U349V100NS00000001#
# 123456 78910     111213
def formata_medida_fractum(msg):
    end =msg[32:35]
    temp = msg[7:10] + '.' + msg[10]
    umid = msg[13:15] + '.' + msg[15]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sense = { 
    "sense": 
    {"temperatura": temp,
        "umidade": umid,
        "luz": "0",
        "time": timestamp
    },
    "estado": 
	{"status": "null",
	  "manual":'null',
	  "local":'null',
      "created": "null"
    },
    "setup": 
	{"temp_min": "null",
      "temp_max": "null"
    },
    "end":end
} 
    senseString = json.dumps(sense)
    return senseString


def formata_medida(msg):
    end = msg[-4:-4+3]
    if(msg[1]=='-'):
        temp = msg[1:4] + '.' + msg[4]
        umid = msg[5:7] + '.' + msg[7]
    else:
        temp = msg[1:3] + '.' + msg[3]
        umid = msg[5:7] + '.' + msg[7]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sense = { 
    "sense": 
    {"temperatura": temp,
        "umidade": umid,
        "luz": "0",
        "time": timestamp
    },
    "estado": 
	{"status": "null",
	  "manual":'null',
	  "local":'null',
      "created": "null"
    },
    "setup": 
	{"temp_min": "null",
      "temp_max": "null"
    },
    "end":end
} 
    senseString = json.dumps(sense)
    return senseString
   
def formata_status(msg):
    st = msg[2]
    lr = msg[10]
    sup = msg[4:6]+'.'+msg[6]
    inf = msg[7:9]+'.'+msg[9]
    man = msg[10]
    loc = msg[11]
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = { 
    "sense": 
    {"temperatura": "nul",
        "umidade": "nul",
        "luz": "0",
        "time": "nul"
    },
    "estado": 
	{"status": st,
	  "manual":man,
	  "local":loc,
      "created": timestamp
    },
    "setup": 
	{"temp_max": sup,
      "temp_min": inf,
      "created": timestamp
    },
    "end":"null"
	}
    statusString = json.dumps(status)
    return statusString
    
erro = "b'*0\x00\x00\x000\x00\xad\xa20000230#"
try:
    while True:
        res = ser.readline()
        if res:
            #print(res)
            try:
                res = res.decode()
                #print(res)
                #print(res[0:4])
                #print(str(len(res)))
                if(res != '[Errno 111] Connection refused'):
                    if(res[:0+2] == '*E'):
                        ser.write(limpar.encode())
                        #print(limpar)
                        status = formata_status(res)
                        pub.publicar_sense_local(status)
                        pub.save_log_local(status)
                        pub.save_status_local(status)
                        pub.save_setup_local(status)                
                        post.status(status)
                        post.log_status(status)
                      
                    elif(len(res)==38 and (res[0:3]== '*01')):
                        sense = formata_medida_fractum(res)
                        pub.publicar_sense_local(sense)
                        pub.salvar_sense_local(sense)
                        post.medida_out(sense)
                        sleep(3)
                        ser.write(p_medida.encode())
                        #print(p_medida)
                        
                    elif(len(res)==39 and (res[1:4]== '*01')):
                        sense = formata_medida_fractum(res)
                        pub.publicar_sense_local(sense)
                        pub.salvar_sense_local(sense)
                        post.medida_out(sense)
                        sleep(3)
                        ser.write(p_medida.encode())
                        #print(p_medida)
                        
                    elif(len(res)==17 and res[0:2]!='*C' and res[-1] == '#'):
                        print('leitura medida')
                        ser.write(limpar.encode())
                        #print(limpar)
                        sense = formata_medida(res)
                        pub.publicar_sense_local(sense)
                        pub.salvar_sense_local(sense)
                        post.medida_in(sense)
                        sleep(3)
                        ser.write(p_status.encode())
                        #print(p_status)
                        
                
            except Exception as e:
                ser.write(limpar.encode())
                print('medida estufa lida')
                resp='*224488990000230#'
                
                #print(limpar)
                sense = formata_medida(resp)
                pub.publicar_sense_local(sense)
                pub.salvar_sense_local(sense)
                post.medida_in(sense)
                sleep(3)
                ser.write(p_status.encode())
                #print(p_status)
                
except KeyboardInterrupt:
    print('Processo finalizado\n')

  #  time.sleep(2)

