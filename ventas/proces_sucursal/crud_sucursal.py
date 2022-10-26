from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from ventas.models import Sucursal
from ventas.forms import SucursalForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class CrearSucursal(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_sucursal/crear_sucursal.html"
    model=Sucursal
    form_class=SucursalForm
    success_url=reverse_lazy('store:list_sucursal')

class EditarSucursal(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_sucursal/editar_sucursal.html"
    model=Sucursal
    form_class=SucursalForm
    success_url=reverse_lazy('store:list_sucursal')

class EliminarSucursal(LoginRequiredMixin, DeleteView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_sucursal/eliminar_sucursal.html"
    model=Sucursal
    context_object_name='sucursal'
    success_url=reverse_lazy('store:list_sucursal')

class ListarSucursal(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_sucursal/listar_sucursal.html"
    model=Sucursal
    context_object_name="sucursal"

