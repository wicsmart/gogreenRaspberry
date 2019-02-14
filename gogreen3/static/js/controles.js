//Function that enables or disables the local/remote and open/close controls if that system is on automatic or manual
$(function(){

	$('.mostra').hide();
	$('.aguardar').hide();
	$('#cancelar').hide();
	$('#alterar').hide();
	$.ajax({
            url: '/freshData/',
            type: 'get',
            dataType: 'json',
            success: function (data) { 
				console.log(data);
				$('#temperaturaOut').text(data.senseout.temperatura + '°C');
				$('#umidadeOut').text(data.senseout.umidade + '%');
				$('#umidade').text(data.sensein.umidade + '°C');
				$('#temperatura').text(data.sensein.temperatura + '%');
				console.log(data.status);
				if(data.status.status == 1){
					$("#fechar").prop('disabled',true);
					$("#abrir").prop('disabled',false);

					message = ('<strong>ALUMINET ESTÁ ESTENDIDA</strong>');
					$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.status == 0){
					$("#abrir").prop('disabled',true);
					$("#fechar").prop('disabled',false);
					message =('<strong>ALUMINET ESTÁ RECOLHIDA</strong>');
					$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.status == 2){
					$("#fechar").prop('disabled',true);
					$("#abrir").prop('disabled',true);
					message = ('<strong>ALUMINET ESTÁ EM TRANSIÇÃO</strong>');
					$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.status == 3){
					$("#fechar").prop('disabled',true);
					$("#abrir").prop('disabled',true);
					message = ('<strong>ALUMINET ESTÁ INDEFINIDA</strong>');
					$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.manual == 1){
					$('#auto_man').text('AUTOMÁTICO');
					$('#man').prop('disabled',false);
					$('#auto').prop('disabled',true);
					$('.aguardar').hide();
					$('.mostra').hide();
				}else if(data.status.manual == 0){
					$('#auto_man').text('MANUAL');
					$('#man').prop('disabled',true);
					$('#auto').prop('disabled',false);
					$('.aguardar').hide();
					$('.mostra').show();
				}
				if(data.status.local == 1){
					str = "<h2 style='float: center' align='center' ><span class='glyphicon glyphicon-refresh'"+
						"style='color:green'></span>ATUAÇÃO</h2>";
					$('#rem_auto').html(str);
					$('#comandos').show();
					$('#limites').show();
				}else if(data.status.local == 0){
					str = "<h2 style='float: center' align='center'>Comandos localmente dentro da Estufa</h2>";
					$('#rem_auto').html(str);
					$('#comandos').hide();		
					$('#limites').hide();				
				}
				$("#min_temp").val(data.setup.temp_min);
				$("#max_temp").val(data.setup.temp_max);
			}			
		});
		
	var table = $(".display tbody");

	$.ajax({
            url: '/log/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
				array = parseLog(data);
				table.empty();
				$.each(array, function(index, value) {
					 table.append("<tr><td>"+value.evento+"</td>" +
                    "<td>"+value.data+"</td>"+ "</td></tr>");
				});
				 $(".display").DataTable( {
					 "order": [[ 1, "desc" ]]
					} );
			}	
		});

// eventosBotoes();
});

function parseLog(data){
	var logs = [];
		
	for(var i in data){
		var item = data[i];
		if(item.status == "0")
			logs.push({"evento": "Recolhida", "data": item.created});
		else if(item.status == "1")
			logs.push({"evento": "Estendida", "data": item.created});
		else if(item.status == "2")
			logs.push({"evento": "Transição", "data": item.created});
		else if (item.status == "3")
			logs.push({"evento": "Indefinido", "data": item.created});
		if(item.acao == "0")
			logs.push({"evento": "Comando Recolher", "data": item.created});
		else if(item.acao == "1")
			logs.push({"evento": "Comando Estender", "data": item.created});
	}
	return logs;
}

function eventosBotoes(){
	
	var checker = $('#automan');
	var local = $('#localrem');
	var open = $('#abrir');
	var close = $('#fechar');

	checker.change(function(){
		if(checker.is(':checked')){
			if ( $('.aguardar').css('display') == 'none' ){
				publicar_manual(1);
			}
	    	$('.mostra').hide();
	    	$('.aguardar').show();
	    	$('#man').prop('disabled',false);
			$('#auto').prop('disabled',false);
		
		}else {
			if ( $('.aguardar').css('display') == 'none' ){
				publicar_manual(0);
			}
	    	$('.aguardar').show();
	    	$('#man').prop('disabled',false);
			$('#auto').prop('disabled',false);
		}
	});
	
	local.change(function(){
		if(local.is(':checked')){
			//opções de atuação no modo LOCAL
		} else {
			//opções de atuação no modo REMOTO
		}
	});
}


