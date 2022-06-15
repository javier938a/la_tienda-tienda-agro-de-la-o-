$(document).ready(function(){
    $("#id_proveedor").select2();
    $("#id_categoria").select2();
    $("#id_fecha_vencimiento").datepicker({
        dateFormat:'yy-mm-dd',
    });
    $("#id_fecha_vencimiento").mask("0000-00-00");
 
});