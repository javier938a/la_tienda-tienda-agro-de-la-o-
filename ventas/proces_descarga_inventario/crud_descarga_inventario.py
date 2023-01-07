from django.views.generic import TemplateView, DetailView
from ventas.models import ProductoStockSucursal
from ventas.models import DescargaProductos, DetalleDescargaProducto
from django.contrib.auth.mixins import LoginRequiredMixin
from ventas.models import Sucursal
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
import json

class ListarDescargasProductos(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_descarga_productos/listar_descargas_productos.html"
    context_object_name="descarga_prod"



def obtener_lista_de_descarga_productos_json(request):
    data=[]
    descarga_productos=None
    draw=request.POST.get('draw')
    start=request.POST.get('start')
    length=request.POST.get('length')
    searchValue=request.POST.get('search[value]')
    condiciones_de_busqueda=None
    if searchValue!='':
        condiciones_de_busqueda=Q(fecha_descarga__date__icontains=searchValue) | Q(descripcion__icontains=searchValue) | Q(usuario__username__icontains=searchValue) | Q(sucursal__descripcion__icontains=searchValue)
    totalRecords=DescargaProductos.objects.all().count()

    totalRecordWithFilter=0
    if condiciones_de_busqueda is not None:
        if int(start)>=int(length):
            descarga_productos=DescargaProductos.objects.filter(condiciones_de_busqueda).order_by('-fecha_descarga')[int(start):int(length)+int(start)]
        else:
            descarga_productos=DescargaProductos.objects.filter(condiciones_de_busqueda).order_by('-fecha_descarga')[int(start):int(length)]
        totalRecordWithFilter=descarga_productos.count()
    else:
        if int(start)>=int(length):
            descarga_productos=DescargaProductos.objects.all().order_by('-fecha_descarga')[int(start):int(length)+int(start)]
        else:
            descarga_productos=DescargaProductos.objects.all().order_by('-fecha_descarga')[int(start):int(length)]
        
    for descarga in descarga_productos:
        url_detalle_descarga=reverse('store:detalle_descarga', args=[descarga.id])
        action="""
                <div class="btn-group">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="%s">Detalle de descarga</a></li>
                    </ul>
                </div>
            """%(url_detalle_descarga)
        data.append({
            'id':str(descarga.id),
            'usuario':str(descarga.usuario),
            'fecha_de_descarga':str(timezone.localtime(descarga.fecha_descarga)),
            'descripcion':str(descarga.descripcion),
            'sucursal':str(descarga.sucursal),
            'total':str(descarga.total),
            'action':action
        })
    return JsonResponse({
        'draw':int(draw),
        'iTotalRecords':totalRecordWithFilter,
        'iTotalDisplayRecords':totalRecords,
        'data':data
    })


class ViewDetalleDescargaProducto(LoginRequiredMixin, DetailView):
    login_url='/ventas/login/'
    redirect_field_name="redirect_to"
    template_name="proces_descarga_productos/detalle_descarga_producto.html"
    model=DescargaProductos
    context_object_name="descargas"

    def get_context_data(self, **kwargs):
        context=super(ViewDetalleDescargaProducto, self).get_context_data(**kwargs)
        descarga_productos=DescargaProductos.objects.get(id=self.kwargs['pk'])
        detalle_descarga_producto_carga=DetalleDescargaProducto.objects.filter(descarga_productos=descarga_productos)
        context['detalle_descarga_producto_carga']=detalle_descarga_producto_carga
        return context

class ViewCrearDescargaProducto(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_descarga_productos/crear_descarga_productos.html"

    def get_context_data(self, **kwargs):
        context= super(ViewCrearDescargaProducto, self).get_context_data(**kwargs)
        context['sucursales']=Sucursal.objects.all()
        return context


def listar_productos_a_descargar_por_sucursal_autocomplete(request):
    clave = request.POST.get('term')
    id_sucursal=request.POST.get('id_sucursal')
    print(clave)
    sucursal=Sucursal.objects.get(id=id_sucursal)
    productos=None
    datos=[]
    if(clave.strip()!=''):
        lista_productos=ProductoStockSucursal.objects.filter(sucursal=sucursal).filter(Q(producto__nombre_producto__icontains=clave)|Q(producto__descripcion__icontains=clave)|Q(producto__codigo_producto=clave))
        for prod in lista_productos:
            if prod.producto!= None:
                fila=str(prod.id)+'|'+str(prod.producto.nombre_producto)+'|'+str(prod.producto.descripcion)+'|'+str(prod.cantidad)
                datos.append(fila)
    else:
        lista_productos=ProductoStockSucursal.objects.filter(sucursal=sucursal)
        for prod in lista_productos:
            if prod.producto!= None:
                fila=str(prod.id)+'|'+str(prod.producto.nombre_producto)+'|'+str(prod.producto.descripcion)+'|'+str(prod.cantidad)
                datos.append(fila)
    
    return JsonResponse(datos, safe=False)


def agregar_producto_a_descargar_a_detalle(request):
    id_prod_stock=request.POST.get('id_prod_stock')
    
    producto_stock_ubi=ProductoStockSucursal.objects.get(id=id_prod_stock)
    fila_producto='<tr>'
    fila_producto+='<td><input class="form-control idprod" type="text" value="'+str(producto_stock_ubi.id)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.producto.nombre_producto)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.producto.descripcion)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.presentacion)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.cantidad)+'" disabled></td>'
    fila_producto+='<td><input class="form-control cant" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control cost" type="text" value="'+str(producto_stock_ubi.costo)+'" disabled></td>'
    fila_producto+='<td><input class="form-control tot" type="text" value="" disabled></td>'
    fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
    fila_producto+='</tr>'

    datos={
        'fila_producto':fila_producto,
    }
    return JsonResponse(datos, safe=False)


