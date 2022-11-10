function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    $("#monto_apertura").on('input', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });
    $("#monto_apertura").keyup(function(evt){
        let monto_de_apertura=parseFloat($(this).val());
        let corte_anterior=parseFloat($("#corte_anterior").val());
        let diferencia= redondear((corte_anterior-monto_de_apertura));
        let estado_primeravez=$("#estado_primeravez").val();
        if(estado_primeravez=="ninguno"){
            if(!isNaN(monto_de_apertura)){
                $("#mostrar_cuadratura").text("como es primera vez que abre apertura usted iniciara el dia con $"+monto_de_apertura);
            }else{
                $("#mostrar_cuadratura").text("Aun no se ha realizado ninguna apertura de caja ");  
            }
        }else{
            $("#diferencia_oculta").val(diferencia);
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
        }
        
    });
    $("#btn_efectuar_apertura").click(function(evt){
        evt.preventDefault();
        let diferencia= parseFloat($("#diferencia_oculta").val())
        let estado_primeravez=$("#estado_primeravez").val();
        alert(estado_primeravez)
        if(estado_primeravez!="ninguno"){
            if(diferencia==0){
                let url_efectuar_apertura=$("#url_efectuar_apertura").val()
                let monto_de_apertura=$("#monto_apertura").val();
                const csrftoken=getCookie('csrftoken');
                let datos={
                    csrfmiddlewaretoken:csrftoken,
                    'monto_de_apertura':monto_de_apertura
                }
                $.ajax({
                    url:url_efectuar_apertura,
                    type:'POST',
                    data:datos,
                    dataType:'json',
                    success:function(data){
                        console.log(data)
                        let res = data.res;
                        if(res==true){
                            toastr['success']("Apertura realizada correctamente!");
                            let url_listar_apertura_corte=$("#url_listar_apertura_corte").val();
                            window.open(url_listar_apertura_corte, '_parent');
                        }else{
                            toastr['warning']("Hubo un error de sistema favor consulte con soporte tecnico");
                        }
                    }
                });
            }else{
               toastr['error']("Para realizar apertura la apertura la diferencia debe de ser cero") 
            }
        }else{
            let url_efectuar_apertura=$("#url_efectuar_apertura").val()
            let monto_de_apertura=$("#monto_apertura").val();
            const csrftoken=getCookie('csrftoken');
            let datos={
                csrfmiddlewaretoken:csrftoken,
                'monto_de_apertura':monto_de_apertura
            }
            $.ajax({
                url:url_efectuar_apertura,
                type:'POST',
                data:datos,
                dataType:'json',
                success:function(data){
                    console.log(data)
                    let res = data.res;
                    if(res==true){
                        toastr['success']("Apertura realizada correctamente!");
                        let url_listar_apertura_corte=$("#url_listar_apertura_corte").val();
                        window.open(url_listar_apertura_corte, '_parent');
                    }else{
                        toastr['warning']("Hubo un error de sistema favor consulte con soporte tecnico");
                    }
                }
            });
        }
    });

    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }
})