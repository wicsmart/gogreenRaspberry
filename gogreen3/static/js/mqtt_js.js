
var mqtt;
var reconnectTimeout = 200;
var host="127.0.0.1";
var port=9001;		
		
function onFailure(message) {
			console.log("Connection Attempt to Host "+host+"Failed");
			setTimeout(MQTTconnect, reconnectTimeout);
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function onMessageArrived(msg){
	var checker = $('#automan');
			out_msg="Message received "+msg.payloadString;
			var obj = JSON.parse(msg.payloadString);
			console.log(obj);
			if(obj.estado.local == "0" || obj.estado.local == "1"){
				addLog(obj.estado);
			}
			if(obj.estado.local == 1){
				str = "<h2 style='float: center' align='center' ><span class='glyphicon glyphicon-refresh'"+
						"style='color:green'></span>ATUAÇÃO</h2>";
				$('#rem_auto').html(str);
				$('#comandos').show();
				$('#limites').show();
			}else if(obj.estado.local == 0){
				str = "<h2 style='float: center' align='center'>Comandos localmente dentro da Estufa</h2>";
				$('#rem_auto').html(str);
				$('#comandos').hide();		
				$('#limites').hide();				
			}
				
			if(obj.estado.manual == "1"){
				$('#auto_man').text('AUTOMÁTICO');
				$('#man').prop('disabled',false);
				$('#auto').prop('disabled',true);
				$('.aguardar').hide();
				$('.mostra').hide();
			}else if(obj.estado.manual == "0"){
				$('#auto_man').text('MANUAL');
				$('#man').prop('disabled',true);
				$('#auto').prop('disabled',false);
				$('.aguardar').hide();
				$('.mostra').show();
			}
			if(obj.setup.min_temp != null){
				
				inf = obj.setup.temp_min;
				sup = obj.setup.temp_max;
				$("#min_temp").val(inf);
				$("#max_temp").val(sup);
				console.log(inf);
			}
			if (obj.estado.status == "1"){
				$("#abrir").prop('disabled',false);
				$("#fechar").prop('disabled',true);
				message = ('<strong>ALUMINET ESTA ESTENDIDA</strong>');
				$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>');
			
			}else if(obj.estado.status == "0"){
				$("#abrir").prop('disabled',true);
				$("#fechar").prop('disabled',false);
				message = ('<strong>ALUMINET ESTA RECOLHIDA</strong>');
				$('#alert_placeholder').html('<div class="alert alert-success" align="center"><span>'+message+'</span></div>');
			
			}else if(obj.estado.status == "2"){
				$("#abrir").prop('disabled',true);
				$("#fechar").prop('disabled',true);
				message = ('<strong>ALUMINET ESTA EM TRANSIÇÃO</strong>');
				$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
			}else if(obj.estado.status == "3"){
				$("#abrir").prop('disabled',true);
				$("#fechar").prop('disabled',true);
				message = ('<strong>ALUMINET ESTA INDEFINIDA</strong>');
				$('#alert_placeholder').html('<div class="alert alert-warning" align="center"><span>'+message+'</span></div>');
			}else if(obj.end == "230"){
				$('#temperatura').html(obj.sense.temperatura+'°C');
				$('#umidade').html(obj.sense.umidade+ '%');
			}else if(obj.end == "001"){
				temp=obj.sense.temperatura;
				aux =  temp.replace("+","");
				$('#temperaturaOut').html(aux+'°C');
				$('#umidadeOut').html(obj.sense.umidade + '%');
			}
}

function addLog(estado){
	var msgLog;
	var t = $('#tabelaLog').DataTable();
    if(estado.status == "0") msgLog = "Estendido";
    if(estado.status == "1") msgLog = "Recolhido";
    if(estado.status == "2") msgLog = "Transição";
    if(estado.status == "3") msgLog = "Indefinido";
    
    t.row.add([
        msgLog,
        estado.created
    ]).draw( false );
}

function onConnect() {
		mqtt.subscribe('status');
		console.log("subscribed on status");
}

function MQTTconnect() {
		console.log("connecting to "+ host +" "+ port);
		mqtt = new Paho.MQTT.Client(host,port,"clientjs");
		var options = {
			timeout: 3,
			onSuccess: onConnect,
			onFailure: onFailure
			 };
		mqtt.onMessageArrived = onMessageArrived;
		mqtt.onConnectionLost = onConnectionLost;
		mqtt.connect(options); //connect
}

MQTTconnect();

function publicar_acao(com){
	console.log(com);
	message = new Paho.MQTT.Message(com.toString());
	message.destinationName = "acao";
	mqtt.send(message);
	
}

function publicar_setup(setup){
	console.log(setup);
	message = new Paho.MQTT.Message(setup.toString());
	message.destinationName = "setup";
	mqtt.send(message);
}
	
function publicar_manual(man){
	console.log(man);
	message = new Paho.MQTT.Message(man.toString());
	message.destinationName = "manual";
	mqtt.send(message);
}
	
	
	
	
	
	var dateFormat = function () {
    var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
        timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
        timezoneClip = /[^-+\dA-Z]/g,
        pad = function (val, len) {
            val = String(val);
            len = len || 2;
            while (val.length < len) val = "0" + val;
            return val;
        };

    // Regexes and supporting functions are cached through closure
    return function (date, mask, utc) {
        var dF = dateFormat;

        // You can't provide utc if you skip other args (use the "UTC:" mask prefix)
        if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
            mask = date;
            date = undefined;
        }

        // Passing date through Date applies Date.parse, if necessary
        date = date ? new Date(date) : new Date;
        if (isNaN(date)) throw SyntaxError("invalid date");

        mask = String(dF.masks[mask] || mask || dF.masks["default"]);

        // Allow setting the utc argument via the mask
        if (mask.slice(0, 4) == "UTC:") {
            mask = mask.slice(4);
            utc = true;
        }

        var _ = utc ? "getUTC" : "get",
            d = date[_ + "Date"](),
            D = date[_ + "Day"](),
            m = date[_ + "Month"](),
            y = date[_ + "FullYear"](),
            H = date[_ + "Hours"](),
            M = date[_ + "Minutes"](),
            s = date[_ + "Seconds"](),
            L = date[_ + "Milliseconds"](),
            o = utc ? 0 : date.getTimezoneOffset(),
            flags = {
                d:    d,
                dd:   pad(d),
                ddd:  dF.i18n.dayNames[D],
                dddd: dF.i18n.dayNames[D + 7],
                m:    m + 1,
                mm:   pad(m + 1),
                mmm:  dF.i18n.monthNames[m],
                mmmm: dF.i18n.monthNames[m + 12],
                yy:   String(y).slice(2),
                yyyy: y,
                h:    H % 12 || 12,
                hh:   pad(H % 12 || 12),
                H:    H,
                HH:   pad(H),
                M:    M,
                MM:   pad(M),
                s:    s,
                ss:   pad(s),
                l:    pad(L, 3),
                L:    pad(L > 99 ? Math.round(L / 10) : L),
                t:    H < 12 ? "a"  : "p",
                tt:   H < 12 ? "am" : "pm",
                T:    H < 12 ? "A"  : "P",
                TT:   H < 12 ? "AM" : "PM",
                Z:    utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
                o:    (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
                S:    ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
            };

        return mask.replace(token, function ($0) {
            return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
        });
    };
}();

// Some common format strings
dateFormat.masks = {
    "default":      "ddd mmm dd yyyy HH:MM:ss",
    shortDate:      "m/d/yy",
    mediumDate:     "mmm d, yyyy",
    longDate:       "mmmm d, yyyy",
    fullDate:       "dddd, mmmm d, yyyy",
    shortTime:      "h:MM TT",
    mediumTime:     "h:MM:ss TT",
    longTime:       "h:MM:ss TT Z",
    isoDate:        "yyyy-mm-dd",
    isoTime:        "HH:MM:ss",
    isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",
    isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
};

// Internationalization strings
dateFormat.i18n = {
    dayNames: [
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ],
    monthNames: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ]
};

// For convenience...
Date.prototype.format = function (mask, utc) {
    return dateFormat(this, mask, utc);
};
