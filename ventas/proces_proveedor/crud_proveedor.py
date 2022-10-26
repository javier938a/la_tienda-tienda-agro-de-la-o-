from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ventas.forms import ProveedorForm
from ventas.models import Proveedor

class CrearProveedor(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"

    template_name="proces_proveedor/crear_proveedor.html"
    model=Proveedor
    form_class=ProveedorForm
    context_object_name='form'
    success_url=reverse_lazy('store:list_prove')


class EditarProveedor(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_proveedor/editar_proveedor.html"
    model=Proveedor
    form_class=ProveedorForm
    context_object_name='form'
    success_url=reverse_lazy('store:list_prove')

class EliminarProveedor(LoginRequiredMixin, DeleteView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_proveedor/eliminar_proveedor.html"
    model=Proveedor
    context_object_name='proveedor'
    success_url=reverse_lazy('store:list_prove')


class ListarProveedor(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_proveedor/listar_proveedor.html"
    model=Proveedor
    context_object_name='proveedores'
