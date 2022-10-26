from email import contentmanager
from typing import List
from unittest import result
from django.views.generic import TemplateView, ListView, DetailView
from ventas.models import DevolucionVenta, DetalleDevolucionVenta, ProductoStockSucursal, Venta, DetalleVenta, Sucursal
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
import json

class ListarDevolucionesVentas(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_devolucion_venta/listar_devoluciones_ventas.html"
    model=DevolucionVenta
    context_object_name="devolucionVenta"


class ViewCrearDevolucionVenta(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_devolucion_venta/crear_devolucion_venta.html"

    def get_context_data(self, **kwargs):
        context=super(ViewCrearDevolucionVenta, self).get_context_data(**kwargs)
        context['suc']=Sucursal.objects.filter(id=self.request.user.sucursal.id)
        return context

class ViewDetalleDevolucion(LoginRequiredMixin, DetailView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_devolucion_venta/detalle_devolucion_venta.html"
    model=DevolucionVenta
    context_object_name="devolucion"
    def get_context_data(self, **kwargs):
        context=super(ViewDetalleDevolucion, self).get_context_data(**kwargs)
        devolucion=DevolucionVenta.objects.get(id=self.kwargs['pk'])
        detalle_devolucion=DetalleDevolucionVenta.objects.filter(devolucion_venta=devolucion)
        context['detalle_devolucion']=detalle_devolucion
        
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
    res=True
    id_venta=request.POST.get('id_venta')
    descripcion_devo=request.POST.get('descripcion_devo')
    id_sucursal=request.POST.get('id_sucursal')
    sucursal=Sucursal.objects.get(id=id_sucursal)
    total=request.POST.get('total')
    usuario=request.user
    detalles_devo= json.loads(request.POST.get('detalles_devo'))
    #Obteniendo la factura o venta que se registrara en la devolucion de venta
    try:
        factura=Venta.objects.get(id=id_venta)
        devolucion_venta_obj=DevolucionVenta.objects.get_or_create(
            factura=factura,
            descripcion=descripcion_devo,
            sucursal=sucursal,
            usuario=usuario,
            total_devolucion=total
        )

        resultado_devo=devolucion_venta_obj[1]
        if resultado_devo==True:
            devolucion_venta=devolucion_venta_obj[0]
            for detalle_dev in detalles_devo:
                #obteniendo el producto de cada venta 
                id_detalle_venta=detalle_dev['id_detalle_venta']
                #obteniendo el detalle de la venta por medio del ID del detalle de la venta para obtener el productostock
                detalle_venta=DetalleVenta.objects.get(id=id_detalle_venta)
                #obteniendo el producto stock
                producto_stock_suc=detalle_venta.producto_stock
                #obteniendo el precio del producto
                precio_producto=producto_stock_suc.precio
                #obteniendo la cantidad a devolver que es el total del dinero que se registrara en el campo total
                cantidad_devolver=detalle_dev['cantidad_devolver']
                #este seria la nueva cantidad que se registraria en la venta de donde se esta devolviendo
                nueva_cantidad=detalle_dev['nueva_cantidad']
                #aqui se obtendria el total del dinero a devolver que se registraria en total_devolucion
                total_devolucion=detalle_dev['dinero_devolver']
                #aqui se obtiene el nuevo total de venta que se utilizaria para actualizar la venta
                nuevo_total_venta=detalle_dev['nuevo_total_venta']
                #actualizando la nueva cantidad y el nuevo total de la venta
                DetalleVenta.objects.filter(id=id_detalle_venta).update(
                        cantidad=nueva_cantidad,
                        total=nuevo_total_venta  
                    )
                #actualizando el stock de los productos devueltos
                prod_stock=ProductoStockSucursal.objects.get(id=producto_stock_suc.id)
                stock_actual=int(prod_stock.cantidad)
                print("Heheheh")
                print(str(stock_actual))
                nuevo_stock=int(cantidad_devolver)+stock_actual
                ProductoStockSucursal.objects.filter(id=producto_stock_suc.id).update(
                    cantidad=nuevo_stock
                )
                #creando la devolucion sobre venta por cada producto
                devoluciones=DetalleDevolucionVenta.objects.create(
                    devolucion_venta=devolucion_venta,
                    producto_stock_suc=producto_stock_suc,
                    cantidad_devolver=cantidad_devolver, 
                    precio=precio_producto,
                    total=total_devolucion          
                )
            #actualizando el total de la venta con los productos devueltos
            
            efectuar_nueva_total_de_venta=DetalleVenta.objects.filter(factura__id=id_venta).aggregate(Sum('total'))
            print("Viendo que devuelve si se eliminan todas las ventas")
            print(efectuar_nueva_total_de_venta)
            #actualizando la venta si la venta queda a cero todos los productos quedaran a cero y la venta cero se justificara con la devolucion degistrada
            nuevo_total_sin_iva=float(efectuar_nueva_total_de_venta['total__sum'])
            nuevo_total_iva=nuevo_total_sin_iva*0.13
            nuevo_total_con_iva=nuevo_total_sin_iva+nuevo_total_iva
            #actualizando venta
            venta_a_actualizar=Venta.objects.filter(id=id_venta)
            venta_a_actualizar.update(
                total_iva= round(nuevo_total_iva,2),
                total_sin_iva=round(nuevo_total_sin_iva, 2),
                total_con_iva=round(nuevo_total_con_iva, 2)
            )
    except ValueError:
        print("Hubo un error de sistema favor llamar a soporte tecnico")
        res=False


    return JsonResponse({
        'res':res,
    })





