$(document).ready(function(){
    //aplicando calendario
    $("#id_fecha_nacimiento").datepicker({
        dateFormat:'yy-mm-dd',
    });
    $("#id_sucursal").select2();
    //enmascarando todos los input con jquery-mask
    $("#id_fecha_nacimiento").mask("0000-00-00");
    $("#id_telefono").mask("0000-0000");
    $("#id_dui").mask("00000000-0");
    $("#id_nit").mask("0000-000000-000-0");

});