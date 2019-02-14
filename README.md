O arquvio gogreen3/script.sh é executado no boot para iniciar o django local para ser usado caso não tenha internet

O arquivo gogreen3/script2.sh também executado no boot para deixar dois processos rodando
  gateway.py lê as entradas da serial da rasberry
  subscriber_local.py é um cliente mqtt que escuta as ações do usuário na página html e salva essas ações localmente
  
 O arquivo gg/gpio.py é executado somente uma vez para dar um pulso no pino 15 da respberry para poder utilizar os rádio acoplado nela
