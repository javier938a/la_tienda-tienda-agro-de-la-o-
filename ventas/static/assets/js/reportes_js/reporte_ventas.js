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
    $("#frm_reporte_venta").submit(function(evt){
        
        let fecha_inicial=$("#fecha_inicio").val();
        let fecha_final=$("#fecha_final").val();
        if(fecha_inicial.length>0 && fecha_final.length>0){
            
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

})