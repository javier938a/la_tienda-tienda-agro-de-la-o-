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
    $(".select").select2();

    url_clave=$("#url_auto_prod").val();
    csrftoken=getCookie('csrftoken');
    clave=$("#producto").val();
    data={
        csrfmiddlewaretoken:csrftoken,
        'clave':clave
    }

    //validando el campo de costo a solo numeros
    $(document).on('input',".cant", function(){
        this.value = this.value.replace(/[^0-9]/g,'');
    });

    //validando a decimales
    $(document).on('input', ".cost",function () {
        this.value = this.value.replace(/[^0-9,.]/g, '').replace(/,/g, '.');
    });

    $(document).on('input', ".pre",function () {
        this.value = this.value.replace(/[^0-9,.]/g, '').replace(/,/g, '.');
    });

      

    //lista los productos en un autocomplete
    $("#producto").autocomplete({
        source:function(request, response){
            $.ajax({
                url:url_clave,
                type:"GET",
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
           let producto = ui.item.value;
           let prod_array=producto.split('|');
           id_producto=prod_array[0];
            agregar_producto_a_tabla(id_producto);
        }
    });

    //funcion que sirve para agregar una fila a la tabla
    function agregar_producto_a_tabla(id_producto){
        let url=$("#url_update_datos_inventario").val();
        let csrftoken=getCookie('csrftoken');
        let datos={
            csrfmiddlewaretoken:csrftoken,
            'id_producto':id_producto,
        };
        $.ajax({
            url:url,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let fila_producto=data.fila_producto;
                $("#table-productos").prepend(fila_producto);
                $("#producto").val("");
            }            
        });
    }
    //ELIMINANDO FILA de un producto
    $(document).on('click', '.delfila', function(evt){
       let fila = $(this).parents('tr');
       fila.remove();
        //redecalculando los totales cada vez que se elimina una fila
        calcular_totales();
    });
    //calculando los totales de todos los productos ingresados

    $(document).on('keyup', '.cant', function(){//obteniendo el evento de cada una de las celdas en donde se ingresa la cantidad
        let cantidad= parseInt($(this).val());//obteniendo el total que se esta ingresando
        let costo=$(this).closest('tr').find('.cost').val();//obtenendo el costo que esta en el canpo costo no se convierte porque pueda quee este vacio
        console.log(costo);                                 //closest devuelve el primer antecesor del elemento
        if(costo!=''){//si el el campo costo no esta vacio multiplica el costo por el total
            let total=cantidad*parseFloat(costo);
            $(this).closest('tr').find('.tot').val('$'+redondear(total));//se asigna el total campo del total
        }else{
            $(this).closest('tr').find('.tot').val("$0.0");//de lo contrario el input del total sera vacio
        }
        calcular_totales();
    });

    $(document).on('keyup', '.cost', function(){
        let costo=parseFloat($(this).val().replace('$',''));//obteniendo el costo ingresado actualmente
        let cantidad=$(this).closest('tr').find('.cant').val();
        console.log(cantidad.length);
        
        if(cantidad!=''){//si cantidad es diferente de vacio es porque hay algun costo del producto ingresado
            console.log("Simpre ")
            console.log(cantidad);
            //y efectuamos la operacion
            let total=costo*parseFloat(cantidad);

            console.log(total)
            if(isNaN(total)){//verifica que el numero sea NaN si es NaN entonces el total vale cero
                $(this).closest('tr').find('.tot').val('$0.0');
            }else{
                $(this).closest('tr').find('.tot').val('$'+ redondear(total));
            }
            
        }else{
            $(this).closest('tr').find('.tot').val("$0.0");
        }
        calcular_totales();
    })
    //calcula la suma de los totales de los productos
    function calcular_totales(){
        let total=0.0;//creando una varible contadora que contara todos los costos
        $("#table-productos tr").each(function(){
            let cantidad_str=$(this).find('.cant').val();
            let costo_str=$(this).find('.cost').val().replace('$','');
            let cantidad=0;
            let costo=0;
            if(cantidad_str!=''){
                cantidad=parseInt(cantidad_str);            
            }
            if(costo_str!=''){
                costo=parseFloat(costo_str);
            }
            total+=cantidad*costo;

            
        });
        console.log(total);
        $("#total").text('$'+redondear(total));//mostrando el total
    }

    //funcion para redondear cantidades a dos digitos
    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }

    //guardar el inventario
    $("#actualizar").click(function(evt){
        let tabla_prod=$("#table-productos tr");
        let resultado=validar_lista_productos(tabla_prod);
        if(resultado){//si resultado es true hay que guardar todos los productos 
            detalles_productos=obtener_productos(tabla_prod);//obteniendo los detalles de productos
            productos_json=JSON.stringify(detalles_productos);//convirtiendo los productos a json
            console.log(detalles_productos);
            descripcion=$("#descripcion").val();//obteniendo la descripcion
            id_sucursal=$("#sucursal").val();//obteniendo la sucursal
            id_inventario=$("#id_inventario").val();

            total=$("#total").text().replace('$','');
            const csrftoken=getCookie('csrftoken');
            if(descripcion.length>0 && id_sucursal.length>0){//si hay una descipcion ingresado y un id_sucursal seleccionado se procede a enviar
                datos_inventario={
                    csrfmiddlewaretoken:csrftoken,
                    'id_inventario':id_inventario,
                    'descripcion':descripcion,
                    'id_sucursal':id_sucursal,
                    'total':total,
                    'productos_json':productos_json
                }
                url=$("#url_update_detalle_inv").val();
                $.ajax({
                    url:url,
                    type:'POST',
                    data:datos_inventario,
                    dataType:'json',
                    success:function(data){
                        resultado=data.res;
                        if(resultado==true){
                            toastr['success']("Inventario cargado exitosamente");
                            setTimeout(function(){
                                url_listar_inv=$("#url_list_inv").val();
                                window.location.href=url_listar_inv;
                            }, 1500)
                        }
                    }            
                });

            }else{
                toastr['error']("Dede de ingresar una descripcion y seleccionar un sucursal")
            }
            
        }else{
            toastr['warning']("Debe de llenar todos los campos de los productos ingresados");
        }
    });
    
    function validar_lista_productos(tabla){//cuenta si todo los campos estan vacios si encuentra 1 suma cero y no deja registrar
        cuenta_vacios=0;
        resultado=false;
        tabla.each(function(){
            let sel=$(this).find('.select').val();
            let cant=$(this).find('.cant').val();
            let cost= $(this).find('.cost').val();
            let pre= $(this).find('.pre').val();
            let tot=$(this).find('.tot').val();
            if(sel.length===0){
                cuenta_vacios++;
            }
            if(cant.length===0){
                cuenta_vacios++;
            }
            if(cost.length===0){
                cuenta_vacios++;
            }
            if(pre.length===0){
                cuenta_vacios++;
            }
        });
        
        if(cuenta_vacios===0){
            
            resultado=true;
        }

        return resultado;
    }


    function obtener_productos(tabla){//FUNCION QUE RECORRE TODA LA TABL Y RETORNA TODOS LOS PRODUCTOS A GUARDAR
       let datos=[];
       tabla.each(function(){
            let idproducto=$(this).find('.idprod').val();
            let id_prod_inv=$(this).find(".id_prod_inv").val();
            let id_presentacion=$(this).find('.select').val();
            let cantidad=$(this).find('.cant').val();
            let costo=$(this).find('.cost').val().replace("$","");
            let precio=$(this).find('.pre').val().replace("$", "");
            let total=$(this).find('.tot').val().replace("$",'');
            fila={'id_prod_inv':id_prod_inv,'id_producto':idproducto, 'id_presentacion':id_presentacion, 'cantidad':cantidad, 'costo':costo, 'precio':precio, 'total':total};
            datos.push(fila);       
        });
       return datos;
    }

});