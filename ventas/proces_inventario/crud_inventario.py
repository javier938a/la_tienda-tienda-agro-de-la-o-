import json
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ventas.models import InventarioProductos, Sucursal, Producto, Presentacion, User, ProductoStockSucursal
from django.http import request, JsonResponse
from ventas.models import CargaProductos, DetalleCargaProductos
from ventas.forms import ProductoInventarioForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.urls import reverse

class ViewCrearInventario(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_inventario/crear_inventario.html"
    def get_context_data(self, **kwargs) :
        context=super(ViewCrearInventario, self).get_context_data()
        sucursales=Sucursal.objects.all()
        context['suc']=sucursales
        return context

class EditarProductoInventario(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_inventario/editar_producto_inventario.html"
    model=ProductoStockSucursal
    form_class=ProductoInventarioForm
    context_object_name='form'  

    def get_context_data(self, **kwargs):
        context=super(EditarProductoInventario, self).get_context_data(**kwargs)
        producto_stock_ubi=ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk']))
        cantidad_anterior=str(producto_stock_ubi.cantidad)
        costo_anterior=str(producto_stock_ubi.costo)
        precio_anterior=str(producto_stock_ubi.precio)
        print("Precio Anterior: "+str(precio_anterior)+" Costo anterior: "+str(costo_anterior))
        context.get('form').fields.get('usuario').empty_label=None
        usuario=ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk'])).usuario
        print(usuario)
        context.get('form').fields.get('usuario').queryset=User.objects.filter(id=usuario.id)
        sucursal=ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk'])).sucursal
        context.get('form').fields.get('sucursal').empty_label=None
        context.get('form').fields.get('sucursal').queryset=Sucursal.objects.filter(id=sucursal.id)
        context.get('form').fields.get('producto').empty_label=None
        producto=ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk'])).producto
        context.get('form').fields.get('producto').queryset=Producto.objects.filter(Q(id=producto.id))
        #asignando a dos imput ocultos el valor anterior para despues registrarlos
        context.get('form').fields.get('cantidad_anterior').initial=cantidad_anterior
        context.get('form').fields.get('precio_anterior').initial=precio_anterior
        context.get('form').fields.get('costo_anterior').initial=costo_anterior
        return context

    def form_valid(self, form):
        print(form)
        form_val=super(EditarProductoInventario, self).form_valid(form)
        
        producto=ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk'])).producto
        sucursal=ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk'])).sucursal
        cantidad=int(ProductoStockSucursal.objects.get(Q(id=self.kwargs['pk'])).cantidad)
        costo_anterior=form.cleaned_data.get('costo_anterior')
        precio_anterior=form.cleaned_data.get('precio_anterior')
        presentacion=form.cleaned_data.get('presentacion')
        costo=float(form.cleaned_data.get('costo'))
        precio=float(form.cleaned_data.get('precio'))
        print("Este es el costo "+str(costo_anterior) + " Este es el precio anterior "+str(precio_anterior))
        descripcion="Cambiando el precio o costo del producto "+str(producto)
        usuario_realiza_cambio=self.request.user
        total=0.0

        CargaProductos.objects.create(
                descripcion=descripcion,
                usuario=usuario_realiza_cambio,
                sucursal=sucursal,
                total=0.0
            )
            #obteniendo el ultimo registro ingresado
        carga_producto_obj=CargaProductos.objects.all().last()
        DetalleCargaProductos.objects.create(
                carga_producto=carga_producto_obj,
                producto=producto,
                presentacion=presentacion,
                cantidad_anterior=cantidad,
                cantidad=0,
                nueva_cantidad=cantidad,
                costo_anterior=costo_anterior,
                costo=costo,
                precio_anterior=precio_anterior,
                precio=precio,
                total=0.0,
                tipo_prod='existe'

            )
        

        return form_val
    
    def get_success_url(self):

        return reverse_lazy('store:list_inv')

class ViewEditarInventario(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
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

class DetalleInventario(LoginRequiredMixin, DetailView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    model=ProductoStockSucursal
    template_name="proces_inventario/detalle_inventario.html"
    context_object_name="producto"


class EliminarInventario(LoginRequiredMixin, DeleteView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_inventario/eliminar_inventario.html"
    model=ProductoStockSucursal
    context_object_name="producto_stock"
    success_url=reverse_lazy('store:list_inv')
    def get_context_data(self, **kwargs):
        context=super(EliminarInventario, self).get_context_data(**kwargs)
        
        print(context)
        return context
    

    

class ListarInventario(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_inventario/listar_inventario.html"



def obtener_lista_productos_inv_json(request):
    data=[]
    inventario=None
    draw=request.POST.get('draw')
    start=request.POST.get('start')
    length=request.POST.get('length')
    searchValue=request.POST.get('search[value]')
    condiciones_de_busqueda=None
    if searchValue!='':
        condiciones_de_busqueda=Q(fecha_de_registro__date__icontains=searchValue) | Q(sucursal__descripcion=searchValue) | Q(usuario__username__icontains=searchValue) | Q(producto__nombre_producto__icontains=searchValue) | Q(producto__codigo_barra__icontains=searchValue) | Q(producto__categoria__categoria__icontains=searchValue)
    
    totalRedords=ProductoStockSucursal.objects.all().count()

    totalRecordWithFilter=0
    if condiciones_de_busqueda is not None:
        if int(start)>=int(length):
            inventario=ProductoStockSucursal.objects.filter(condiciones_de_busqueda).order_by('-fecha_de_registro')[int(start):int(length)+int(start)]
        else:
            inventario=ProductoStockSucursal.objects.filter(condiciones_de_busqueda).order_by('-fecha_de_registro')[int(start):int(length)]
        totalRecordWithFilter=inventario.count()
    else:
        if int(start)>=int(length):
            inventario=ProductoStockSucursal.objects.all().order_by('-fecha_de_registro')[int(start):int(length)+int(start)]
        else:
            inventario=ProductoStockSucursal.objects.all().order_by('-fecha_de_registro')[int(start):int(length)]
        totalRecordWithFilter=inventario.count()
    
    for inv in inventario:
        url_detalle=reverse('store:det_inv', args=[inv.id])
        url_editar=reverse('store:edit_prod_inv', args=[inv.id])
        url_del=reverse('store:del_inv', args=[inv.id])
        action="""
                <div class="btn-group">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu">              
                        <li><a class="dropdown-item" href="%s">Detalle de producto</a></li>
                        <li><a class="dropdown-item" href="%s" class="dropdown-item">Editar Producto</a></li>
                        <li><a class="dropdown-item" href="%s">Eliminar producto</a></li>
                    </ul>
                </div>
        """%(url_detalle, url_editar, url_del)
        print(inv.producto.codigo_barra)
        
        if inv.producto.codigo_barra==None:
            data.append({
            'id':inv.id, 
            'sucursal':str(inv.sucursal), 
            'usuario':str(inv.usuario),             
            'fecha_de_registro':str(inv.fecha_de_registro), 
            'codigo':'No Existe', 
            'producto':str(inv.producto), 
            'cantidad':inv.cantidad, 
            'presentacion':str(inv.presentacion), 
            'categoria':str(inv.producto.categoria), 
            'costo':str(inv.costo), 
            'precio':str(inv.precio), 
            'action':action })
        else:
            data.append({
            'id':str(inv.id),
            'sucursal':str(inv.sucursal), 
            'usuario':str(inv.usuario),             
            'fecha_de_registro':str(inv.fecha_de_registro), 
            'codigo':str(inv.producto.codigo_barra), 
            'producto':str(inv.producto), 
            'cantidad':str(inv.cantidad), 
            'presentacion':str(inv.presentacion), 
            'categoria':str(inv.producto.categoria), 
            'costo':str(inv.costo), 
            'precio':str(inv.precio), 
            'action':action })
    
        

    return JsonResponse({
        'draw':int(draw),
        "iTotalRecords":totalRecordWithFilter,
        'iTotalDisplayRecords':totalRedords,
        'data':data
    }, safe=False)

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





    
