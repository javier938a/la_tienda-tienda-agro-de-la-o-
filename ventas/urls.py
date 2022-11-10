from unicodedata import name
from django.urls import path


from .views import Index
from .views import iniciar_session, cerrar_session
from .views import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario, DetalleUsuario
from .views import ListarTipoUsuario, CrearTipoUsuario, EditarTipoUsuario, EliminarTipoUsuario
from .views import ListarProveedor, CrearProveedor, EditarProveedor, EliminarProveedor
from .views import ListarSucursal, CrearSucursal, EditarSucursal, EliminarSucursal
from .views import ListarCategoriasProducto, CrearCategoriaProducto, EditarCategoriaProducto, EliminarCategoriaProducto
from .views import ListarProductos, CrearProducto, EditarProducto, EliminarProducto
from .views import ListarPresentacion, CrearPresentacion, EditarPresentacion, EliminarPresentacion
from .views import ListarCargaProductos, ViewCargaInventario, DetalleCargaInventario, listar_productos_cargados_y_sin_cargar_autocomplete, agregar_producto_detalle_carga, cargar_producto_inventario
from .views import ListarDescargasProductos, ViewCrearDescargaProducto, listar_productos_a_descargar_por_sucursal_autocomplete, agregar_producto_a_descargar_a_detalle, efectuar_descarga_de_productos
from .views import ListarInventario, ViewCrearInventario, ViewEditarInventario, EliminarInventario, obtener_productos_autocomplete, agregar_producto_detalle
from .views import guardar_datos_inventario, actualizar_datos_inventario, update_producto_detalle, DetalleInventario
from .views import ListarVentas, ViewCrearVenta, ViewDetalleVenta, verificar_stock_producto, obtener_productos_inventario_autocomplete, agregar_producto_detalle_venta, efectuar_venta
from .views import ListarDevolucionesVentas, ViewCrearDevolucionVenta, ViewDetalleDevolucion, obtener_ventas_autocomplete, listar_productos_de_venta, efectuar_devolucion_venta
from .views import ListarAperturaCorte, CrearApertura, ViewRealizarCorteCaja, proces_efectuar_apertura_caja, proces_verificar_si_hay_apertura_de_caja, verificar_apertura_activa_de_usuario
from .views import ListarCajas, CrearCaja, EditarCaja, EliminarCaja
from .views import agregar_producto_a_detalle_por_codigo
from .views import imprimir_ticket, Obtener_ticket
from .views import ViewSelectReporteVentas, PrintViewReporteVentas
from .views import grafico_reporte_ventas



