import json
from math import prod
from multiprocessing import context
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from ventas.models import CargaProductos, DetalleCargaProductos, User, Presentacion, Sucursal, ProductoStockSucursal, Producto
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

class ViewCargaInventario(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_carga_productos/crear_carga_producto.html"
    def get_context_data(self, **kwargs):
        context=super(ViewCargaInventario, self).get_context_data(**kwargs)
        sucursal=Sucursal.objects.all()
        context['suc']=sucursal
        return context

class ListarCargaProductos(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_carga_productos/listar_carga_productos.html"


def obtener_lista_cargas_de_productos_json(request):
    #comentarios sobre la explicacion de este codigo 
    #estan en el obtener_lista_productos
    data=[]
    cargas_productos=None
    draw=request.POST.get('draw')
    start=request.POST.get('start')
    length=request.POST.get('length')
    searchValue=request.POST.get('search[value]')
    condiciones_de_busqueda=None
    if searchValue!='':
        condiciones_de_busqueda=Q(fecha_carga__date__icontains=searchValue) | Q(descripcion__icontains=searchValue) | Q(usuario__username__icontains=searchValue) | Q(sucursal__descripcion__icontains=searchValue)
    totalRecords=CargaProductos.objects.all().count()

    totalRecordWithFilter=0
    if condiciones_de_busqueda is not None:
        if int(start)>=int(length):
            cargas_productos=CargaProductos.objects.filter(condiciones_de_busqueda).order_by('-fecha_carga')[int(start):int(length)+int(start)]
        else:
            cargas_productos=CargaProductos.objects.filter(condiciones_de_busqueda).order_by('-fecha_carga')[int(start):int(length)]
        totalRecordWithFilter=cargas_productos.count()
    else:
        if int(start)>=int(length):
            cargas_productos=CargaProductos.objects.all().order_by('-fecha_carga')[int(start):int(length)+int(start)]
        else:
            cargas_productos=CargaProductos.objects.all().order_by('-fecha_carga')[int(start):int(length)]
        totalRecordWithFilter=cargas_productos.count()
   
    for carga in cargas_productos:
        url_detalle=reverse('store:detalle_carga', args=[carga.id])
        action="""
                <div class="btn-group">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="%s">Detalle de carga</a></li>
                    </ul>
                </div>
        """%(url_detalle)
    
        data.append({
            'id':str(carga.id),
            'usuario':str(carga.usuario),
            'fecha_carga':str(timezone.localtime(carga.fecha_carga)),
            'descripcion':str(carga.descripcion),
            'sucursal':str(carga.sucursal),
            'total':str(carga.total),
            'action':action
        })
    return JsonResponse({
        'draw':int(draw),
        'iTotalRecords':totalRecordWithFilter,
        'iTotalDisplayRecords':totalRecords,
        'data':data
    }, safe=False)


class DetalleCargaInventario(LoginRequiredMixin, DetailView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_carga_productos/detalle_carga_producto.html"
    model=CargaProductos
    context_object_name="carga_prod"
    def get_context_data(self, **kwargs):
        context=super(DetalleCargaInventario, self).get_context_data(**kwargs)
        detalle_carga_carga=DetalleCargaProductos.objects.filter(carga_producto__id=self.kwargs['pk'])
        context['detalle_producto_carga']=detalle_carga_carga
        return context



def listar_productos_cargados_y_sin_cargar_autocomplete(request):
    id_sucursal=request.POST.get('id_sucursal')
    sucursal=Sucursal.objects.get(id=id_sucursal)
    clave=request.POST.get('term')
    producto_stock=None
    producto=None
    print("id_sucursal="+str(sucursal))
    print(clave)
    if clave.strip()!='':
        producto=Producto.objects.filter(Q(nombre_producto__icontains=clave)| Q(descripcion__icontains=clave))
        producto_stock=ProductoStockSucursal.objects.filter(sucursal=sucursal).filter(Q(producto__nombre_producto__icontains=clave)|Q(producto__descripcion__icontains=clave))
    else:
        producto=Producto.objects.all()
        producto_stock=ProductoStockSucursal.objects.filter(sucursal=sucursal)
    list_prod=[]
    for producto in producto:
        if producto.nombre_producto!=None:
            print(producto)
            #esta validacion es solo para que no se puedan agregar los productos que ya se cargaron el el inventario
            if ProductoStockSucursal.objects.filter(Q(producto=producto) & Q(sucursal=sucursal)).exists()==False:
                fila=str(producto.id)+'|'+str(producto.nombre_producto)+'|'+'ninguna'+'|'+'0'+'|nuevo'
                list_prod.append(fila)
    #AQUI SE LISTARIAN TODOS LOS PRODUCTOS QUE YA EXISTEN EN EL INVENTARIO
    print(producto_stock)
    for producto_stock in producto_stock:
        if producto_stock.producto != None:
            fila=str(producto_stock.id)+'|'+str(producto_stock.producto.nombre_producto)+'|'+str(producto_stock.presentacion)+', Cantidad:|'+str(producto_stock.cantidad)+'|existe'
            list_prod.append(fila)   

    return JsonResponse(list_prod, safe=False)


def agregar_producto_detalle_carga(request):
    id_producto_de_donde_sea=request.POST.get('id_producto')
    stock_actual=request.POST.get('stock_actual')
    presentacion=request.POST.get('presentacion')
    fila_producto="<tr>"
    datos=[]
    res=False
    if stock_actual is not None:#verificamos primero que el stock actual no sea none
        stock=int(stock_actual)#convertimos la cadena
        if stock>0:#verificamos que sea mayor que cero
            if presentacion!='ninguna':
                producto_tock=ProductoStockSucursal.objects.get(id=id_producto_de_donde_sea)
                fila_producto+='<td>'
                fila_producto+='<input class="form-control tipo_prod" type="hidden" value="existe">'
                fila_producto+='<input class="form-control idprod" type="text" value="'+str(producto_tock.id)+'" disabled></td>'
                fila_producto+='<td>'
                fila_producto+='<input class="form-control" type="text" value="'+str(producto_tock.producto)+'" disabled></td>'
                fila_producto+='<td>'
                fila_producto+='<input class="form-control presentacion" type="hidden" value="'+str(producto_tock.presentacion.id)+'">'
                fila_producto+='<input class="form-control" type="text" value="'+str(producto_tock.presentacion)+'" disabled>'
                fila_producto+='</td>'
                fila_producto+='<td><input class="form-control cant" type="text" value="1" ></td>'
                fila_producto+='<td><input class="form-control cost" type="text" value="'+str(producto_tock.costo)+'" ></td>'
                fila_producto+='<td><input class="form-control pre" type="text" value="'+str(producto_tock.precio)+'"></td>'
                #calculando el total
                total=1*float(producto_tock.costo)
                fila_producto+='<td><input class="form-control tot" type="text" value="$'+str(total)+'" disabled></td>'
                fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
                fila_producto+='</tr>'
                res=True
        elif stock==0:
            if presentacion=='ninguna':
                producto=Producto.objects.get(id=id_producto_de_donde_sea)
                fila_producto+='<td>'
                fila_producto+='<input class="form-control tipo_prod" type="hidden" value="nuevo">'
                fila_producto+='<input class="form-control idprod" type="hidden" value="'+str(producto.id)+'" disabled></td>'
                fila_producto+='</td>'
                fila_producto+='<td>'
                fila_producto+='<input class="form-control" type="text" value="'+str(producto.nombre_producto)+'" disabled>'
                fila_producto+='</td>'
                presentaciones=Presentacion.objects.all()
                fila_producto+='<td>'+obtener_presentaciones(presentaciones)+'</td>'
                fila_producto+='<td><input class="form-control cant" type="text" value=""></td>'
                fila_producto+='<td><input class="form-control cost" type="text" value="" ></td>'
                fila_producto+='<td><input class="form-control pre" type="text" value=""></td>'
                fila_producto+='<td><input class="form-control tot" type="text" value="" disabled></td>'
                fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
                fila_producto+='</tr>'
                res=True
            elif presentacion!='ninguna':
                producto_tock=ProductoStockSucursal.objects.get(id=id_producto_de_donde_sea)
                fila_producto+='<td>'
                fila_producto+='<input class="form-control tipo_prod" type="hidden" value="existe">'
                fila_producto+='<input class="form-control idprod" type="text" value="'+str(producto_tock.id)+'" disabled></td>'
                fila_producto+='<td>'
                fila_producto+='<input class="form-control" type="text" value="'+str(producto_tock.producto)+'" disabled></td>'
                fila_producto+='<td>'
                fila_producto+='<input class="form-control presentacion" type="hidden" value="'+str(producto_tock.presentacion.id)+'">'
                fila_producto+='<input class="form-control" type="text" value="'+str(producto_tock.presentacion)+'" disabled>'
                fila_producto+='</td>'
                fila_producto+='<td><input class="form-control cant" type="text" value="1" ></td>'
                fila_producto+='<td><input class="form-control cost" type="text" value="'+str(producto_tock.costo)+'" ></td>'
                fila_producto+='<td><input class="form-control pre" type="text" value="'+str(producto_tock.precio)+'"></td>'
                #calculando el total
                total=1*float(producto_tock.costo)
                fila_producto+='<td><input class="form-control tot" type="text" value="$'+str(total)+'" disabled></td>'
                fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
                fila_producto+='</tr>'
                res=True
    
    datos={
        'res':res,
        'fila_producto':fila_producto
    }

    return JsonResponse(datos, safe=False)
        

def cargar_producto_inventario(request):
    descripcion=request.POST.get('descripcion')
    id_sucursal=request.POST.get('id_sucursal')
    sucursal = Sucursal.objects.get(id=id_sucursal)
    detalles_productos= json.loads(request.POST.get('detalles_productos'))
    user=request.user
    total=request.POST.get('total')
    res=True
    try:
        ##primero se crea y se obtiene la carga de producto
        CargaProductos.objects.create(
            descripcion=descripcion,
            usuario=user,
            sucursal=sucursal,
            total=total
        )       
        
        cargaProducto=CargaProductos.objects.all().last()#se obtiene la carga 
        for producto in detalles_productos:#se reccorren los detalles uno por uno y se obtienen los valores
            tipo_prod=producto['tipo_prod']
            id_prod_o_stockubi=producto['id_prod_o_stockubi']
            id_presentacion=producto['id_presentacion']
            cantidad=int(producto['cantidad'])
            costo=producto['costo']
            precio=producto['precio']
            total=producto['total']
            presentacion=Presentacion.objects.get(id=id_presentacion)#obteniendo el id de la presentacion del producto 

            #registrando la carga de producto
            producto=None
            if tipo_prod=="nuevo":#si es nuevo el producto se obtiene el producto objeto a partir del id 
                producto=Producto.objects.get(id=id_prod_o_stockubi)
                DetalleCargaProductos.objects.create(#creando el producto
                    carga_producto=cargaProducto,
                    producto=producto,
                    presentacion=presentacion,
                    cantidad_anterior=0,
                    cantidad=cantidad,
                    nueva_cantidad=cantidad,
                    costo_anterior=0.0,
                    costo=costo,
                    precio_anterior=0.0,
                    precio=precio,
                    total=total,
                    tipo_prod=tipo_prod
                )
                
            
            elif tipo_prod=='existe':#si no es nuevo se obtiene el producto en base al producto stock ubicacion
                producto_stock_ubi=ProductoStockSucursal.objects.get(id=id_prod_o_stockubi)
                producto=producto_stock_ubi.producto##obteniendo el objeto producto
                cantidad_anterior=int(producto_stock_ubi.cantidad)#obteniendo la cantidad anterior a ser sumada con esta nueva cantidad
                nueva_cantidad=cantidad_anterior+int(cantidad)#a la cantidad anterior se le suma la nueva cantidad para obtener la cantidad actual
                
                #ahora iriamos con los costos costo anterior y costo actual
                costo_anterior=float(producto_stock_ubi.costo)
                precio_anterior=float(producto_stock_ubi.precio)
                
                DetalleCargaProductos.objects.create(#creando el producto
                    carga_producto=cargaProducto,
                    producto=producto,
                    presentacion=presentacion,
                    cantidad_anterior=cantidad_anterior,
                    cantidad=cantidad,
                    nueva_cantidad=nueva_cantidad,
                    costo_anterior=costo_anterior,
                    costo=costo,
                    precio_anterior=precio_anterior,
                    precio=precio,
                    total=total,
                    tipo_prod=tipo_prod
                )
            


            ##Una vez creado la carga se tiene que modificar el stock de el inventario o ProductoStockUbicacion
            if tipo_prod=='nuevo':##si el producto es nuevo se agrega al inventario y se le asigna la cantidad y costo del producto que se le a ingresado ya que no hay registro o stock de ese producto no se tiene que sumar nada
                producto=Producto.objects.get(id=id_prod_o_stockubi)
                presentacion=Presentacion.objects.get(id=id_presentacion)

                ProductoStockSucursal.objects.create(
                    sucursal=sucursal,
                    usuario=user,
                    producto=producto,
                    presentacion=presentacion,
                    cantidad=cantidad,
                    costo=costo,
                    precio=precio
                )
            elif tipo_prod=='existe':#si el producto ya existe en el inventario se actualiza nomas dicho producto en stock
                #obiamente antes de actualizar hay que tener en cuenta el stock actual para sumarle lo que el usuario le ha ingresado
                producto_stockubi=ProductoStockSucursal.objects.get(id=id_prod_o_stockubi)
                cantidad_actual=int(producto_stockubi.cantidad)
                nueva_cantidad=cantidad_actual+cantidad
                ProductoStockSucursal.objects.filter(id=id_prod_o_stockubi).update(
                cantidad=nueva_cantidad,
                costo=costo,
                precio=precio  
                )
    except ValueError:
        print("Hubo un error del sistema favor contactarse con soporte tecnico")
        res=False

    print(detalles_productos)

    return JsonResponse({
        'res':res,
    })
            
def obtener_presentaciones(presentaciones):
    sel='<select class="form-control presentacion select">'
    sel+='<option value="">Seleccione</option>'
    for pre in presentaciones:
        sel+='<option value="'+str(pre.pk)+'">'+str(pre.presentacion)+'</option>'
    
    sel+="</select>"
    return sel

