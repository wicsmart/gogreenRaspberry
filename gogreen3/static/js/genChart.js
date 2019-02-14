

getSenseIn();
getSenseOut();
getSenseInPie();
getSenseInAll();

function getSenseIn(){
    $.ajax({
            url: '/sensein/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
            temperaturaIn = new Array();
            umidadeIn = new Array();
              for(var i in data){
                timestamp = convertToTimestamp(data[i].time);
                temperaturaIn.push([timestamp, data[i].temperatura]);
                umidadeIn.push([timestamp, data[i].umidade]);
              }
              Highcharts.setOptions({
				time: {
					timezoneOffset: 3 * 60
				}
			});

    Highcharts.stockChart('d1', {
            title: {
                  text: 'Dentro da Estufa'
                  },
             plotOptions: {
             series: {
				animation: {
                duration: 2000
					}
				}
			},
          series:[{
                name: 'temperatura',
                data: temperaturaIn,
                 type: 'spline',
                tooltip: {
                    valueDecimals: 1,
                    valueSuffix: '°C'
                }
            },
            {
                name: 'umidade',
                data: umidadeIn,
                 type: 'spline',
                tooltip: {
                    valueDecimals: 1,
                    valueSuffix: '%'
                }
          }],
                chart: {
                events: {
                    load: function () {
                    var series1 = this.series[0];
                    var series2 = this.series[1];
                        setInterval(function () {
                            $.ajax({
                                url: '/lastsensein/',
                                type: 'get',
                                dataType: 'json',
                                success: function (data) {
                                    timestamp = convertToTimestamp(data.time);
                                    var x = timestamp,
                                    t = data.temperatura;
                                    series1.addPoint([x, t], true, true);
                                    u = data.umidade;
                                    series2.addPoint([x, u], true, true);

                                }
                            })
                        },300000);
                    }
                }
            },

            rangeSelector: {
              buttons: [{
                  count: 3,
                  type: 'day',
                  text: '3D'
              },{
                  count: 1,
                  type: 'week',
                  text: '1S'
              },
              {
                  count: 1,
                  type: 'month',
                  text: '1M'
              }, {
                  type: 'all',
                  text: 'all'
              }],
              selected: 2,
              inputEnabled: false

          },
           yAxis: {
            title: {
                text: 'Temperature (°C) e Umidade ( % )'
            }
         
        }
    });
          }
        });

}

function getSenseOut(){
    $.ajax({
        url: '/senseout/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            temperaturaOut = new Array();
            umidadeOut = new Array();
            for(var i in data){
                timestamp = convertToTimestamp(data[i].time);
                temperaturaOut.push([timestamp, data[i].temperatura]);
                umidadeOut.push([timestamp, data[i].umidade]);
            }
            Highcharts.setOptions({
				time: {
					timezoneOffset: 3 * 60
				}
			});
            Highcharts.stockChart('e1', {
            title: {
                  text: 'Ambiente Externo'
                  },
                   plotOptions: {
             series: {
				animation: {
                duration: 2000
					}
				}
			},

          series:[{
                name: 'temperatura',
                data: temperaturaOut,
               type: 'spline',
                tooltip: {
                    valueDecimals: 1,
                    valueSuffix: '°C'
                }
            },
            {
                name: 'umidade',
                data: umidadeOut,
                type: 'spline',
                tooltip: {
                    valueDecimals: 1,
                    valueSuffix: '%'
                }
          }],
                chart: {
                events: {
                    load: function () {
                    var series1 = this.series[0];
                    var series2 = this.series[1];
                        setInterval(function () {
                            $.ajax({
                                url: '/lastsenseout/',
                                type: 'get',
                                dataType: 'json',
                                success: function (data) {
                                    timestamp = convertToTimestamp(data.time);
                                    console.log(timestamp);
                                    console.log(data.temperatura);
                                    var x = timestamp,
                                    t = data.temperatura;
                                    series1.addPoint([x, t], true, true);
                                    u = data.umidade;
                                    series2.addPoint([x, u], true, true);

                                }
                            })
                        },300000);
                    }
                }
            },

            rangeSelector: {
              buttons: [{
                  count: 1,
                  type: 'day',
                  text: '3D'
              },{
                  count: 1,
                  type: 'week',
                  text: '1S'
              }, 
              {
                  count: 1,
                  type: 'month',
                  text: '1M'
              },{
                  type: 'all',
                  text: 'all'
              }],
              selected: 1,
              inputEnabled: false

          },
           yAxis: {
            title: {
                text: 'Temperature (°C) e Umidade ( % )'
            }
        }
    });
          }
        });
}




