from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class UserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class Sucursal(models.Model):
    logo=models.ImageField(verbose_name="logo", upload_to="logo_sucursal", null=True, blank=True)
    descripcion=models.CharField(max_length=50, help_text="Ingrese una descripcion de la sucursal")
    direccion=models.TextField(help_text="Ingrese la direccion de la tienda")
    telefono=models.CharField(max_length=50, help_text="Ingrese el telefono de la ubicacion")

    def __str__(self) -> str:
        return self.descripcion
class TipoUsuario(models.Model):
    tipo_usuario=models.CharField(max_length=50, help_text="Ingrese el tipo de Usuario")

    def __str__(self):
        return self.tipo_usuario
class Caja(models.Model):
    numero_de_caja=models.CharField(help_text="Ingrese el numero",max_length=100)

    def __str__(self):
        return "%s"%self.numero_de_caja

class User(AbstractUser):
    objects=UserManager()
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    tipo_usuario=models.ForeignKey(TipoUsuario, help_text="Ingrese el tipo de Usuario", on_delete=models.SET_NULL, null=True)
    caja=models.ForeignKey(Caja, on_delete=models.SET_NULL, null=True)
    fecha_nacimiento=models.DateField(null=True, blank=True, help_text="Ingrese la fecha de nacimiento")
    telefono=models.CharField(max_length=11, help_text="Ingrese su numero de telefono", null=True, blank=True)
    dui=models.CharField(max_length=10, help_text="Ingrese el numero de dui", null=True, blank=True)
    nit=models.CharField(max_length=19, help_text="Ingrese el numero de dui", null=True, blank=True)

    class Meta:
        db_table="auth_user"
    
    def natural_key(self):
        return (self.username)

class Proveedor(models.Model):
    nombre=models.CharField(help_text="Ingrese el nombre del proveedor", max_length=100, null=True)
    empresa=models.CharField(help_text="Ingrese el nombre de la empresa", max_length=100, null=True)
    direccion=models.TextField(help_text="Ingrese la direccion del proveedor", null=True)
    celular=models.CharField(help_text="Ingrese el Celular del proveedor", max_length=11, null=True)
    telefono=models.CharField(help_text="Ingrese el telefono del proveedor", max_length=11, null=True)

    def __str__(self):
        return "%s %s"%(self.nombre, self.empresa)
    

class Categoria(models.Model):
    categoria=models.CharField(max_length=50, help_text="Ingrese la categoria del producto", null=True)

    def __str__(self) -> str:
        return "%s"%str(self.categoria) 

class Producto(models.Model):
    proveedor=models.ForeignKey(Proveedor, help_text="Seleccione el proveedor", on_delete=models.SET_NULL, null=True)
    codigo_producto=models.CharField(max_length=500, help_text="Codigo del producto", null=True)
    codigo_barra=models.CharField(max_length=100, help_text="Ingrese el codigo de barra del producto", null=True)
    nombre_producto=models.CharField(max_length=100, help_text="Ingrese el nombre del producto")
    descripcion=models.CharField(max_length=100, help_text="Ingrese la descripcion del producto")
    fecha_vencimiento=models.DateField(help_text="Ingrese la fecha de vencimiento", null=True, blank=True)
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria=models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return "%s"%self.nombre_producto


class Correlativos(models.Model):
    nombre_documento=models.CharField(max_length=100, help_text="Ingrese el nombre del documento")
    numero_correlativo_actual=models.CharField(max_length=100,help_text="Ingrese el numero de correlativo actual")

    def __str__(self):
        return "%s --> %s"%(self.nombre_documento, self.numero_correlativo_actual)


class Presentacion(models.Model):
    presentacion=models.CharField(max_length=50, help_text="Ingrese la presentacion")

    def __str__(self) -> str:
        return "%s"%self.presentacion
class DescargaProductos(models.Model):
    fecha_descarga=models.DateTimeField(auto_now_add=True)
    descripcion=models.CharField(max_length=100, help_text="Ingrese la descripcion del evento de descarga")
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null="Usuario que hace ka descarga")
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, help_text="Sucursal de donde se hace la descarga")
    total=models.FloatField(null=True, help_text="")

