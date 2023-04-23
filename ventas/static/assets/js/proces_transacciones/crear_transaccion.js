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

});