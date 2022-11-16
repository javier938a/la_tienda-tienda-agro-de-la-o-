$(document).ready(function(){
    $("#fecha_inicio").datepicker({
        dateFormat:'yy-mm-dd',
    });
    $("#fecha_inicio").mask('0000-00-00');

    $("#fecha_final").datepicker({
        dateFormat:'yy-mm-dd',
    });
    $("#fecha_final").mask('0000-00-00');
    //generando el reporte
    $("#tipo_reporte").select2();
    $("#id_sucursal").select2();
    $("#frm_reporte_apertura").submit(function(evt){
        
        let fecha_inicial=$("#fecha_inicio").val();
        let fecha_final=$("#fecha_final").val();
        let id_sucursal=$("#id_sucursal").val();
        let tipo_reporte=$("#tipo_reporte").val();
        if(fecha_inicial.length>0 && fecha_final.length>0){
            if(tipo_reporte=="0"){

            }else if(tipo_reporte=="1"){
                if(id_sucursal!=0){

                }else{
                    toastr['warning']("Debe de seleccionar una sucursal para generar este reporte!!");
                    evt.preventDefault();
                }
            }
        }else{
            toastr['warning']("Debe de Ingresar la fecha de inicio y fin del reporte de ventas que quieres generar")
            evt.preventDefault();
        }

        /*
        if(fecha_final !='' && fecha_inicial!=''){
            evt.preventDefault();
            toastr['warning']("Debe de llenar los dos campos de fecha");
        }*/

    })
    
    $("#tipo_reporte").change(function(){
        let tipo_reporte=$("#tipo_reporte").val();
        console.log(tipo_reporte)
        if(tipo_reporte=="1"){
            $("#list_sucursal").css({
                'display':'block',
            });
        }else if(tipo_reporte=="0"){
            $("#id_sucursal").val("0");
            $("#list_sucursal").css({
                'display':'none',
            });  
        }
    })

})