$(document).ready(function(){
    $("#eliminar_producto_en_inventario").submit(function(evt){
        let cantidad_disponible= parseInt($("#cantidad_disponible").val());

        if(cantidad_disponible==0){

        }else{
            toastr['error']("No puede eliminar este producto en el inventario, Aun quedan Stock para este producto, para poder eliminarla debe tener stock '0'!!")
            evt.preventDefault();
        }
        
    });
});