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
    $("#limpiar").click(function(evt){
        evt.preventDefault();
        $(".cantidad1_b").val("");
        $(".cantidad2_b").val("");
        $(".cantidad1_m").val("");
        $(".cantidad2_m").val("");
        $("#total_billete").val("$0.0");
        $("#total_moneda").val("$0.0");
        $("#total_billete_moneda").val("$0.0");
        $("#id_total_en_grande").val("$0.0");
    });
    $("#tipo_transaccion").select2();
    //validando las cantidades a que solo pueda ingresar solo numeros
    $(document).on('input', '.cantidad1_b', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });
    $(document).on('input', '.cantidad2_b', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });

    $(document).on('input', '.cantidad1_m', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });
    $(document).on('input', '.cantidad2_m', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });
    $("#btn_guardar_transaccion").click(function(evt){
        evt.preventDefault();        
        const csrftoken = getCookie("csrftoken");
        let id_tipo_transaccion = $("#tipo_transaccion").val();
        let nombre_cliente=$("#nombre_cliente").val();
        let apellido_cliente=$("#apellido_cliente").val();
        let concepto=$("#concepto").val();
        if(id_tipo_transaccion.length>0 && nombre_cliente.length>0 && apellido_cliente.length>0 && concepto.length>0){
            let total_billete = $("#total_billete").val().replace("$", "");
            let total_moneda=$("#total_moneda").val().replace("$", "");
            let total_billete_moneda=$("#total_billete_moneda").val().replace("$","");
            let detalle_transaccion = obtener_datos_transaccion();
            let datos={
                csrfmiddlewaretoken:csrftoken,
                'id_tipo_transaccion':id_tipo_transaccion,
                'nombre_cliente':nombre_cliente,
                'apellido_cliente':apellido_cliente,
                'concepto':concepto,
                'total_billete':total_billete,
                'total_moneda':total_moneda,
                'total_billete_moneda':total_billete_moneda,
                'detalle_transaccion':JSON.stringify(detalle_transaccion)
            }
            let url_efectuar_trans_json=$("#url_efectuar_trans_json").val();
            $.ajax({
                url:url_efectuar_trans_json,
                type:"POST",
                data:datos,
                dataType:'json',
                success:function(data){
                    console.log(data.res)
                    let resultado=data.res;
                    if(resultado){
                        $("#btn_guardar_transaccion").prop('disabled', true);
                        setTimeout(function(){
                            window.location.href=$("#url_list_trans").val();
                        }, 1000)
                        toastr["error"]("La transaccion fue realizada correctamente");
                    }
                }
            });
        }else{
            toastr["error"]("Debe de ingresar el nombre, apellido del cliente el tipo de transaccion y el concepto");
        }
    });

    //primero se haran los totales de los billetes de la izquierda
    $(".cantidad1_b").keyup(function(){
        let cantida_denominacion=$(this).val();//primero obtenemos la cantidad
        //luego obtenemos el precio de la denominacion
        let precio_denominacion=$(this).closest('tr').find(".precio_deno1_b").val().replace("$","");
        
        //console.log(precio_denominacion)
        //luego hacemos el total de la cantidad por la denominacion y lo agregamos al campo
        //que esta despues del igual
        let valor_total=parseInt(cantida_denominacion)*parseFloat(precio_denominacion);
        if(isNaN(valor_total)){
            $(this).closest("tr").find(".total1_b").val("$0");
        }else{
            $(this).closest("tr").find(".total1_b").val("$"+valor_total);
        }
        calculo_total_billete()
        


    });
    //luego los totales de los billetes de la derecha
    $(".cantidad2_b").keyup(function(evt){
        let cantidad_denominacion=$(this).val();
        let precio_denominacion=$(this).closest('tr').find('.precio_deno2_b').val().replace("$", "");
        //console.log(precio_denominacion)

        let valor_total = parseInt(cantidad_denominacion)*parseFloat(precio_denominacion);
        if(isNaN(valor_total)){
            $(this).closest("tr").find(".total2_b").val("$0");
        }else{
            $(this).closest("tr").find(".total2_b").val("$"+valor_total);
        }
        calculo_total_billete();
        
    });

    $(".cantidad1_m").keyup(function(evt){
        let cantidad_denominacion=$(this).val();
        let precio_denominacion=$(this).closest("tr").find('.precio_deno1_m').val().replace("$", '');

        let valor_total=parseInt(cantidad_denominacion)*parseFloat(precio_denominacion);
        if(isNaN(valor_total)){
            $(this).closest("tr").find(".total1_m").val("$0");
        }else{
            $(this).closest("tr").find(".total1_m").val("$"+valor_total.toFixed(2));
        }
        calculo_total_moneda();
    });

    $(".cantidad2_m").keyup(function(evt){
        let cantida_denominacion=$(this).val();
        let precio_denominacion=$(this).closest("tr").find('.precio_deno2_m').val().replace("$", "");

        let valor_total=parseInt(cantida_denominacion)*parseFloat(precio_denominacion);
        if(isNaN(valor_total)){
            $(this).closest("tr").find(".total2_m").val("$0");
        }else{
            $(this).closest("tr").find(".total2_m").val("$"+valor_total.toFixed(2));
        }
        calculo_total_moneda();
    });

    function calculo_total_billete(){
        let total_billete=0;
        $("#table-denominacion-billete tr").each(function(index){
            let total_deno_b1=$(this).find(".total1_b").val();
            let total_deno_b2=$(this).find(".total2_b").val();
                if(total_deno_b1!=''){
                    total_billete+=parseFloat(total_deno_b1.replace("$", ""));
                }
                
                if(total_deno_b2){
                    total_billete+=parseFloat(total_deno_b2.replace("$", ""));
                }
                


            $("#total_billete").val("$"+total_billete.toFixed(2));
            console.log(total_billete)

        });
        calcular_total_billete_moneda();
    }

    function calculo_total_moneda(){
        let total_moneda=0;
        $("#table-denominacion-moneda tr").each(function(index){
            let total_deno_m1=$(this).find(".total1_m").val();
            let total_deno_m2=$(this).find(".total2_m").val();
            if(total_deno_m1!=''){
                total_moneda+=parseFloat(total_deno_m1.replace("$", ""));
            }

            if(total_deno_m2!=""){
                total_moneda+=parseFloat(total_deno_m2.replace("$", ""));
            }

            $("#total_moneda").val("$"+total_moneda.toFixed(2))
        })
        calcular_total_billete_moneda();
    }

    function calcular_total_billete_moneda(){
        let total_billete=$("#total_billete").val();
        let total_moneda=$("#total_moneda").val();
        let total=0;
        if(total_billete!='' && total_moneda!=''){
            total = parseFloat(total_billete.replace("$", ""))+parseFloat(total_moneda.replace("$", ""));
        }else if (total_billete!="" &&  total_moneda==''){
            total = parseFloat(total_billete.replace("$", ""));
        }else if(total_billete=="" && total_moneda!=""){
            total=parseFloat(total_moneda.replace("$", ""))
        }
        console.log("billete: "+total_billete+" "+" Moneda: "+total_moneda)
        $("#total_billete_moneda").val("$"+total.toFixed(2));
        $("#id_total_en_grande").val("$"+total.toFixed(2))
    }

    function obtener_datos_transaccion(){
        let datos = [];
        //recorriendo los datos del billete
        $("#table-denominacion-billete tr").each(function(index){
            //id_deno1_b seria la primera columna de billetes
            let id_deno1_b=$(this).find(".id_deno1_b").val();
            //cantidad1_b seria la primera cantidad de billete segun denominacion
            let cantidad1_b=$(this).find(".cantidad1_b").val();
            //totales de la primera columna
            let total1_b=$(this).find(".total1_b").val().replace("$", "");

            console.log("id_deno1_b:"+id_deno1_b+" cantidad1_b:"+cantidad1_b+" total2b: "+total1_b);
            let dinero = {"id_denominacion":id_deno1_b, "cantidad":cantidad1_b, "total":total1_b};
            datos.push(dinero);
            
        });

        $("#table-denominacion-billete tr").each(function(index){
            if(index!=3){//aqui validamos que index sea difente de 3 porque cuando llega a 3 tira un valor undefine, ya que la columna que esta a la par tiene 4 filas y en la segunda columna la busca pero tira valor undefined
                //id_deno2_b seria la segunda columna de billetes
                let id_deno2_b=$(this).find(".id_deno2_b").val();
                //cantidad2_b seria la segunda columna de cantidad de billetes
                let cantidad2_b=$(this).find(".cantidad2_b").val();
                //totales de la segunda columna
                let total2_b=$(this).find(".total2_b").val().replace("$", "");
                console.log(index);
                console.log("id_deno2_b:"+id_deno2_b+" cantidad2_b:"+cantidad2_b+" total2_b:"+total2_b);
                console.log(index);

                    let dinero = {"id_denominacion":id_deno2_b, "cantidad":cantidad2_b, "total":total2_b};
                    datos.push(dinero);
                }
        });
        //ahora vamos con la moneda

        $("#table-denominacion-moneda tr").each(function(index){
            //obteniendo los id de la primera columna de la tabla de moneda
            let id_deno1_m = $(this).find(".id_deno1_m").val();
            //obteniendo las cantidades de las primera columna
            let cantidad1_m=$(this).find(".cantidad1_m").val();
            //oteniendo los totales de la primera columna
            let total1_m=$(this).find(".total1_m").val().replace("$","");
            let dinero={'id_denominacion':id_deno1_m, 'cantidad':cantidad1_m, 'total':total1_m};
            datos.push(dinero);
        });

        $("#table-denominacion-moneda tr").each(function(index){
            //obteniendo los id de la segunda columna de moneda
            let id_deno2_m=$(this).find(".id_deno2_m").val();
            //obteniendo las cantidades de la segunda columna en moneda
            let cantidad2_m=$(this).find(".cantidad2_m").val();
            //obteniendo los totales de la segunda columna en moneda
            let total2_m=$(this).find(".total2_m").val().replace("$","");
            let dinero={'id_denominacion':id_deno2_m, 'cantidad':cantidad2_m, 'total':total2_m};
            datos.push(dinero);
        });

        console.log(datos);
        return datos
    }

});