def efectuar_descarga_de_productos(request):
    detalles_de_productos_descarga= json.loads(request.POST.get('detalles_descarga_producto'))
    descripcion=request.POST.get('descripcion')
    usuario=request.user
    sucursal=request.user.sucursal
    total=request.POST.get('total')
    #aqui se guarda y se obtiene los datos de la descarga 
    descarga_producto_obj=DescargaProductos.objects.get_or_create(
        descripcion=descripcion,
        usuario=usuario,
        sucursal=sucursal, 
        total=total
    )
    res=False
    res_save_descarga=descarga_producto_obj[1]
    if res_save_descarga==True:
        descarga_productos=descarga_producto_obj[0]
        for producto_detalle in detalles_de_productos_descarga:
            id_prod_stock=producto_detalle['id_prod_stock']
            producto_stock_suc=ProductoStockSucursal.objects.get(id=id_prod_stock)
            producto=producto_stock_suc.producto
            presentacion=producto_stock_suc.presentacion
            cantidad_anterior=producto_stock_suc.cantidad
            cantidad_a_descargar=producto_detalle['cantidad']
            nueva_cantidad=int(cantidad_anterior)-int(cantidad_a_descargar)
            costo=producto_detalle['costo']
            precio=producto_stock_suc.precio
            total=producto_detalle['total']

            #creando la tabla detalle de la descarga en la tabla Detalle de descarga
            DetalleDescargaProducto.objects.create(
                descarga_productos=descarga_productos,
                producto=producto,
                presentacion=presentacion,
                cantidad_anterior=cantidad_anterior,
                cantidad_descargada=cantidad_a_descargar,
                nueva_cantidad=nueva_cantidad,
                costo=costo,
                precio=precio,
                total=total
            )

            ##una ver registrado los detalles es hora de actualizar el stock del producto
            ProductoStockSucursal.objects.filter(id=id_prod_stock).update(
                cantidad=nueva_cantidad
            )
        res=True
    print(request.POST)
    return JsonResponse({'res':res})

