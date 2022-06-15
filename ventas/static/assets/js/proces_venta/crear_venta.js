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
    $("#sucursal").select2();

    let url_inv_autocomplete=$("#url_productos_inv_autocomplete").val();
    const csrftoken=getCookie('csrftoken');
    let id_sucursal=$("#sucursal").val();
    $("#tipo_busqueda").change(function(){
        let num_tipo=$(this).val();
        if(num_tipo==="1"){
            $("#codigo_barra").css({
                'display':'block',
            });
            $("#producto").css({
                'display':'none',
            })
        }else if(num_tipo==="2"){
            $("#producto").css({
                'display':'block'
            });
            $("#codigo_barra").css({
                'display':'none',
            });
        }
    });

    $("#tipo_venta").change(function(){
        let tipo_venta=$(this).val();
        if(tipo_venta==="1"){
            //alert("tipo_vente:"+tipo_venta);
            $("#txt_efectivo_sin_ticket").css({
                'display':'block',
            });
            $("#txt_efectivo").css({
                'display':'none',
            });
        }else if(tipo_venta==="2"){
            //alert("tipo_venta:"+tipo_venta);
            $("#txt_efectivo_sin_ticket").css({
                'display':'none',
            });
            $("#txt_efectivo").css({
                'display':'block',
            });
        }
    });

    $("#codigo_barra").keypress(function(evt){
        let codigo_barra=$("#codigo_barra").val();
        let url_agregar_prod_barra=$("#url_agregar_prod_barra").val();
        const csrftoken=getCookie("csrftoken");
        $.ajax({
            url:url_agregar_prod_barra,
            type:"POST",
            data:{
                csrfmiddlewaretoken:csrftoken,
                'codigo_barra':codigo_barra
            },
            dataType:'json',
            success:function(data){
              let res=data.res;
              console.log(data);
              if(res==true){
                let fila_producto=data.fila_producto;
                let id_prod_stock=data.id_prod_stock;
     
                console.log(fila_producto);
                $("#table-productos-venta").prepend(fila_producto);//y se agrega la fila a la tabla
                $("#codigo_barra").val("");
                calcular_totales();

              }else{
                  //toastr['warning']("No existe el producto ó no este codigo de barra no se a asignado a un producto especifico.")
                  $("#codigo_barra").val("");
              }
              
            }
        })
    })

    $("#producto").autocomplete({
        source:function(request, response){
            $.ajax({
                url:url_inv_autocomplete,
                type:"POST",
                data:{
                    csrfmiddlewaretoken:csrftoken,
                    'id_sucursal':id_sucursal,
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
            let prod_array=producto.split('|');
            id_prod_stock=prod_array[0];
            console.log(producto);
            let detalle_productos=$("#table-productos-venta tr")
            let esta_agregado=validar_producto_unico(detalle_productos, id_prod_stock);
            if(esta_agregado){//si esta agregando devuelve siempre false entonces se agrega el producto
                agregar_producto_detalle_venta(id_prod_stock);//agregando el producto
            }else{//de lo contrario es por ya hay un producto del mismo agregado y manda un error
                $("#producto").val("");//limpiando el campo de producto
                toastr['error']("Este producto ya esta agregado en la venta, porfavor ingrese otro producto");
                
            }
            

        }
    });

    function agregar_producto_detalle_venta(id_prod_stock){
        let url_add_prod_venta=$('#url_add_prod_venta').val();
        const csrftoken=getCookie('csrftoken');
        datos={
            csrfmiddlewaretoken:csrftoken,
            'id_prod_stock':id_prod_stock
        }
        $.ajax({
            url:url_add_prod_venta,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let res = data.res
                let fila_producto=data.fila_producto;
                if(res===true){//si res retorna true es porque de este producto aun hay en existencia
                    console.log(fila_producto);
                    $("#table-productos-venta").prepend(fila_producto);//y se agrega la fila a la tabla
                    $("#producto").val("");
                    calcular_totales();
                }else{
                    toastr['warning']("De este producto que intenta agregar ya no hay en existencia");
                }
            }
        })
    }

    $(document).on('input', '.cant', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
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
   
    $(document).on('keyup', '.cant', function(){//obteniendo el evento de cada una de las celdas en donde se ingresa la cantidad
        let cantidad= parseInt($(this).val());//obteniendo el total que se esta ingresando
        let precio=$(this).closest('tr').find('.pre').val().replace('$', '');//obtenendo el costo que esta en el canpo costo no se convierte porque pueda quee este vacio
                                        //closest devuelve el primer antecesor del elemento

        if(!isNaN(cantidad)){//si el el campo costo no esta vacio verifica el stock de este producto y si hay en existencia multiplica el costo por el total
            //datos para calcular el stock en tiempo real
            let id_prod_stock=$(this).closest('tr').find('.id_prod_stock').val();//id del producto de la fila
            const csrftoken=getCookie('csrftoken');
            let url_verificar_stock=$("#url_verificar_stock").val();//aqui se almacena la url que consulta el stock
            datos_prod={
                        csrfmiddlewaretoken:csrftoken,
                        'id_prod_stock':id_prod_stock,//se le envia el id de producto stock ubicacion
            }
            let fila_producto = $(this).closest('tr');//almacena la referencia a la fila del producto
            let campo_cantidad=$(this);//almacena la referencia al campo actual para usarlo dentro de la respuesta de la peticion ajax
            $.ajax({                  //que consulta el stock
                url:url_verificar_stock,
                type:'POST',
                data:datos,
                dataType:'json',
                success:function(data){
                    let cantidad_real=parseInt(data.cantidad_real);
                    if(cantidad>0 && cantidad<=cantidad_real){
                        console.log("Entra aqui")
                        let total=cantidad*parseFloat(precio);
        
                        fila_producto.find('.tot').val('$'+redondear(total));//se asigna el total campo del total
                        calcular_totales();
                    }else if(cantidad>cantidad_real){
                        console.log("cantidad real: "+cantidad_real)
                        campo_cantidad.val(""+cantidad_real);
                        calcular_totales();
                        toastr["error"](cantidad_real+" es la cantidad maxima que hay en existencia para este producto")
                    }
                    //si la cantidad ingresada es menor que la cantidad dispobible
                }
           });
        }else{
            fila_producto.find('.tot').val("$0.0");//de lo contrario el input del total sera vacio
            calcular_totales();
            //si el campo esta vacio obtiene la cantidad antes borrada y se la suma 
            
        }
       
    });


    function calcular_totales(){
        let total=0;
        $("#table-productos-venta tr").each(function(){
            let cantidad_str=$(this).find(".cant").val();
            let precio_str=$(this).find(".pre").val();
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
        let total_iva= redondear(total*0.13);
        $("#total_iva").text("$"+total_iva);
        //aqui iria el total sin iva
        $("#total_sin_iva").text("$"+total);
        let total_con_iva=total_iva+redondear(total);
        $("#total").text("$"+ redondear(total_con_iva));
    }
    let ticket=null;//esta variable es para cuando el usuario le de guardar a la venta almacene los datos de la venta devueltos
                    //para posteriormento imprimirlo en el evento del teclado
    $("#efectuar_venta").click(function(evt){
        console.log("Hola");
        let no_documento=$("#no_documento").val();
        console.log(no_documento.length);
        if(no_documento.length>0){            
            let detalles_venta_prod=$("#table-productos-venta tr");
            let res_validad_detalles=validar_detalles_ventas(detalles_venta_prod);
            if(res_validad_detalles==false){///si resultado es igual false entonces es porque todos los campos de ingresar cantidades es correcto y hay al menos un producto ingresado
                const csrftoken=getCookie("csrftoken");
                let detalles_de_facturas=obtener_detalles_productos(detalles_venta_prod);
                let numero_factura=$("#no_documento").val();
                let total_iva=$("#total_iva").text().replace('$','');
                let total_sin_iva=$("#total_sin_iva").text().replace('$', '');
                let total=$("#total").text().replace('$','');         
                let id_sucursal=$("#sucursal").val();
                let datos={
                    csrfmiddlewaretoken:csrftoken,
                    'numero_factura':numero_factura,
                    'id_sucursal':id_sucursal,
                    'total_iva':total_iva,
                    'total_sin_iva':total_sin_iva,
                    'total':total,
                    'detalles_de_facturas':JSON.stringify(detalles_de_facturas),
               }
               url_efectuar_venta=$("#url_efectuar_venta").val();
               $.ajax({
                    url:url_efectuar_venta,
                    type:'POST',
                    data:datos,
                    dataType:'json',
                    success:function(data){
                        let resultado=data.res;
                        if(resultado){
                            ticket=JSON.stringify(data.datos_factura);//si el resultado es true entonces obtengo los datos de la factura y mandarla a imprimirla
                            let tipo_venta=$("#tipo_venta").val();
                            if(tipo_venta==="2"){
                                $("#efectuar_venta").prop('disabled', true);
                                $("#txt_efectivo").prop('disabled', false);
                            }else if(tipo_venta==="1"){
                                $("#efectuar_venta").prop('disabled', true);
                                $("#txt_efectivo_sin_ticket").prop('disabled', false);
                            }

                            ///aqui el codigo que imprimira el ticket e redireccionara al listado de ventas
                        }else{
                            toastr['error']("La Venta no pudo ser registrada exitosamente");
                        }
                    }
               });
            }else{
                toastr['error']("Debe de ingresar al menos un producto y debe de ingresar todas las cantidades de todos los productos ingresados");
            }
        }else{
            toastr['error']("Debe de ingresar un numero de factura");
        }
    });

    //calculando cambio
    $("#txt_efectivo").keyup(function(evt){
        let total=0;
        let efectivo=0;
        if($("#total").text().replace("$", "")!=''){
            total=parseFloat($("#total").text().replace("$", ""));
        }
        if($("#txt_efectivo").val().replace("$", "")!=''){
            efectivo=parseFloat($("#txt_efectivo").val().replace("$", ""));
        }
        let cambio=efectivo-total;
        console.log("total "+total);
        console.log("efectivo "+efectivo);
        console.log("cambio "+cambio);
        
        $("#txt_cambio").val("$"+redondear(cambio));

    })

    $("#txt_efectivo_sin_ticket").keyup(function(evt){
        let total=0;
        let efectivo=0;
        if($("#total").text().replace("$", "")!=''){
            total=parseFloat($("#total").text().replace("$", ""));
        }
        if($("#txt_efectivo_sin_ticket").val().replace("$", "")!=''){
            efectivo=parseFloat($("#txt_efectivo_sin_ticket").val().replace("$", ""));
        }
        let cambio=efectivo-total;
        console.log("total "+total);
        console.log("efectivo "+efectivo);
        console.log("cambio "+cambio);
        
        $("#txt_cambio").val("$"+redondear(cambio));
    });

    $("#txt_efectivo_sin_ticket").keypress(function(evt){
        let num_tecla_enter=evt.which;
        if(num_tecla_enter===13){
            toastr['success']("Venta registrada exitosamente");                          
            setTimeout(function(){
                window.location.href=$("#url_listar_ventas").val();
            }, 1000) 
        }
 
    })

    $("#txt_efectivo").keypress(function(evt){
        console.log(evt.which)//la tecla enter es la numero 13 si da enter se imprime la factura
        console.log(ticket);
        let num_tecla_enter=evt.which;
        if(num_tecla_enter===13){
            url_print_ticket=$("#url_print_ticket").val();
            const csrftoken=getCookie('csrftoken');
            let datos={
                        csrfmiddlewaretoken:csrftoken,
                        'ticket':ticket
            }
            $.ajax({
                    url:url_print_ticket,
                    type:'POST',
                    data:datos,
                    dataType:'json',
                    success:function(data){
                    let resultado=data.res;
                    if(resultado){  
                        toastr['success']("Venta registrada exitosamente");                          
                        toastr['success']("Imprimiendo ticket");
                        setTimeout(function(){
                            window.location.href=$("#url_listar_ventas").val();
                        }, 1000)
    
                                            ///aqui el codigo que imprimira el ticket e redireccionara al listado de ventas
                    }else{
                            toastr['error']("La Venta no pudo ser registrada exitosamente");
                        }
                    }
            });
        }
    })

    //imprimiendo ticket al dar enter al input


    function validar_detalles_ventas(tabla_detalle){
        //cuenta que no haya ningun campo de cantidad vacio
        let cuenta_cantidad=0;
        let res=false;//si res cambia a true es porque hay campos de cantidades vacios
        tabla_detalle.each(function(index){
            let cantidad=$(this).find('.cant').val();
            if(cantidad.length===0){
                cuenta_cantidad++;
                console.log("Entro aqui...")
                console.log(cantidad);

            }
        })
        let num_filas=tabla_detalle.length;
        if(cuenta_cantidad>0 || num_filas===0){
            res=true
        }
        
        return res;
    }

    function obtener_detalles_productos(tabla_detalle){
        let datos=[];
        tabla_detalle.each(function(){
            let id_producto_stock=$(this).find('.id_prod_stock').val();
            let cantidad=$(this).find('.cant').val();
            let precio=$(this).find('.pre').val().replace('$','');
            let total=$(this).find('.tot').val().replace('$','');
            fila={'id_prod_stock':id_producto_stock, 'cantidad':cantidad, 'precio':precio, 'total':total};
            datos.push(fila);
        });
        return datos;
    }

    //validar que no se agregue dos veces el mismo producto
    function validar_producto_unico(tabla, id){
        res=true;
        tabla.each(function(index){
            id_producto_stock=$(this).find('.id_prod_stock').val();
            
            console.log("este es el id: "+id_prod_stock)
            if(id_producto_stock===id){
               res=false 
            }
        });
        console.log("Resultado siempre da "+res)
        return res;
    }

    
});