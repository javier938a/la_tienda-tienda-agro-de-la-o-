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
    $("#id_categoria").select2();
    $("#id_sucursal").select2();
    $("#frm_reporte_inventario").submit(function(evt){
        
        let fecha_inicial=$("#fecha_inicio").val();
        let fecha_final=$("#fecha_final").val();
        let id_sucursal=$("#id_sucursal").val();
        let id_categoria=$("#id_categoria").val();
            if(parseInt(id_sucursal)>0 || parseInt(id_categoria)>0){

            }else{
                toastr['warning']("Debe de seleccionar una categoria o una sucursal para generar el reporte");
                evt.preventDefault(); 
            }
    

        /*
        if(fecha_final !='' && fecha_inicial!=''){
            evt.preventDefault();
            toastr['warning']("Debe de llenar los dos campos de fecha");
        }*/

    });
})