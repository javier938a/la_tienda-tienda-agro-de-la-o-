$(document).ready(function(){
    var url_chart = $("#url_chart_hoy").val();
    if(url_chart != undefined){
        var options = {
            chart: {
                height: 350,
                type: 'bar',
            },
            dataLabels: {
                enabled: false
            },
            series: [],
            title: {
                text: 'Reporte de venta diario...',
            },
            noData: {
              text: 'Loading...'
            }
          }
        let grafico=new ApexCharts(
            document.querySelector("#reportsChart"), 
            options
        )
        grafico.render();
    
        $.getJSON(url_chart, function(response) {
          grafico.updateSeries([{
            name: 'Venta',
            data: response
          }])
        });
    }
});
                    