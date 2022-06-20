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
    let url_auto_list_ventas=$("#url_autocomplete_venta").val();//obteniendo la url donde se listan las ventas
    let clave_codigo=$("#codigo_venta").val();//este campo servira para buscar la venta
    const csrftoken = getCookie('csrftoken');
    
    $("#codigo_venta").autocomplete({//este campo servira para buscar la venta por codigo de venta
        source:function(request, response){
            $.ajax({
                url:url_auto_list_ventas, 
                type:'POST',
                data:{
                    csrfmiddlewaretoken:csrftoken,
                    term:request.term
                },
                dataType:'json',
                success:function(data){
                    response(data);
                }
            })
        },
        minLength:2,
        select:function(event, ui){
            let item_venta=ui.item.value;
            let item_venta_array=item_venta.split('|');
            let id_venta=item_venta_array[0];
            console.log(id_venta)
            agregar_productos_de_venta_seleccionada(id_venta)//una vez obteniendo la venta obtenemos el id este metodo servira para listar todos los productos de dicha venta
        }
    });

    function agregar_productos_de_venta_seleccionada(id_venta){
        const csrftoken=getCookie('csrftoken');
        let url_listar_datos_venta=$("#url_listar_productos_de_venta").val();
        //alert(url_listar_datos_venta);
        let datos={
            csrfmiddlewaretoken:csrftoken,
            'id_venta':id_venta
        };
        $.ajax({
            url:url_listar_datos_venta,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let filas_ventas=data.filas_ventas;
                $("#table-productos").empty();
                $("#table-productos").prepend(filas_ventas);
            
            }
        })

    }

    $(document).on('keyup', '.cant_devo', function(){
        //obteniendo la cantidad del producto vendido se convierte a entero
        let cantidad_vendida= parseInt($(this).closest('tr').find('.cant_vendida').text());
        console.log(cantidad_vendida)
        //obteniendo la cantidad a devolver que es la cantidad escrita y se pasa a entero
        let cantidad_devolver= parseInt($(this).val());
        //obteniendo la nueva cantidad que queda en la venta que es la diferencia ente la cantidad vendida menos la cantidad a devolver
        let nueva_cantidad=cantidad_vendida-cantidad_devolver;
        //mostrandolo la nueva cantidad en tiempo real
        $(this).closest('tr').find('.nueva_cant').text(nueva_cantidad)
        //obteniendo el precio del producto a devolver
        let precio_prod=parseFloat($(this).closest('tr').find('.precio_prod').text());
        //multiplicando el precio del producto por la cantidad de dinero a devolver
        //esto daria el total de dinero a devolver
        let dinero_devol=cantidad_devolver*precio_prod
        //mostrando el total de dinero a devolver
        $(this).closest('tr').find('.dinero_devol').text(dinero_devol);
        //luego calculariamos el nuevo total que quedaria en la venta
        let nuevo_total_de_venta=nueva_cantidad*precio_prod;
        //mostrando la nueva cantidad que quedaria en la venta
        $(this).closest('tr').find('.nuevo_total_venta').text(nuevo_total_de_venta);
        
    });

});