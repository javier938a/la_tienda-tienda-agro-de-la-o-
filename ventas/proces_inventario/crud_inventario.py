import json
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from ventas.models import InventarioProductos, Sucursal, Producto, Presentacion, User, ProductoStockSucursal
from django.http import request, JsonResponse
from django.db.models import Q
from django.core.serializers import serialize

class ViewCrearInventario(TemplateView):
    template_name="proces_inventario/crear_inventario.html"
    def get_context_data(self, **kwargs) :
        context=super(ViewCrearInventario, self).get_context_data()
        sucursales=Sucursal.objects.all()
        context['suc']=sucursales
        return context

class ViewEditarInventario(TemplateView):
    template_name="proces_inventario/editar_inventario.html"

    def get_context_data(self, **kwargs):
        sucursales=Sucursal.objects.all()
        context=super(ViewEditarInventario, self).get_context_data(**kwargs)
        inventario_prod=InventarioProductos.objects.get(id=self.kwargs['pk'])#obteniendo el inventario que se quiere editar en base al id pasado como argumento
        productos_inv=ProductoStockSucursal.objects.filter(inventario_productos=inventario_prod)#obteniendo los productos de ese inventario
        presentaciones=Presentacion.objects.all()
        context['suc']=sucursales
        context['inventario_prod']=inventario_prod
        context['productos_inv']=productos_inv
        context['presentaciones']=presentaciones
        context['id_inventario']=self.kwargs['pk']
        return context

class DetalleInventario(DetailView):
    model=InventarioProductos
    template_name="proces_inventario/detalle_inventario.html"
    context_object_name="inventario"
    def get_context_data(self, **kwargs):
        context=super(DetalleInventario, self).get_context_data(**kwargs)
        #obteniendo el listado de productos de este inventario
        detalle_inv=ProductoStockSucursal.objects.filter(inventario_productos__id=self.kwargs['pk'])
        context['detalle_inv']=detalle_inv

        print(context)
        return context


class EliminarInventario(TemplateView):
    pass

class ListarInventario(ListView):
    template_name="proces_inventario/listar_inventario.html"
    model=ProductoStockSucursal
    context_object_name="inventario"

    def get_queryset(self):
        sucursal=self.request.user.sucursal
        return self.model.objects.filter(sucursal=sucursal)

def obtener_productos_autocomplete(request):
    clave=request.GET.get('term').strip()
    print("Esto imprime")
    print(request.GET.get('term'))
    productos=None
    datos=[]
    if clave.strip()!='':
        productos=Producto.objects.filter(Q(nombre_producto__icontains=clave))
        for prod in productos:
            datos.append(str(prod.pk)+'|'+str(prod.descripcion))
    else:
        productos=Producto.objects.all()
        for prod in productos:
            datos.append(str(prod.pk)+'|'+str(prod.descripcion))
    return JsonResponse(datos, safe=False)

def agregar_producto_detalle(request):
    id_producto=request.POST.get('id_producto')
    producto=Producto.objects.get(pk=id_producto)
    presentaciones=Presentacion.objects.all()
    fila_producto='<tr>'
    fila_producto+='<td><input class="form-control idprod" type="text" value="'+str(id_producto)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto.nombre_producto)+'" disabled></td>'
    fila_producto+='<td>'+obtener_presentaciones(presentaciones)+'</td>'
    fila_producto+='<td><input class="form-control cant" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control cost" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control pre" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control tot" type="text" value="" disabled></td>'
    fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
    fila_producto+='</tr>'

    datos={
        'fila_producto':fila_producto
    }
    return JsonResponse(datos, safe=False)
    
def update_producto_detalle(request):
    id_producto=request.POST.get('id_producto')
    producto=Producto.objects.get(pk=id_producto)
    presentaciones=Presentacion.objects.all()
    fila_producto='<tr>'
    fila_producto+='<td><input class="form-control idprod" type="text" value="'+str(id_producto)+'" disabled><input class="id_inv" type="hidden" value=""></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto.nombre_producto)+'" disabled></td>'
    fila_producto+='<td>'+obtener_presentaciones(presentaciones)+'</td>'
    fila_producto+='<td><input class="form-control cant" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control cost" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control pre" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control tot" type="text" value="" disabled></td>'
    fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
    fila_producto+='</tr>'

    datos={
        'fila_producto':fila_producto
    }
    return JsonResponse(datos, safe=False)
    


