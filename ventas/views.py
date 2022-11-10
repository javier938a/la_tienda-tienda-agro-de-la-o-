from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView
from ventas.proces_login.op_login import iniciar_session, cerrar_session
from ventas.proces_usuario.crud_usuario import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario, DetalleUsuario
from ventas.proces_tipo_usuario.crud_tipo_usuario import ListarTipoUsuario, CrearTipoUsuario, EditarTipoUsuario, EliminarTipoUsuario
from ventas.proces_proveedor.crud_proveedor import ListarProveedor, CrearProveedor, EditarProveedor, EliminarProveedor
from ventas.proces_sucursal.crud_sucursal import ListarSucursal, CrearSucursal, EditarSucursal, EliminarSucursal
from ventas.proces_categoria_producto.crud_categoria import ListarCategoriasProducto, CrearCategoriaProducto, EditarCategoriaProducto, EliminarCategoriaProducto
from ventas.proces_producto.crud_producto import ListarProductos, CrearProducto, EditarProducto, EliminarProducto
from ventas.proces_presentacion.crud_presentacion import ListarPresentacion, CrearPresentacion, EditarPresentacion, EliminarPresentacion
from ventas.proces_inventario.crud_inventario import ListarInventario,  ViewCrearInventario, ViewEditarInventario, EliminarInventario, obtener_productos_autocomplete
from ventas.proces_carga_inventario.crud_carga_inventario import ListarCargaProductos, ViewCargaInventario, DetalleCargaInventario, listar_productos_cargados_y_sin_cargar_autocomplete, agregar_producto_detalle_carga, cargar_producto_inventario
from ventas.proces_descarga_inventario.crud_descarga_inventario import ListarDescargasProductos, ViewCrearDescargaProducto, listar_productos_a_descargar_por_sucursal_autocomplete, agregar_producto_a_descargar_a_detalle, efectuar_descarga_de_productos
from ventas.proces_inventario.crud_inventario import DetalleInventario, agregar_producto_detalle, guardar_datos_inventario, actualizar_datos_inventario, update_producto_detalle
from ventas.proces_venta.crud_venta import ListarVentas, ViewCrearVenta, ViewDetalleVenta, imprimir_ticket, Obtener_ticket,verificar_stock_producto, obtener_productos_inventario_autocomplete, agregar_producto_detalle_venta, efectuar_venta
from ventas.proces_venta.crud_venta import agregar_producto_a_detalle_por_codigo
from ventas.proces_reportes.reportes import  ViewSelectReporteVentas ,PrintViewReporteVentas
from ventas.proces_reportes.reportes import grafico_reporte_ventas
from ventas.proces_devoluciones_venta.crud_devoluciones_venta import ListarDevolucionesVentas, ViewCrearDevolucionVenta, ViewDetalleDevolucion, obtener_ventas_autocomplete, listar_productos_de_venta, efectuar_devolucion_venta
from ventas.proces_apertura_corte.crud_apertura_corte import ListarAperturaCorte, CrearApertura, proces_efectuar_apertura_caja, proces_verificar_si_hay_apertura_de_caja
from ventas.proces_caja.crud_caja import ListarCajas,CrearCaja, EditarCaja, EliminarCaja

# Create your views here.

from django.db.models import Sum
from django.db.models import Q
from .models import Venta


class Index(TemplateView):
    template_name="ventas/index.html"

    def get_context_data(self, **kwargs):
        context= super(Index, self).get_context_data(**kwargs)
        fecha_hoy=timezone.now().strftime("%Y-%m-%d")
        print("hola.......")
        print(type(fecha_hoy))
        print(fecha_hoy)
        ventas_hoy=Venta.objects.filter(Q(fecha_venta__date=fecha_hoy))
        print(ventas_hoy)
        suma_ventas=ventas_hoy.aggregate(Sum('total_con_iva'))
        total=suma_ventas.get('total_con_iva__sum')
        total_ventas=0
        if total is not None:
            total_ventas=round(suma_ventas.get('total_con_iva__sum'), 2)
        
        context['total_con_iva']=total_ventas
        return context
