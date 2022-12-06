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

    $(document).on('input', '.cant', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });

    $(document).on('input', '.cost', function(){
        this.value = this.value.replace(/[^0-9,.]/g, '').replace(/,/g, '.');
    });
    $(document).on('input', '.pre', function(){
        this.value = this.value.replace(/[^0-9,.]/g, '').replace(/,/g, '.');
    });


    //listar los productos a cargar pueden ser nuevos o productos 
    let url_listar_productos_cargados_y_sin_cargar=$("#url_listar_productos_cargados_y_sin_cargar").val();
    const csrftoken=getCookie('csrftoken')
    let id_sucursal=$("#sucursal").val();  
    //lo que se esta haciendo aqui almacenando en un hidden el valor del id sucursal
    //por medio del evento change ya que da una falla al agarrarlo directamebte del select 
    $("#sucursal").change(function(){
        //debido a que cuando seleccionamos una sucursal el sistema nos busca todos los productos cargados en esa sucursal
        //no podemos cambiar de sucursal cuando ya hemos ingresado los productos que pertenecen a esa sucursal
        //si cambiamos tenemos que borrar todo lo ingresado, y agregar solo productos que esten cargados en esa sucursal
        //y los productos que aun no han sido cargados del catalogo
        //primero obtenemos el numero de filas que hay en la tabla de esta manera nos aseguramos que no se haya ingresado aun productos
        //y poder cambiar de sucursal libremente
        let numero_filas_en_tabla=$("#table-productos-carga tr").length;
        if(numero_filas_en_tabla>0){//si ya hay produtos agregados al detalle le preguntamos si desea cambiar de sucursal y alertamos al usuario que si lo cambia se borraran todo lo que haya ingresado hasta ese momento
            let cambiar_sucursal=window.confirm("¿Esta seguro que desea cambiar de sucursal? se borrara lo que se ha agregado hasta ahorita.")
            if(cambiar_sucursal==true){//si el usuario dice que si entonces procedemos a borrar todo el contenido de la tabla
                $("#table-productos-carga tr").remove();//y agregamos al hidden input el nuevo id de sucursal
                $("#id_sucursal_hidden").val($(this).val())
            }else{//de lo contrario establecemos el en el select la ultima sucursal seleccionada que se encuentra en el hidden input
                let id_sucursal_hidden = $("#id_sucursal_hidden").val();
                $(this).val(id_sucursal_hidden).trigger('change.select2');
            }
            
        }else{//si el numero de filas de la tabla es cero podremos cambiar de sucursal libremente
            $("#id_sucursal_hidden").val($(this).val());
        }

    });  
    $("#producto").autocomplete({
        source:function(request, response){
            //console.log("Hola esto es el autocomplete")
            let id_sucursal_hidden=$("#id_sucursal_hidden").val();

            console.log("id_sucursal="+id_sucursal)
            if(id_sucursal_hidden!="0"){
                $.ajax({
                    url:url_listar_productos_cargados_y_sin_cargar,
                    type:"POST",
                    data:{
                        csrfmiddlewaretoken:csrftoken,
                        'id_sucursal':id_sucursal_hidden,
                        term:request.term
                    },
                    dataType:'json',
                    success:function(data){
                        response(data)
                    }
                })
            }else{
                toastr["warning"]("Debe de seleccionar la sucursal en donde cargara los productos");
            }
        },
        minLength:2,
        select:function(event, ui){
            let producto=ui.item.value;
            let prod_array=producto.split('|');
            let id_prod_cualquiera=prod_array[0];
            let detalle_productos=$("#table-productos-carga tr");
            esta_agregado=validar_producto_nuevo_unico(detalle_productos, id_prod_cualquiera);
            console.log("Hola que tal "+esta_agregado)
            if(esta_agregado){
                presentacion=prod_array[2];
                stock=prod_array[3];
                console.log(producto)
                agregar_producto_detalle_carga(id_prod_cualquiera, presentacion, stock);   
            }else{
                $("#producto").val("");//limpiando el campo de producto
                toastr['error']("Este producto ya esta agregado en el detalle de carga, porfavor ingrese otro producto");
                     
            } 
        }
    });


    function agregar_producto_detalle_carga(id_prod_cualquiera, presentacion, stock){
        const csrftoken=getCookie('csrftoken');
        let url_add_prod_detalle_carga=$("#url_add_prod_detalle_carga").val();
        let datos={
            csrfmiddlewaretoken:csrftoken,            
            'presentacion':presentacion,
            'stock_actual':stock,
            'id_producto':id_prod_cualquiera
        };
        $.ajax({
            url:url_add_prod_detalle_carga,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let res = data.res
                let fila_producto=data.fila_producto;
                if(res===true){//si res retorna true es porque de este producto aun hay en existencia
                    console.log(fila_producto);
                    $("#table-productos-carga").prepend(fila_producto);//y se agrega la fila a la tabla
                    calcular_totales();//calculando los totales
                    $("#producto").val("");
                }else{
                    toastr['warning']("De este producto que intenta agregar ya no hay en existencia");
                }
            }
        })
    }

    $("#efectuar_carga").click(function(){
        let descripcion_carga=$("#descripcion").val();
        if(descripcion_carga.length>0){
           let id_sucursal = $("#id_sucursal_hidden").val();
           if(id_sucursal.length>0){
            let tabla_producto_detalle=$("#table-productos-carga tr");
            let res_tabla_detalle=validar_detalles_carga(tabla_producto_detalle);
            if(res_tabla_detalle===false){
                if(parseInt(id_sucursal)>0){
                    let detalles_productos= obtener_detalles_productos(tabla_producto_detalle);
                    console.log("Detalle..")
                    console.log(detalles_productos);
                    let total=$("#total").text().replace("$", "");
                    const csrftoken=getCookie("csrftoken");
                    let datos={
                        csrfmiddlewaretoken:csrftoken,
                        'descripcion':descripcion_carga,
                        'id_sucursal':id_sucursal,
                        'detalles_productos':JSON.stringify(detalles_productos),
                        'total':total,
                    };
                    console.log(datos);
                    let url_cargar_prod_inv=$("#url_cargar_prod_inv").val();
                    console.log(url_cargar_prod_inv)
                    $.ajax({
                        url:url_cargar_prod_inv,
                        type:'POST',
                        data:datos,
                        dataType:'json',
                        success:function(data){
                            let res = data.res;
                            if(res===true){
                                toastr['success']("Inventario cargado exitosamente");
                                setTimeout(function(){
                                    window.location.href=$("#url_listar_cargas_inventario").val();
                                }, 1000)
                            }else{
                                toastr['sucess']("Error al cargar inventario favor comuniquese con soporte tecnico")
                            }
                        }
                    });
                }else{
                    toastr['warning']("Debe de seleccionar una sucursal antes de poder realizar una carga de productos al inventario");
                }
            }else{
                toastr['error']("Debe de ingresar mas de un producto y llenar todos los campos");
            }
           }else{
               toastr['error']("Debe de seleccionar una sucursal antes de efectuar una carga");
           }

        }else{
            toastr['error']("Debe de llenar una descripcion de carga")
        }
    });


    function validar_detalles_carga(tabla_detalle){
        //cuenta que no haya ningun campo de cantidad vacio
        let cuenta_cantidad=0;
        let cuenta_precio=0;
        let cuenta_costo=0;
        let cuenta_presentacion=0;
        let res_cant=false;//si res cambia a true es porque hay campos de cantidades vacios
        let res_pres=false
        let res_presentacion=false;
        let res_cost=false
        let res=false
        tabla_detalle.each(function(index){
            let cantidad=$(this).find('.cant').val();
            let precio=$(this).find('.pre').val();
            let costo=$(this).find('.cost').val()
            let presentacion=$(this).find(".presentacion").val();

            if(cantidad.length===0){
                cuenta_cantidad++;
                console.log("Entro aqui...")
                console.log(cantidad);

            }
            if(precio.length===0){
                cuenta_precio++;
                console.log("Precio aqui")
            }
            if(costo.length===0){
                cuenta_costo++;
                console.log("costo aqui")
            }
            if(presentacion.length===0){
                cuenta_presentacion++;
                console.log("Precentacion  aqui")
            }
        })
        let num_filas=tabla_detalle.length;
        if(cuenta_cantidad>0 || num_filas===0){
            res_cant=true
        }
        if(cuenta_precio>0 || num_filas===0){
            res_pres=true
        }
        if(cuenta_costo>0 || num_filas===0){
            res_cost=true
        }
        if(cuenta_presentacion>0 || num_filas===0){
            res_presentacion=true
        }

        console.log(res_cant+' '+res_pres+' '+res_cost+' '+res_presentacion)
        console.log(cuenta_cantidad+' '+cuenta_precio+' '+cuenta_costo+' '+cuenta_presentacion);
        //con solo uno que sea true res pasara a true 
        if(res_cant===true || res_pres===true || res_cost===true || res_presentacion===true){
            res=true
        }

        
        return res;
    }

    function obtener_detalles_productos(tabla_detalle){
        let datos=[];
        tabla_detalle.each(function(){
            let tipo_prod=$(this).find('.tipo_prod').val();
            let id_producto_stock=$(this).find('.idprod').val();
            let presentacion=$(this).find('.presentacion').val();
            let cantidad=$(this).find('.cant').val();
            let costo=$(this).find('.cost').val();
            let precio=$(this).find('.pre').val();
            let total=$(this).find('.tot').val().replace('$', '');
            fila_prod={
                'tipo_prod':tipo_prod,
                'id_prod_o_stockubi':id_producto_stock,//porque el id puede de la tabla producto o tabla ProductoStockUbicacion
                'id_presentacion':presentacion,
                'cantidad':cantidad,
                'costo':costo,
                'precio':precio,
                'total':total
            };
            datos.push(fila_prod);

        });
        return datos;
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

    $(document).on('keyup', '.cost', function(evt){
        let costo_str=$(this).val();
        let costo='';
        let cantidad=$(this).closest('tr').find('.cant').val();
        let array_cadena_puntos=costo_str.split('.');
        if(array_cadena_puntos.length==1){
            costo= parseFloat(costo_str);
        }else{
            costo_solo_dos_decimales=costo_str.slice(0,5);
            array_dos_punto=costo_solo_dos_decimales.split('.')
            if(array_dos_punto.length==2){
                parte_entera=array_dos_punto[0];
                //aqui eliminamos el segundo punto decimal
                parte_decimal=array_dos_punto[1].replace('.',' ')
                console.log(parte_decimal)
                costo_solo_un_decimal=parte_entera+'.'+parte_decimal;
                costo=parseFloat(costo_solo_un_decimal);
                console.log("hola")
                console.log(costo)
                $(this).val(costo_solo_dos_decimales);
            }

        }
        if(!isNaN(costo)){
            let total=parseFloat(cantidad)*costo;
            $(this).closest('tr').find('.tot').val("$"+redondear(total));
        }else{
            $(this).val("0.0");
            $(this).closest('tr').find('.tot').val("$0.0");
        }
        calcular_totales();
    });


    
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

    function calcular_totales(){
        let total=0;
        $("#table-productos-carga tr").each(function(){
            let cantidad_str=$(this).find(".cant").val();
            let precio_str=$(this).find(".cost").val();
            let cantidad=0;
            let precio=0;
        
            if(cantidad_str!=''){
                cantidad=parseInt(cantidad_str);
            }
            if(precio_str!=''){
                precio=parseFloat(precio_str.replace("$",''));
            }
            total+=(cantidad*precio);
        });
        console.log(total)

        $("#total").text("$"+ redondear(total));
    }

    //validar que no se agregue dos veces el mismo producto
    function validar_producto_nuevo_unico(tabla, id){
        res=true;
        tabla.each(function(index){
            let id_producto_stock=$(this).find('.idprod').val();
            let tipo_prod=$(this).find('.tipo_prod').val();
            if(tipo_prod=="nuevo"){
                if(id_producto_stock===id){
                    res=false;
                }
            }else if(tipo_prod=="existe"){
                if(id_producto_stock===id){
                    res=false
                }
            }
            
            console.log("este es el id: "+id_producto_stock)

        });
        console.log("Resultado siempre da "+res)
        return res;
    }


})