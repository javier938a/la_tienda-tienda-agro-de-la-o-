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
    $("#reimprimir").click(function(evt){
        const csrftoken=getCookie("csrftoken");
        //para imprimir la factura nuevamente es necesario primero traer los datos de la factura desde el servidor
        //porque donde se va imprimir no va ser necesariamente directamente desde el servidor si no de un cliente
        //por ahorita asumimos que se va imprimir desde el servidor
        let id_venta=$("#id_venta").val();//se obtiene el id almacenado
        let url_get_ticket=$("#url_get_ticket").val();//la url para obtener los dats de la factura
        datos={
            csrfmiddlewaretoken:csrftoken,
            'id_venta':id_venta,
        };
        $.ajax({//se hace la peticion
            url:url_get_ticket,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let resultado=data.res;
                if(resultado){                            
                    datos_ticket= JSON.stringify(data.datos_ticket);//se obtienen los datos luego hay que hacer otra peticion a donde se va imprimir el ticket
                    //console.log(datos_fact);
                    let url_print_ticket=$("#url_print_ticket").val();
                    const csrftoken=getCookie('csrftoken');
                    datos={
                        csrfmiddlewaretoken:csrftoken,
                        'ticket':datos_ticket
                    };
                    $.ajax({
                        url:url_print_ticket,
                        type:'POST',
                        data:datos,
                        dataType:'json',
                        success:function(data){
                            console.log(data);
                        }
                    })

                    ///aqui el codigo que imprimira el ticket e redireccionara al listado de ventas
                }else{
                    toastr['error']("La Venta no pudo ser registrada exitosamente");
                }
            }
       });
    });
})