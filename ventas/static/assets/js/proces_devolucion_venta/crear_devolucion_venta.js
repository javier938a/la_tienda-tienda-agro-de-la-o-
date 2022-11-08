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
                console.log(filas_ventas);
                //agregando el id de la venta en un campo oculto 
                $("#id_venta").val(id_venta);
                $("#table-devolucion-productos").empty();
                $("#table-devolucion-productos").prepend(filas_ventas);
            
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
        //Validando que la cantidad a devolver no sea mayor a la cantidad que se haya vendido
        if($(this).val().length>0){
            if( parseFloat(cantidad_devolver)>=0.0 && parseFloat(cantidad_devolver)<=parseFloat(cantidad_vendida)){
                //mostrandolo la nueva cantidad en tiempo real
                $(this).closest('tr').find('.nueva_cant').text(redondear(nueva_cantidad))
                //obteniendo el precio del producto a devolver
                let precio_prod=parseFloat($(this).closest('tr').find('.precio_prod').val().replace('$',''));
                console.log($(this).closest('tr').find('.precio_prod'));
                //multiplicando el precio del producto por la cantidad de dinero a devolver
                //esto daria el total de dinero a devolver
                let dinero_devol=cantidad_devolver*precio_prod
                //mostrando el total de dinero a devolver
                $(this).closest('tr').find('.dinero_devol').text("$"+redondear(dinero_devol));
                //luego calculariamos el nuevo total que quedaria en la venta
                let nuevo_total_de_venta=nueva_cantidad*precio_prod;
                //mostrando la nueva cantidad que quedaria en la venta
                $(this).closest('tr').find('.nuevo_total_venta').text("$"+redondear(nuevo_total_de_venta));
                
            }else{
                $(this).val('');
                $(this).closest('tr').find('.nueva_cant').text("");
                $(this).closest('tr').find('.dinero_devol').text("");
                $(this).closest('tr').find('.nuevo_total_venta').text("");                
                toastr['info']('la cantidad a devolver tiene que ser mayor o igual a la cantidad que se ventido en esta venta');
            }
        }else{
            $(this).closest('tr').find('.nueva_cant').text("");
            $(this).closest('tr').find('.dinero_devol').text("");
            $(this).closest('tr').find('.nuevo_total_venta').text("");
        }
        calculo_totales();

    });

    function calculo_totales(){
        let total_dinero_devoler=0.0;
        $("#table-devolucion-productos tr").each(function(){
            let cantidad_devolver_str=$(this).find('.cant_devo').val();
            let precio_producto_str=$(this).find('.precio_prod').val();
            let cantidad=0;
            let precio=0.0;
            if(cantidad_devolver_str!=''){
                cantidad=parseInt(cantidad_devolver_str);
            }
            if(precio_producto_str!=''){
                precio=parseFloat(precio_producto_str.replace('$',''));
            }
            
            total_dinero_devoler+=(cantidad*precio);
            console.log(precio_producto_str.replace("$",''));
        });
        $("#total").text("$"+redondear(total_dinero_devoler));  

    }
    //funcion para redondear cantidades a dos digitos
    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }
    //efectuando la devolucion sobre venta
    $("#efectuar_devolucion").click(function(evt){
        let total=$("#total").text().replace('$', '');
        console.log('hola: '+total)
        if(total!=''){
            if(parseFloat(total)>0){
                let descripcion_devo=$("#descripcion_devo").val();
                let id_sucursal=$("#sucursal").val();
                if(descripcion_devo.length>0 && id_sucursal.length>0){//validando que haya una descripcion de la devolucion
                    let id_venta=$("#id_venta").val();
                    let tabla_datos=$("#table-devolucion-productos tr");
                    let datos_devoluciones=obtener_producto_devolver(tabla_datos);
                    console.log(datos_devoluciones);
                    let detalles_devoluciones_json=JSON.stringify(datos_devoluciones);
                    console.log(detalles_devoluciones_json);
                    const csrftoken=getCookie('csrftoken');
                    let datos={
                        csrfmiddlewaretoken:csrftoken,
                        'id_venta':id_venta,
                        'descripcion_devo':descripcion_devo,
                        'id_sucursal':id_sucursal,
                        'detalles_devo':detalles_devoluciones_json,
                        'total':total
                    };
                    let url_efectuar_devolucion=$("#url_efectuar_devolucion").val();
                    $.ajax({
                        url:url_efectuar_devolucion, 
                        type:'POST',
                        data:datos,
                        dataType:'json',
                        success:function(data){
                            let res=data.res;
                            if(res==true){
                                toastr['success']("Devolucion efectuada exitosamente");
                                setTimeout(function(){
                                    let url_listar_devoluciones=$("#url_listar_devoluciones").val();
                                    window.location.href=url_listar_devoluciones;
                                }, 1500);
                            }else{
                                toastr['warning']("Hubo un error de sistema favor llamar a soporte tecnico");
                            }
                            console.log(data);
                        }
                    });
                    

                }else{
                    toastr['warning']("Debe agregar una breve descripcion del porque se hizo esta devolucion");
                }       
            }else{
                toastr['warning']('Para efectuar devolucion debe de devolver al menos un producto, no puede dejar los campos a cero');
            }       
        }
    });

    function obtener_producto_devolver(tabla_datos){
        let datos=[];
        tabla_datos.each(function(index){
            let id_detalle_venta=$(this).find('.id_detalle_venta').text();
            let cantidad_devolver=$(this).find('.cant_devo').val();
            let nueva_cantidad=$(this).find('.nueva_cant').text();
            let dinero_devolver=$(this).find('.dinero_devol').text().replace('$', '');
            let nuevo_total_venta=$(this).find('.nuevo_total_venta').text().replace('$', '');
            if(cantidad_devolver!=''){
                let fila={'id_detalle_venta':id_detalle_venta, 'cantidad_devolver':cantidad_devolver, 'nueva_cantidad':nueva_cantidad, 'dinero_devolver':dinero_devolver, 'nuevo_total_venta':nuevo_total_venta};
                datos.push(fila);
            }
        });
        return datos;
    }

});