from typing import List
from django.views.generic import TemplateView, ListView
from ventas.models import DevolucionVenta, Venta, DetalleVenta, Sucursal
from django.db.models import Q
from django.http import JsonResponse
class ListarDevolucionesVentas(ListView):
    template_name="proces_devolucion_venta/listar_devoluciones_ventas.html"
    model=DevolucionVenta
    context_object_name="devolucionVenta"


class ViewCrearDevolucionVenta(TemplateView):
    template_name="proces_devolucion_venta/crear_devolucion_venta.html"

    def get_context_data(self, **kwargs):
        context=super(ViewCrearDevolucionVenta, self).get_context_data(**kwargs)
        context['suc']=Sucursal.objects.filter(id=self.request.user.sucursal.id)
        return context

def obtener_ventas_autocomplete(request):
    clave=request.POST.get('term').strip()
    print("Hola: "+str(clave))
    venta_listar=None
    datos_ventas=[]
    if clave is not None:
        venta_listar=Venta.objects.filter(Q(numero_factura__icontains=clave))
    else:
        venta_listar=Venta.objects.all()
    for venta in venta_listar:
        datos_ventas.append(str(venta.id)+'|'+str(venta.numero_factura)+'|'+str(venta.fecha_venta))
    print(datos_ventas)
    return JsonResponse(datos_ventas, safe=False)

def listar_productos_de_venta(request):
    id=request.POST.get('id_venta')
    venta=Venta.objects.get(id=id)
    detalle_de_venta=DetalleVenta.objects.filter(factura=venta)
    print(detalle_de_venta)
    filas_ventas=''

    
    for detalle in detalle_de_venta:
        filas_ventas+='<tr>'
        filas_ventas+='<td class="id_detalle_venta">'+str(detalle.id)+'</td>'
        filas_ventas+='<td>'+detalle.producto_stock.producto.nombre_producto+'</td>'
        filas_ventas+='<td>'+detalle.producto_stock.presentacion.presentacion+'</td>'
        filas_ventas+='<td class="cant_vendida">'+str(detalle.cantidad)+'</td>'
        filas_ventas+='<td><input class="form-control precio_prod" value="$'+str(detalle.precio)+'" disabled></td>'
        filas_ventas+='<td>$'+str(detalle.total)+'</td>'
        filas_ventas+='<td><input class="form-control cant_devo"></td>'
        filas_ventas+='<td class="nueva_cant"></td>'
        filas_ventas+='<td class="dinero_devol"></td>'
        filas_ventas+='<td class="nuevo_total_venta"></td>'
        filas_ventas+='</tr>'
    datos={
        'filas_ventas':filas_ventas
    }


    return JsonResponse(datos, safe=True)

def efectuar_devolucion_venta(request):
    res=False
    id_venta=request.POST.get('id_venta')
    descripcion_devo=request.POST.get('descripcion_devo')
    sucursal=request.POST.get('id_sucursal')
    detalles_devo=request.POST.get('detalles_devo')
    print(detalles_devo)
    return JsonResponse({
        'res':res,
    })


    


