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
    
    let url_list_descarga_prod = $("#url_list_prod_a_descargar").val();//url de la lista de productos a descargar
    let csrftoken = getCookie('csrftoken');
    $("#producto").autocomplete({
        source:function(request, response){
            $.ajax({
                url:url_list_descarga_prod,
                type:"POST",
                data:{
                    csrfmiddlewaretoken:csrftoken,
                    term:request.term
                },
                dataType:'json',
                success:function(data){
                    response(data)
                }
            })
        },
        minLength:2,
        select:function(event, ui){
            let producto=ui.item.value;
            let array_producto=producto.split('|');
            let detalle_productos=$("#table-productos-descarga tr");
            let id_prod_stock=array_producto[0];
            let esta_agregado=validar_producto_unico(detalle_productos, id_prod_stock);
            if(esta_agregado){
                agregar_producto_a_descargar_detalle(id_prod_stock);
            }else{
                toastr['error']("Este producto ya esta agregado en el detalle de productos, ingrese otro distinto");
                $("#producto").val("");
            }
            

        }
    });  
    
    function agregar_producto_a_descargar_detalle(id_producto){
        const csrftoken=getCookie('csrftoken');
        let url_add_prod_a_descarga=$("#url_add_prod_a_descarga").val();
        let datos={
            csrfmiddlewaretoken:csrftoken,
            'id_prod_stock':id_producto,
        };
        $.ajax({
            url:url_add_prod_a_descarga,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let fila_producto=data.fila_producto                
                $("#table-productos-descarga").prepend(fila_producto)
                $("#producto").val("");
            }
        });
    }

    $(document).on('keyup', '.cant', function(evt){
        let cantidad=parseInt($(this).val());//obteniendo la cantidad ingresada
        let costo=$(this).closest('tr').find('.cost').val().replace('$', '');
        console.log(costo);
        if(!isNaN(cantidad)){
            let total = cantidad*parseFloat(costo)
            if(!isNaN(total)){
                $(this).closest('tr').find('.tot').val("$"+redondear(total));
            }            
        }else{
            $(this).val("0");
            $(this).closest('tr').find('.tot').val("$0.0");
        }
        calcular_totales();
    });

    $("#efectuar_descarga").click(function(evt){
        let descripcion=$("#descripcion").val();
        if(descripcion.length>0){
            let tabla_detalle_de_descarga_productos=$("#table-productos-descarga tr");
            let res_tabla_descarga_prod=validar_detalle_de_descarga_productos(tabla_detalle_de_descarga_productos);
            if(res_tabla_descarga_prod===false){
                const csrftoken=getCookie('csrftoken');
                let detalles_descarga_producto=obtener_detalle_productos_a_descargar(tabla_detalle_de_descarga_productos);
                let total=$("#total").text().replace('$', '');
                console.log(detalles_descarga_producto)
                let url_efectuar_descarga_prod=$("#url_efectuar_descarga_prod").val();
                let datos={
                    csrfmiddlewaretoken:csrftoken,
                    'descripcion':descripcion,
                    'total':total,
                    'detalles_descarga_producto':JSON.stringify(detalles_descarga_producto)
                }
                console.log(datos);
                $.ajax({
                    url:url_efectuar_descarga_prod,
                    type:'POST',
                    data:datos,
                    dataType:'json',
                    success:function(data){
                        let res=data.res;
                        if(res===true){
                            toastr['success']("Descarga efectuada exitosamente")
                            setTimeout(function(){
                                window.location.href=$("#url_listar_descarga_prod").val();
                            }, 1000);
                        }else{
                            toastr['error']("Hubo un error al registrar los datos comuniquese con el administrador del sistema..");
                        }
                    }
                });
            }else{
                toastr['error']("Debe de llenar todos los campos de cantidad de todos los productos en la descarga a efectuar..");
            }
        }else{
            toastr['error']("Debe de agregar una descripcion como justificacion de la descarga de los productos");
        }
    })

    //validar que no se agregue dos veces el mismo producto
    function validar_producto_unico(tabla, id){
        res=true;
        tabla.each(function(index){
            id_prod_stock=$(this).find('.idprod').val();
            
            console.log("este es el id: "+id_prod_stock)
            if(id_prod_stock===id){
               res=false 
            }
        });
        console.log("Resultado siempre da "+res)
        return res;
    }

    $(document).on('click', '.delfila', function(){
        let fila = $(this).parents('tr');
        fila.remove();
        calcular_totales();
    });
    //funcion para redondear cantidades a dos digitos
    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }

    function validar_detalle_de_descarga_productos(tabla_detalle){
        let cuenta_cantidad=0;
        let res=false;

        tabla_detalle.each(function(index){
            let cantidad=$(this).find('.cant').val();
            if(cantidad.length===0){
                cuenta_cantidad++;
            }
        });
        let num_filas=tabla_detalle.length;
        if(cuenta_cantidad>0 || num_filas===0){
            res=true
        }
        return res;
    }

    function obtener_detalle_productos_a_descargar(tabla){
        let datos=[];
        tabla.each(function(index){
            let id_prod_stock=$(this).find('.idprod').val();
            let cantidad=$(this).find('.cant').val();
            let costo=$(this).find('.cost').val();
            let total=$(this).find('.tot').val().replace('$','');
            let fila={'id_prod_stock':id_prod_stock, 'cantidad':cantidad, 'costo':costo, 'total':total};
            datos.push(fila);
        });
        
        return datos;
    }

    function calcular_totales(){
        let total=0;
        $("#table-productos-descarga tr").each(function(index){
            let cantidad_str=$(this).find(".cant").val();
            let costo_str=$(this).find('.cost').val();
            let cantidad=0;
            let costo=0;
            if(cantidad_str!=''){
                cantidad=parseInt(cantidad_str);
            }
            if(costo_str!=''){
                costo=parseFloat(costo_str.replace('$', ''));
            }
            total+=(cantidad*costo);
        });
        $("#total").text("$"+redondear(total))
    }

});