class DetalleDescargaProducto(models.Model):
    descarga_productos=models.ForeignKey(DescargaProductos, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    presentacion=models.ForeignKey(Presentacion, on_delete=models.SET_NULL, null=True)
    cantidad_anterior=models.IntegerField(help_text="Ingrese la cantidad anterior del producto", null=True)
    cantidad_descargada=models.IntegerField(help_text="Ingrese la cantidad del producto", null=True)
    nueva_cantidad=models.IntegerField(help_text="Ingrese la nueva cantidad", null=True)
    costo=models.FloatField(help_text="Ingrese el costo del producto", null=True)
    precio=models.FloatField(help_text="Ingrese el precio a como se va dar el producto en la venta", null=True)
    total=models.FloatField(help_text="", null=True)

    def __str__(self):
        return "%s -> %s"%(self.descarga_productos, self.producto)

class CargaProductos(models.Model):
    fecha_carga=models.DateTimeField(auto_now_add=True)
    descripcion=models.CharField(max_length=200, help_text="Descripcion de la carga de producto")
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Ingrese el usuario que realiza la carga")
    sucursal=models.ForeignKey(Sucursal, help_text="Sucursal donde se realiza la carga", on_delete=models.SET_NULL, null=True)
    total=models.FloatField(null=True, help_text="")

    def __str__(self):
        return self.descripcion

class DetalleCargaProductos(models.Model):
    carga_producto=models.ForeignKey(CargaProductos, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto,help_text="Ingrese el nombre del producto", on_delete=models.SET_NULL, null=True)
    presentacion=models.ForeignKey(Presentacion, on_delete=models.SET_NULL, null=True)
    cantidad_anterior=models.IntegerField(help_text="Ingrese la cantidad anterior del producto", null=True)
    cantidad=models.IntegerField(help_text="Ingrese la cantidad del producto", null=True)
    nueva_cantidad=models.IntegerField(help_text="Ingrese la nueva cantidad", null=True)
    costo_anterior=models.FloatField(help_text="Ingrese el costo anterior", null=True)
    costo=models.FloatField(help_text="Ingrese el costo del producto", null=True)
    precio_anterior=models.FloatField(help_text="Ingrese el precio anterior", null=True)
    precio=models.FloatField(help_text="Ingrese el precio a como se va dar el producto en la venta", null=True)
    total=models.FloatField(help_text="", null=True)
    tipo_prod=models.CharField(max_length=100, help_text="Ingrese el tipo de producto", null=True)

    def __str__(self):
        return "%s %s"%(str(self.carga_producto), str(self.producto))

class InventarioProductos(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    descripcion=models.CharField(max_length=100, help_text="Descripcion de la carga de inventario")
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    fecha_carga=models.DateTimeField(auto_now_add=True, help_text="fecha de creacion")
    total=models.FloatField(help_text="Ingrese el total de el inventario", null=True)

    def __str__(self) -> str:
        return "%s %s "%(self.descripcion, str(self.total))

class ProductoStockSucursal(models.Model):
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    presentacion=models.ForeignKey(Presentacion, on_delete=models.SET_NULL, null=True)
    cantidad=models.IntegerField(help_text="Ingrese la cantidad de producto")
    costo=models.FloatField(help_text="Ingrese el costo de compra del producto ",  null=True)
    precio=models.FloatField(help_text="Ingrese el precio de venta del producto",  null=True)


    def __str__(self) -> str:
        return "%s -> %s"%(str(self.sucursal), self.producto)

class AperturaCorte(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_de_apertura=models.DateTimeField(help_text="fecha y hora de apertura se generara automaticamente porque se registra el mismo momento que se habre apertura" ,auto_now=True)
    monto_de_apertura=models.FloatField(help_text="Ingrese el monto de apertura de su turno")
    monto_de_corte=models.FloatField(help_text="Ingrese el monto de corte de su turno", null=True,blank=True)
    fecha_de_corte=models.DateTimeField(help_text="Ingrese la fecha que se realizara el corte", null=True,blank=True)
    estado_de_apertura=models.BooleanField(help_text="Estado de la apertura, servira para saber si hay una apertura activa para empezar a vender")
    ultima_apertura=models.BooleanField(help_text="Este estado servira para saber si es la ultima apertura", null=True)
    diferencia_de_apertura=models.FloatField(help_text="servira para registrar la diferencia de apertura por si hay meno o mas dinero", blank=True, null=True)
    diferencia_de_corte=models.FloatField(help_text="Sirve para agregar alguna diferencia que haya en este el corte", blank=True, null=True)
    observacion=models.TextField(help_text="Servira para agregarle una observaciones en las aperturas", blank=True, null=True)
    def __str__(self):
        return  "Apertura del Usuario %s estado %s "%(self.usuario, str(self.estado_de_apertura))


class Venta(models.Model):
    fecha_venta=models.DateTimeField(help_text="Ingrese la fecha de la venta", auto_now=True)
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    apertura_corte=models.ForeignKey(AperturaCorte, on_delete=models.SET_NULL, null=True)
    numero_factura=models.CharField(help_text="Ingrese el numero de factura", max_length=50, null=True)
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    total_iva=models.FloatField(help_text="Total resultante de multiplicar el total por el procentaje de iva", null=True)
    total_sin_iva=models.FloatField(help_text="Total de la suma de todos los productos sin iva", null=True)
    total_con_iva=models.FloatField(help_text="Total de la suma de todos los productos mas el total del iva", null=True)
    
    def __str__(self):
        return "Factura N# %s | Total: %s"%(self.numero_factura, self.total_con_iva)


class DetalleVentaServicio(models.Model):
    factura=models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True)
    descripcion_servicio=models.TextField(help_text="ingrese la descripcion del servicio", null=True)#almacenara la descripcion del servicio
    precio=models.FloatField(help_text="Ingrese el precio del servicio")#almacenara el costo total del servicio

    def __str__(self):
        return "Servicio: %s | Precio: %s "%(self.descripcion_servicio, self.precio)

class DetalleVenta(models.Model):
    factura=models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True)
    producto_stock=models.ForeignKey(ProductoStockSucursal, on_delete=models.SET_NULL, null=True)
    cantidad=models.IntegerField(help_text="Ingrese la cantidad a comprar")
    precio=models.FloatField(help_text="Ingrese el precio del producto", null=True)
    total=models.FloatField(help_text="", null=True)

    def __str__(self) -> str:
        return "Producto: %s | Cantidad: %s | Precio: %s | total: %s"%(self.producto_stock, self.cantidad, self.precio, self.total)

class DevolucionVenta(models.Model):
    factura=models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True)
    descripcion=models.TextField(help_text="ingrese la descripcion de la devolucion")
    sucursal=models.ForeignKey(Sucursal, help_text="Ingrese la sucursal en donde se realiza la devolucion", on_delete=models.SET_NULL, null=True)
    fecha_devolucion=models.DateField(help_text="Ingrese la fecha de devolucion", blank=True, null=True, auto_now=True)
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_devolucion=models.FloatField(help_text="Ingrese el total de la devolucion", null=True)
    def __str__(self):
        return "%s "%(self.descripcion)

class DetalleDevolucionVenta(models.Model):
    devolucion_venta=models.ForeignKey(DevolucionVenta, on_delete=models.SET_NULL, null=True)
    producto_stock_suc=models.ForeignKey(ProductoStockSucursal, on_delete=models.SET_NULL, null=True)
    cantidad_devolver=models.IntegerField(help_text="Ingrese la cantidad a devolver", null=True)
    precio=models.FloatField(help_text="Ingrese el precio del producto", blank=True, null=True)
    total=models.FloatField(help_text="Ingrese el total de la devolucion", blank=True,null=True)

    def __str__(self):
        return "%s->%s->%s"%(str(self.devolucion_venta), str(self.producto_stock_suc), str(self.cantidad_devolver))


class ProductoStockGlobal(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    presentacion=models.ForeignKey(Presentacion, on_delete=models.SET_NULL, null=True)
    cantidad=models.IntegerField(help_text="Ingrese la cantidad del producto global")
    precio=models.DecimalField(help_text="Ingrese el precio del producto", decimal_places=2, max_digits=10)
    total=models.DecimalField(help_text="", decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return "%s -> %s"%(self.producto, str(self.cantidad))
