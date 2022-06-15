from pyexpat import model
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from ventas.models import Presentacion
from ventas.forms import PresentacionForm
from django.urls import reverse_lazy

class CrearPresentacion(CreateView):
    template_name="proces_presentacion/crear_presentacion.html"
    form_class=PresentacionForm
    model=Presentacion
    context_object_name="form"
    success_url=reverse_lazy('store:list_pre')

class EditarPresentacion(UpdateView):
    template_name="proces_presentacion/editar_presentacion.html"
    form_class=PresentacionForm
    model=Presentacion
    context_object_name="form"
    success_url=reverse_lazy('store:list_pre')

class EliminarPresentacion(DeleteView):
    template_name="proces_presentacion/eliminar_presentacion.html"
    model=Presentacion
    context_object_name="pre"
    success_url=reverse_lazy('store:list_pre')

class ListarPresentacion(ListView):
    model=Presentacion
    template_name="proces_presentacion/listar_presentacion.html"
    context_object_name="presentacion"
