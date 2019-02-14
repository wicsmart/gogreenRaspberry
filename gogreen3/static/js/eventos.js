 /*
 $.ajax({
            url: '/lastsensein/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $( "#temperatura" ).text( "Temperatura: " + data.temperatura + " °" );
                $( "#umidade" ).text("Umidade: " + data.umidade + " %" );
            }
   });
   
    $.ajax({
            url: '/lastsenseout/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $( "#temperaturaOut" ).text("Temperatura: " + data.temperatura + " °");
                $( "#umidadeOut" ).text("Umidade: " + data.umidade + " %");
            }
   });
     setInterval(function() {
        $.ajax({
            url: '/lastsensein/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $( "#temperatura" ).text( "Temperatura: " + data.temperatura + " °");
                $( "#umidade" ).text("Umidade: " + data.umidade + " %");
            }
        });

        $.ajax({
            url: '/lastsenseout/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
               $( "#temperaturaOut" ).text( "Temperatura : " + data.temperatura + " °");
                $( "#umidadeOut" ).html("Umidade : " + data.umidade + " %" );
            }
        });

        },30000);
*/
function abrir(){
info = {acao: 'abrir'};
    $.ajax({
       type: "POST",
       url: "/acao/",
       dataType: 'json',
       data: info,
       success: function() {
            alert('Aguardando a luminete ser aberta');
       },
       failure: function(data){
            alert('Nao foi possivel comunicar-se com o sistema');
        }
    });
}


function fechar(){
 info = {acao: 'fechar'};
     $.ajax({
          type: "POST",
          url: "/acao/",
          dataType: 'json',
          data: info,
           success: function() {

                alert('Aguardando a luminete ser fechada');
           },
           failure: function(data){
                alert('Nao foi comunicar-se com o sistema');
            }
        });
}