def obtener_presentaciones(presentaciones):
    sel='<select class="form-control select">'
    sel+='<option value="">Seleccione</option>'
    for pre in presentaciones:
        sel+='<option value="'+str(pre.pk)+'">'+str(pre.presentacion)+'</option>'
    
    sel+="</select>"
    return sel

def guardar_datos_inventario(request):
    descripcion=request.POST.get('descripcion')
    id_sucursal=request.POST.get('id_sucursal')
    total=request.POST.get('total')
    productos_json= json.loads(request.POST.get('productos_json'))
    #obteniendo el usuario
    user=User.objects.get(id=request.user.id)#obteniendo el usuario que esta loguiado en el sistema
    #obteniendo la sucursal
    sucursal=Sucursal.objects.get(id=id_sucursal)#obteniendo la sucursal a donde se almacenaran los productos
    crear_inv=InventarioProductos.objects.get_or_create(usuario=user, descripcion=descripcion, sucursal=sucursal, total=total)
    inventario=crear_inv[0]
    #una vez creado el inventario se registrar los detalles del inventario ya que es necesario para crearlo
    cuenta_res=0
    res=False
    for prod in productos_json:
        producto=Producto.objects.get(id=prod['id_producto'])
        presentacion=Presentacion.objects.get(id=prod['id_presentacion'])
        cantidad=prod['cantidad']
        costo=prod['costo']
        precio=prod['precio']
        total=prod['total']
        ProductoStockSucursal.objects.create(
            inventario_productos=inventario, 
            producto=producto, 
            presentacion=presentacion, 
            cantidad=cantidad, 
            costo=costo, 
            precio=precio, 
            total=total
        )
        cuenta_res=cuenta_res+1
    
    if(cuenta_res==len(productos_json)):
        res=True



    return JsonResponse({'res':res,}, safe=False)

def actualizar_datos_inventario(request):
    descripcion=request.POST.get('descripcion')
    id_sucursal=request.POST.get('id_sucursal')
    total=request.POST.get('total')
    id_inventario=request.POST.get('id_inventario')

    productos_json=json.loads(request.POST.get('productos_json'))
    ##obteniendo los objectos para actualizar el inventario
    user=User.objects.get(id=request.user.id)
    sucursal=Sucursal.objects.get(id=id_sucursal)
    inventario_filter=InventarioProductos.objects.filter(id=id_inventario)
    inventario_filter.update(usuario=user, descripcion=descripcion, sucursal=sucursal, total=total)
    #una vez actualizado el inventario se tiene que actualizar los productos de ese inventario y los que no esten creados agregarlos
    productos_detalle_update=ProductoStockSucursal.objects.filter(inventario_productos=inventario_filter.get(id=id_inventario))#obteniendo todos los productos de este inventario
    #obteniendo el inventario para crear los nuevos productos que se agreguen
    inventario=InventarioProductos.objects.get(id=id_inventario)
    #contara si todos los productos se actualizaron y se crearon correctamente
    cuenta_res=0
    #si res pasa a True es porque todo se actualizo correctamente
    res=False
    for prod in productos_json:
        id_prod_inv=""
        if 'id_prod_inv' in prod:        
            id_prod_inv=prod['id_prod_inv']
            presentacion=Presentacion.objects.get(id=prod['id_presentacion'])
            cantidad=prod['cantidad']
            costo=prod['costo']
            precio=prod['precio']
            total=prod['total']
   
            
            
            ProductoStockSucursal.objects.filter(id=id_prod_inv).update(
                                                        presentacion=presentacion,
                                                        cantidad=cantidad,
                                                        costo=costo, 
                                                        precio=precio,
                                                        total=total                                                 
                                                    )
            cuenta_res=cuenta_res+1
        else:
            id_producto=prod['id_producto']
            producto=Producto.objects.get(id=id_producto)
            presentacion=Presentacion.objects.get(id=prod['id_presentacion'])
            cantidad=prod['cantidad']
            costo=prod['costo']
            precio=prod['precio']
            total=prod['total']
            ProductoStockSucursal.objects.create(
                    inventario_productos=inventario, 
                    producto=producto, 
                    presentacion=presentacion, 
                    cantidad=cantidad, 
                    costo=costo, 
                    precio=precio, 
                    total=total
                ) 
            cuenta_res=cuenta_res+1
            
        if(cuenta_res==len(productos_json)):
            res=True

        
    
    return JsonResponse({'res':res}, safe=False)





    
