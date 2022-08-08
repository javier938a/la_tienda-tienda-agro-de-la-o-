from django.contrib import admin
from .models import TipoUsuario, User, Sucursal, Categoria, Presentacion, Producto, ProductoStockSucursal, ProductoStockGlobal
from .models import Venta, DetalleVenta, DetalleVentaServicio, InventarioProductos, CargaProductos, DetalleCargaProductos
from .models import DescargaProductos, DetalleDescargaProducto
from .models import DevolucionVenta, DetalleDevolucionVenta
# Register your models here.

admin.site.register(User)
admin.site.register(TipoUsuario)
admin.site.register(Sucursal)
admin.site.register(Categoria)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(ProductoStockSucursal)
admin.site.register(DetalleVenta)
admin.site.register(Venta)
admin.site.register(ProductoStockGlobal)
admin.site.register(InventarioProductos)
admin.site.register(CargaProductos)
admin.site.register(DetalleCargaProductos)
admin.site.register(DescargaProductos)
admin.site.register(DetalleDescargaProducto)
admin.site.register(DevolucionVenta)
admin.site.register(DetalleVentaServicio)
admin.site.register(DetalleDevolucionVenta)