$(document).ready(function(){
    $("#monto_apertura").on('input', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });
    $("#monto_apertura").keyup(function(evt){
        let monto_de_apertura=parseFloat($(this).val());
        let corte_anterior=parseFloat($("#corte_anterior").val());
        let diferencia= redondear((corte_anterior-monto_de_apertura));
        if($(this).val().length==0){
            $("#mostrar_cuadratura").text("Debe de contar el dinero en caja y contarlo y luego ingresar el monto para aperturar caja")
        }else{
            if(diferencia<0){
                $("#mostrar_cuadratura").text("No cuadra! hay un SOBRANTE en caja de $"+diferencia)
            } else if(diferencia>0){
                $("#mostrar_cuadratura").text("No cuadra! hay un FALTANTE en caja de $"+diferencia)
            }else if(diferencia==0){
                $("#mostrar_cuadratura").text("El dinero en caja esta CUADRADO la diferencia es $"+diferencia)
            }
        }

        
    });

    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }
})