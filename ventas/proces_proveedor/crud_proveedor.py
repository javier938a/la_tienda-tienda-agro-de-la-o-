from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ventas.forms import ProveedorForm
from ventas.models import Proveedor

class CrearProveedor(CreateView):
    template_name="proces_proveedor/crear_proveedor.html"
    model=Proveedor
    form_class=ProveedorForm
    context_object_name='form'
    success_url=reverse_lazy('store:list_prove')


class EditarProveedor(UpdateView):
    template_name="proces_proveedor/editar_proveedor.html"
    model=Proveedor
    form_class=ProveedorForm
    context_object_name='form'
    success_url=reverse_lazy('store:list_prove')

class EliminarProveedor(DeleteView):
    template_name="proces_proveedor/eliminar_proveedor.html"
    model=Proveedor
    context_object_name='proveedor'
    success_url=reverse_lazy('store:list_prove')


class ListarProveedor(ListView):
    template_name="proces_proveedor/listar_proveedor.html"
    model=Proveedor
    context_object_name='proveedores'
