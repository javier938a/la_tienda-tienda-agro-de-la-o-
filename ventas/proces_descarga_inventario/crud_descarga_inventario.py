from itertools import product
from django.views.generic import ListView, TemplateView
from ventas.models import CargaProductos, ProductoStockSucursal
from ventas.models import DescargaProductos, DetalleDescargaProducto
from django.db.models import Q
from django.http import JsonResponse
import json

class ListarDescargasProductos(ListView):
    template_name="proces_descarga_productos/listar_descargas_productos.html"
    model=DescargaProductos
    context_object_name="descarga_prod"

class ViewCrearDescargaProducto(TemplateView):
    template_name="proces_descarga_productos/crear_descarga_productos.html"


def listar_productos_a_descargar_por_sucursal_autocomplete(request):
    clave = request.POST.get('term')
    print(clave)
    sucursal=request.user.sucursal
    productos=None
    datos=[]
    if(clave.strip()!=''):
        lista_productos=ProductoStockSucursal.objects.filter(sucursal=sucursal).filter(Q(producto__nombre_producto__icontains=clave)|Q(producto__descripcion__icontains=clave)|Q(producto__codigo_producto=clave))
        for prod in lista_productos:
            fila=str(prod.id)+'|'+str(prod.producto.nombre_producto)+'|'+str(prod.producto.descripcion)+'|'+str(prod.cantidad)
            datos.append(fila)
    else:
        lista_productos=ProductoStockSucursal.objects.filter(sucursal=sucursal)
        for prod in lista_productos:
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

