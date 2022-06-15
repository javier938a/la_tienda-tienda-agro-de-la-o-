from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from ventas.models import Sucursal
from ventas.forms import SucursalForm
from django.urls import reverse_lazy

class CrearSucursal(CreateView):
    template_name="proces_sucursal/crear_sucursal.html"
    model=Sucursal
    form_class=SucursalForm
    success_url=reverse_lazy('store:list_sucursal')

class EditarSucursal(UpdateView):
    template_name="proces_sucursal/editar_sucursal.html"
    model=Sucursal
    form_class=SucursalForm
    success_url=reverse_lazy('store:list_sucursal')

class EliminarSucursal(DeleteView):
    template_name="proces_sucursal/eliminar_sucursal.html"
    model=Sucursal
    context_object_name='sucursal'
    success_url=reverse_lazy('store:list_sucursal')

class ListarSucursal(ListView):
    template_name="proces_sucursal/listar_sucursal.html"
    model=Sucursal
    context_object_name="sucursal"

