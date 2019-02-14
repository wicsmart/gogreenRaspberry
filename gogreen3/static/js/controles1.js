//Function that enables or disables the local/remote and open/close controls if that system is on automatic or manual
$(function(){

	$('.mostra').hide();
	$.ajax({
            url: '/freshData/',
            type: 'get',
            dataType: 'json',
            success: function (data) { 
				console.log(data);
				$('#temperaturaOut').text(data.senseout.temperatura);
				$('#umidadeOut').text(data.senseout.umidade);
				$('#umidade').text(data.sensein.temperatura);
				$('#temperatura').text(data.sensein.umidade);
				console.log(data.status);
				if(data.status.status == 0){
					message = ('<strong>FECHADA:</strong> Aluminet está fechada.');
					$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.status == 1){
					message =('<strong>ABERTA:</strong> Aluminet está aberta.');
					$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.status == 2){
					message = ('<strong>TRANSIÇÃO:</strong> Aluminet está abrindo.');
					$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
				}
				if(data.status.status == 3){
					message = ('<strong>TRANSIÇÃO:</strong> Aluminet está fechando.');
					$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
				}
				$("#max_temp").txt(data.setup.temp_max);
				$("#min_temp").val(data.setup.temp_min);
				$("#max_umid").val(data.setup.umid_max);
				$("#min_umid").val(data.setup.umid_min);

			}			
		});
	var checker = $('#automan');
	var local = $('#localrem');
	var open = $('#abrir');
	var close = $('#fechar');
	
	
	checker.change(function(){
		if(checker.is(':checked')){
	    	$('.mostra').hide();
		} else {
	    	$('.mostra').show();
		}

	});

	local.change(function(){
		if(local.is(':checked')){
			//opções de atuação no modo LOCAL
		} else {
			//opções de atuação no modo REMOTO
		}
	});

});


//Alerts saying what is happening with the ALUMINET
document.getElementById("abrir").addEventListener("click", function(){
    alert("ALUMINET ESTÁ ABRINDO.");
});

document.getElementById("fechar").addEventListener("click", function(){
    alert("ALUMINET ESTÁ FECHANDO.");
});

function open_aluminet(){
	console.log('teste_open');
}

function close_aluminet(){
	console.log('teste_close');
}


//ALERTAS: ABERTO, FECHADO, TRANSIÇÃO
bootstrap_alert = function() {}

bootstrap_alert.warning = function(message) {
	$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>')
}

$('#abrir').on('click', function() {
    bootstrap_alert.warning('<strong>TRANSIÇÃO:</strong> Aluminet está abrindo.');
});

$('#fechar').on('click', function() {
    bootstrap_alert.warning('<strong>TRANSIÇÃO:</strong> Aluminet está fechando.');
});


// bootstrap_alert.success = aberta(message) {
// 	$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>')
// }

//  function aberta() {
//     bootstrap_alert.warning('<strong>ABERTA:</strong> Aluminet está aberta.');
// }

// bootstrap_alert.danger = function(message) {
// 	$('#alert_placeholder').html('<div class="alert alert-danger" align="center"><span>'+message+'</span></div>')
// }

// function fechada() {
//     bootstrap_alert.warning('<strong>FECHADA:</strong> Aluminet está fechada.');
// }



//Load the limits on disabled mode	
	$("#max_temp").prop('disabled',true);
	$("#min_temp").prop('disabled',true);
	$("#max_umid").prop('disabled',true);
	$("#min_umid").prop('disabled',true);


//Global variables to manage the forms of max/min temperature and humidity
var v_max_temp = $("#max_temp").val();
var v_min_temp = $("#min_temp").val();
var v_max_umid = $("#max_umid").val();
var v_min_umid = $("#min_umid").val();


//Enable or disable the form fields
function disable_values() {

    $("#max_temp").prop('disabled',true);
	$("#min_temp").prop('disabled',true);
	$("#max_umid").prop('disabled',true);
	$("#min_umid").prop('disabled',true); 

    v_max_temp = $("#max_temp").val();
	v_min_temp = $("#min_temp").val();
	v_max_umid = $("#max_umid").val();
	v_min_umid = $("#min_umid").val();


    // if (v_max_temp <= v_min_temp) {
    // 	alert('O limite máximo de temperatura é menor ou igual ao limite mínimo!');
    // 	}


    // if (v_max_umid <= v_min_umid) {
    // 	alert('O limite máximo de umidade é menor ou igual ao limite mínimo!');
    // 	}


    //Enviar os valores
}


//Function that enables the edition of the forms
function enable_values() {

    $("#max_temp").prop('disabled',false);
	$("#min_temp").prop('disabled',false);
	$("#max_umid").prop('disabled',false);
	$("#min_umid").prop('disabled',false);
}


//Function that cancel the changes made and fetch the last value changed
function cancel_values() {

	$("#max_temp").val(v_max_temp);
	$("#min_temp").val(v_min_temp);
	$("#max_umid").val(v_max_umid);
	$("#min_umid").val(v_min_umid);

	$("#max_temp").prop('disabled',true);
	$("#min_temp").prop('disabled',true);
	$("#max_umid").prop('disabled',true);
	$("#min_umid").prop('disabled',true);
}


// $(":input").bind('blur', function () {
    	
//     		alert('O limite máximo de temperatura é menor ou igual ao limite mínimo!');
    	            
// 	});


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


//Check if max humidity is greater than the min humidity
$("#max_umid").focusout(function(){
    
    
    if(parseFloat($("#min_umid").val()) >= parseFloat($("#max_umid").val()))
    {
        alert('O limite máximo de umidade é menor ou igual ao limite mínimo!');
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
            },
            max_umidade: {
                row: '.col-sm-3',
                validators: {
                    notEmpty: {
                        message: 'É necessário ter um valor para o limite máximo de umidade!'
                    }
                }
            },
            min_umidade: {
                row: '.col-sm-3',
                validators: {
                    notEmpty: {
                        message: 'É necessário ter um valor para o limite mínimo de umidade!'
                    }
                }
            }
        }
    });
});