function addLogAcao(el){
  /*    
	var msgLogAcao;
	var t = $('#tabelaLog').DataTable();
    if(msgAcao == "0") msgLogAcao = "Comando Abrir";
    else msgLogAcao = "Comando Fechar";
  
    t.row.add([
        msgLogAcao,
        estado.created
    ]).draw( false );
    */
}
 function ativar_man(){
	 	
	publicar_manual(0);
    $(".aguardar").show();
    $(".mostrar").hide();

}

 function ativar_auto(){
	 	
	publicar_manual(1);
    $(".aguardar").show();
    $(".mostrar").hide();

}
   
    
function open_aluminet(){
	
	publicar_acao(0);
	alert("ALUMINET ESTÁ ABRINDO.");
    $("#abrir").prop('disabled',true);
    $("#fechar").prop('disabled',true);
  //  message = ('<strong>TRANSIÇÃO:</strong> Aluminet está abrindo.');
//	$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
	addLogAcao(0);
}

function close_aluminet(){
	
	publicar_acao(1);
	alert("ALUMINET ESTÁ FECHANDO.");
    $("#fechar").prop('disabled',true);
    $("#abrir").prop('disabled',true);
  //  message = ('<strong>TRANSIÇÃO:</strong> Aluminet está fechando.');
	//$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
	addLogAcao(1);
	
}


//ALERTAS: ABERTO, FECHADO, TRANSIÇÃO
bootstrap_alert = function() {}

//Load the limits on disabled mode	
	$("#max_temp").prop('disabled',true);
	$("#min_temp").prop('disabled',true);

//Enable or disable the form fields
function disable_values() {

    $("#max_temp").prop('disabled',true);
	$("#min_temp").prop('disabled',true);

    v_max_temp = $("#max_temp").val();
	v_min_temp = $("#min_temp").val();
	if(v_max_temp.length == 1) max_temp = '0'+v_max_temp+'0';
	else if(v_max_temp.length == 2) max_temp = v_max_temp+'0';
	else {
		aux = v_max_temp.split(".");
		max_temp = aux[0]+aux[1];
	}
	if(v_min_temp.length == 1) min_temp = '0'+v_min_temp+'0';
	else if(v_min_temp.length == 2) min_temp = v_min_temp+'0';
	else {
		aux = v_min_temp.split(".");
		min_temp = aux[0]+aux[1];
	}
	console.log(v_max_temp);
	console.log(v_min_temp);

	setup = max_temp + min_temp;
	publicar_setup(setup);
	
	$('#cancelar').hide();
	$('#alterar').hide();
}


//Function that enables the edition of the forms
function enable_values() {

    $("#max_temp").prop('disabled',false);
	$("#min_temp").prop('disabled',false);
	
	$('#cancelar').show();
	$('#alterar').show();

}


//Function that cancel the changes made and fetch the last value changed
function cancel_values() {
	$.ajax({
            url: '/freshData/',
            type: 'get',
            dataType: 'json',
            success: function (data) { 
				$("#max_temp").val(data.setup.temp_max);
				$("#min_temp").val(data.setup.temp_min);
			}			
		});
	$("#max_temp").prop('disabled',true);
	$("#min_temp").prop('disabled',true);
	
	$('#cancelar').hide();
	$('#alterar').hide();
	
}

//Check if max temperature is greater than the min temperature
$("#max_temp").focusout(function(){
    
    
    if(parseFloat($("#min_temp").val()) >= parseFloat($("#max_temp").val()))
    {
        alert('O limite máximo de temperatura é menor ou igual ao limite mínimo!');
        $("#alterar").prop('disabled',true);
    }
    else {
        $("#alterar").prop('disabled',false);
    }
    
});

//Validates if the input form is empty
$(document).ready(function() {

    $('#registrationForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            max_temperatura: {
                row: '.col-sm-3',
                validators: {
                    notEmpty: {
                        message: 'É necessário ter um valor para o limite máximo de temperatura!'
                    }
                }
            },
            min_temperatura: {
                row: '.col-sm-3',
                validators: {
                    notEmpty: {
                        message: 'É necessário ter um valor para o limite mínimo de temperatura!'
                    }
                }
            }
        }
    });
});

//Function that scrolls smoothly by clicking when moving through options at the header bar
$(document).ready(function(){
  // Add smooth scrolling to all links
  $("a").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 800, function(){
   
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
});