app_name="store"
urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('login/', iniciar_session, name="login"),
    path('logout/', cerrar_session, name="logout"),
    path('tipo_usuario/', ListarTipoUsuario.as_view(), name="list_tipo_user"),
    path('tipo_usuario/crear_tipo_usuario', CrearTipoUsuario.as_view(), name="crear_tipo_user"),
    path('tipo_usuario/editar_tipo_usuario/<int:pk>', EditarTipoUsuario.as_view(), name="edit_tipo_user"),
    path('tipo_usuario/eliminar_tipo_usuario/<int:pk>', EliminarTipoUsuario.as_view(), name="del_tipo_user"),
    path('usuarios/', ListarUsuarios.as_view(), name="user"),
    path('detalle_usuario/<int:pk>', DetalleUsuario.as_view(), name="detalle_user"),
    path('usuarios/crear_usuarios', CrearUsuario.as_view(), name="crear_user"),
    path('usuarios/editar_usuario/<int:pk>', EditarUsuario.as_view(), name="editar_user"),
    path('usuarios/eliminar_usuario/<int:pk>', EliminarUsuario.as_view(), name="del_user"),
    path('proveedores/', ListarProveedor.as_view(), name="list_prove"),
    path('proveedores/crear_proveedor', CrearProveedor.as_view(), name="crear_prove"),
    path('proveedores/editar_proveedor/<int:pk>', EditarProveedor.as_view(), name="edit_prove"),
    path('proveedores/eliminar_proveedor/<int:pk>', EliminarProveedor.as_view(), name="del_prove"),
    path('sucursales/', ListarSucursal.as_view(), name="list_sucursal"),
    path('sucursales/crear_sucursal', CrearSucursal.as_view(), name="crear_sucursal"),
    path('sucursales/editar_sucursal/<int:pk>', EditarSucursal.as_view(), name="edit_sucursal"),
    path('sucursales/eliminar_sucursal/<int:pk>', EliminarSucursal.as_view(), name="del_sucursal"),
    path('categorias_producto/', ListarCategoriasProducto.as_view(), name="list_cate"),
    path('categorias_producto/crear_categoria_producto', CrearCategoriaProducto.as_view(), name="crear_cate"),
    path('categorias_producto/editar_categoria_producto/<int:pk>', EditarCategoriaProducto.as_view(), name="edit_cate"),
    path('categorias_producto/eliminar_categoria_producto/<int:pk>', EliminarCategoriaProducto.as_view(), name="del_cate"),
    path('productos/', ListarProductos.as_view(), name="list_prod"),
    path('productos/crear_producto', CrearProducto.as_view(), name="crear_prod"),
    path('productos/editar_producto/<int:pk>', EditarProducto.as_view(), name="editar_prod"),
    path('productos/eliminar_producto/<int:pk>', EliminarProducto.as_view(), name="del_prod"),
    path('presentaciones/', ListarPresentacion.as_view(), name="list_pre"),
    path('presentaciones/crear_presentacion', CrearPresentacion.as_view(), name="crear_pre"),
    path('presentaciones/editar_presentacion/<int:pk>', EditarPresentacion.as_view(), name="edit_pre"),
    path('presentacion/eliminar_presentacion/<int:pk>', EliminarPresentacion.as_view(), name="del_pre"),
    path('carga/listar_carga_inventario', ListarCargaProductos.as_view(), name="list_carga_prod"),
    path('carga/agregar_carga_inventario', ViewCargaInventario.as_view(), name="add_carga_prod"),
    path('carga/detalle_de_carga_inventario/<int:pk>', DetalleCargaInventario.as_view(), name="detalle_carga"),
    path('carga/listar_productos_cargados_y_sin_cargar', listar_productos_cargados_y_sin_cargar_autocomplete, name="list_prod_autocomplete"),
    path('carga/agregar_producto_detalle_carga', agregar_producto_detalle_carga, name="add_prod_detalle_carga" ),
    path('descarga_productos/', ListarDescargasProductos.as_view(), name="list_descarga_prod"),
    path('descarga_productos/crear_descarga_productos', ViewCrearDescargaProducto.as_view(), name="crear_descarga_prod"),
    path('list_descarga_productos_autocomplete', listar_productos_a_descargar_por_sucursal_autocomplete, name="list_prod_a_descargar"),
    path('descarga_producto/agregar_producto_a_descargar_a_detalle', agregar_producto_a_descargar_a_detalle, name='add_prod_a_descarga'),
    path('descarga_producto/efectuar_descarga', efectuar_descarga_de_productos, name='efectuar_descarga_prod'),
    path('carga/cargar_producto_inventario', cargar_producto_inventario, name='cargar_prod_inv'),
    path('inventario/', ListarInventario.as_view(), name="list_inv"),
    path('inventario/crear_inventario', ViewCrearInventario.as_view(), name="crear_inv"),
    path('inventario/editar_inventario/<int:pk>', ViewEditarInventario.as_view(), name="edit_inv"),
    path('inventario/detalle_inventario/<int:pk>', DetalleInventario.as_view(), name="det_inv"),
    path('inventario/eliminar_inventario/<int:pk>', EliminarInventario.as_view(), name="del_inv"),
    path('inventario/auto_prod_list', obtener_productos_autocomplete, name='auto_prod_list'),
    path('inventario/agregar_producto', agregar_producto_detalle, name="add_prod_detalle"),
    path('inventario/guardar_detalles_inventario', guardar_datos_inventario, name='guardar_dato_inventario'),
    path('inventario/actualizar_inventario', actualizar_datos_inventario, name='add_update_detalle_inv'),
    path('inventario/agregar_prod_update', update_producto_detalle, name="add_update_inv"),
    path('ventas/', ListarVentas.as_view(), name="list_venta"),
    path('ventas/crear_venta', ViewCrearVenta.as_view(), name="crear_venta"),
    path('ventas/detalle_de_venta/<int:pk>', ViewDetalleVenta.as_view(), name='detalle_venta'),
    path('ventas/agregar_producto_detalle_codigo', agregar_producto_a_detalle_por_codigo, name="add_prod_barra"),
    path('ventas/productos_autocomplete_inv', obtener_productos_inventario_autocomplete, name='prod_inv_autocomplete'),
    path('ventas/agregar_productos_detalle_venta', agregar_producto_detalle_venta, name='add_prod_venta'),
    path('ventas/efectuar_venta', efectuar_venta, name='efectuar_venta'),
    path('ventas/verificar_stock_producto', verificar_stock_producto, name="verificar_stock"),
    path('ventas/imprimir_ticket', imprimir_ticket, name="print_ticket"),
    path('ventas/obtener_ticket', Obtener_ticket, name='get_ticket'),
    path('devoluciones_ventas/', ListarDevolucionesVentas.as_view(), name="dev_ventas"),
    path('devolucion/crear_devolucion_venta', ViewCrearDevolucionVenta.as_view(), name="crear_dev"),
    path('devolucion/efectuar_devolucion_venta', efectuar_devolucion_venta, name='efect_dev'),
    path('devolucion/detalle_devolucion/<int:pk>', ViewDetalleDevolucion.as_view(), name='detalle_dev'),
    path('devoluciones/obtener_ventas_autocomplete', obtener_ventas_autocomplete, name="auto_ventas_list"),
    path('devoluciones/listar_productos_de_venta', listar_productos_de_venta, name="list_prod_de_venta"),
    path('cajas/', ListarCajas.as_view(), name="list_caja"),
    path('cajas/crear_caja', CrearCaja.as_view(), name="crear_caja"),
    path('cajas/editar_caja/<int:pk>', EditarCaja.as_view(), name="edit_caja"),
    path('cajas/eliminar_caja/<int:pk>', EliminarCaja.as_view(), name="del_caja"),
    path('apertura_corte/', ListarAperturaCorte.as_view(), name="list_apertura_corte"),
    path('apertura_corte/crear_apertura_corte', CrearApertura.as_view(), name="crear_apertura"),
    path('apertura_corte/efectuar_apertura', proces_efectuar_apertura_caja, name="efect_ape"),
    path('apertura_corte/verificar_apertura_caja', proces_verificar_si_hay_apertura_de_caja, name="verificar_apertura_activa"),
    path('apertura_corte/verificar_apertura_activa_de_usuario', verificar_apertura_activa_de_usuario, name="ver_ape_act_user"),
    path('apertura_corte/realizar_corte_de_caja/<int:pk>', ViewRealizarCorteCaja.as_view(), name="realizar_corte"),
    path('reporte/select_reporte_ventas', ViewSelectReporteVentas.as_view(), name="reporte_venta_view"),
    path('reporte/print_reporte_venta', PrintViewReporteVentas.as_view(), name="print_report_venta"),
    path('reporte/grafico_reporte', grafico_reporte_ventas, name="url_grafico"),
]