from cProfile import label
from dataclasses import field, fields
from pyexpat import model
from django import forms
from django.contrib.admin import widgets as wd
from django.contrib.auth.forms import UserCreationForm
from .models import User, Sucursal, Categoria, Producto, Presentacion, Proveedor, TipoUsuario
from .models import AperturaCorte, Caja
from .models import EntradaSalidaEfectivo

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model=TipoUsuario
        fields=('tipo_usuario',)
        labels={
            'tipo_usuario':'Tipo de usuario',
        }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name','sucursal','caja', 'tipo_usuario','fecha_nacimiento', 'telefono', 'dui', 'nit')
        labels={
            'username':'Nombre de Usuario',
            'email':'Correo',
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'sucursal':'Sucursal',
            'caja':'No de Caja',
            'tipo_usuario':'Tipo de Usuario',
            'fecha_nacimiento':'Fecha de Nacimiento',
            'telefono':'telefono',
            'dui':'DUI',
            'nit':'NIT'
        }

class SucursalForm(forms.ModelForm):
    class Meta:
        model=Sucursal
        fields=('logo', 'descripcion', 'direccion', 'telefono')
        labels={
            'logo':'Logo de la Empresa',
            'descripcion':'Descripcion',
            'direccion':'Direccion',
            'telefono':'Telefono'
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model=Proveedor
        fields=('nombre', 'empresa', 'direccion', 'celular', 'telefono')
        labels={
            'nombre':'Nombre proveedor',
            'empresa':'Empresa',
            'celular':'N° de Celular',
            'telefono':'Telefono'
        }

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields=('categoria',)
        labels={
            'categoria':'Categoria'
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=("proveedor","nombre_producto", "descripcion","fecha_vencimiento", 'usuario', 'categoria',"codigo_barra")
        labels={
            'proveedor':'proveedor',
            'codigo_barra':'Codigo de barra del producto',            
            'categoria':'Categoria del producto',
            'descripcion':'Descripcion del producto',
            'fecha_vencimiento':"Fecha de vencimiento",
            'usuario':'Usuario',
            'nombre_producto':'Nombre del producto',
           
        }

class EntradaSalidaEfectivoForm(forms.ModelForm):
    class Meta:
        model=EntradaSalidaEfectivo
        fields=('usuario','caja','descripcion', 'tipo_entrada_salida', 'monto')
        labels={
            'usuario':'Usuario',
            'caja':'Caja',
            'descripcion':'Descripcion del movimiento de caja',
            'tipo_entrada_salida':'Tipo de flujo',
            'monto':'Monto'
        }
    
class PresentacionForm(forms.ModelForm):
    class Meta:
        model=Presentacion
        fields=('presentacion',)
        labels={
            'presentacion':'Presentacion'
        }

class CajaForm(forms.ModelForm):
    class Meta:
        model=Caja
        fields=('numero_de_caja',)
        labels={
            'numero_de_caja':'Numero de caja'
        }