function getSenseInAll(){
    $.ajax({
            url: '/senseinall/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
            temperaturaIn = new Array();
            umidadeIn = new Array();
              for(var i in data){
                timestamp = convertToTimestamp(data[i].time);
                temperaturaIn.push([timestamp, data[i].temperatura]);
                umidadeIn.push([timestamp, data[i].umidade]);
              }
              Highcharts.setOptions({
				time: {
					timezoneOffset: 3 * 60
				}
			});

    Highcharts.stockChart('e3', {
            title: {
                  text: 'Histórico total dentro da Estufa'
                  },
             plotOptions: {
             series: {
				animation: {
                duration: 2000
					}
				}
			},
          series:[{
                name: 'temperatura',
                data: temperaturaIn,
                 type: 'spline',
                tooltip: {
                    valueDecimals: 1,
                    valueSuffix: '°C'
                }
            },
            {
                name: 'umidade',
                data: umidadeIn,
                 type: 'spline',
                tooltip: {
                    valueDecimals: 1,
                    valueSuffix: '%'
                }
          }],
                chart: {
                events: {
                    load: function () {
                    var series1 = this.series[0];
                    var series2 = this.series[1];
                        setInterval(function () {
                            $.ajax({
                                url: '/lastsensein/',
                                type: 'get',
                                dataType: 'json',
                                success: function (data) {
                                    timestamp = convertToTimestamp(data.time);
                                    var x = timestamp,
                                    t = data.temperatura;
                                    series1.addPoint([x, t], true, true);
                                    u = data.umidade;
                                    series2.addPoint([x, u], true, true);

                                }
                            })
                        },300000);
                    }
                }
            },

            rangeSelector: {
              buttons: [{
                  count: 3,
                  type: 'day',
                  text: '3D'
              },{
                  count: 1,
                  type: 'week',
                  text: '1S'
              },
              {
                  count: 1,
                  type: 'month',
                  text: '1M'
              }, {
                  type: 'all',
                  text: 'all'
              }],
              selected: 2,
              inputEnabled: false

          },
           yAxis: {
            title: {
                text: 'Temperature (°C) e Umidade ( % )'
            }
         
        }
    });
          }
        });

}


function getSenseInPie(){
    $.ajax({
       url: '/dadosPizza/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
            console.log(data);
            var chart = {
                renderTo: 'd2',
               plotBackgroundColor: null,
               plotBorderWidth: null,
               plotShadow: false
            };
          //  var colors = ['blue','green','red'];
            var title = {
               text: 'Temperatura - Operação dentro da faixa ideal'
            };
            var tooltip = {
               pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            };
        
            var plotOptions = {
               pie: {
                  allowPointSelect: true,
                  cursor: 'pointer',
				  colors: ['#33ccff', '#00cc00','#ff1a1a'],
                  dataLabels: {
                     enabled: true,
                     format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
                     style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor)||
                        'black'
                     }
                  }
               }
            };
            var series = [{
               type: 'pie',
               name: 'Faixa ideal',
               data: [
                  ['Abaixo',   data.tbaixo],
                  {
                     name: 'Dentro',
                     y: data.tdentro,
                     sliced: true,
                     selected: true
                  },
                  ['Acima',   data.tacima],
               ]
            }];
            var json = {};
            json.chart = chart;
            json.title = title;
            json.tooltip = tooltip;
            json.series = series;
            json.plotOptions = plotOptions;
            chart = new Highcharts.Chart(json);

//------------------ Umidade
            var chart1 = {
                renderTo: 'e2',
               plotBackgroundColor: null,
               plotBorderWidth: null,
               plotShadow: false
            };
             var title1 = {
               text: 'Umidade - Operação dentro da faixa ideal'
            };
            var series1 = [{
               type: 'pie',
               name: 'Faixa ideal',
               data: [
                  ['Abaixo',   data.ubaixo],
                  {
                     name: 'Dentro',
                     y: data.udentro,
                     sliced: true,
                     selected: true
                  },
                  ['Acima',   data.uacima],
               ]
            }];
		 var plotOptions1 = {
               pie: {
                  allowPointSelect: true,
                  cursor: 'pointer',
				  colors: ['#33ccff', '#00cc00','#ff1a1a'], 
                  dataLabels: {
                     enabled: true,
                     format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
                     style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor)||
                        'black'
                     }
                  }
               }
            };
            var json1 = {};
            json1.chart = chart1;
            json1.title = title1;
            json1.tooltip = tooltip;
            json1.series = series1;
            json1.plotOptions = plotOptions1;
            chart1 = new Highcharts.Chart(json1);

         }
       });
        }

function convertToTimestamp(time){
          dateTimeParts = time.split(' ');
          timeParts = dateTimeParts[1].split(':');
          dateParts = dateTimeParts[0].split('-');
          date = new Date(dateParts[0], parseInt(dateParts[1], 10) - 1, dateParts[2], timeParts[0], timeParts[1], timeParts[2]);
          return date.getTime();
}





