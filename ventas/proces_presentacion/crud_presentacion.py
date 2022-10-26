from distutils.log import Log
from pyexpat import model
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ventas.models import Presentacion
from ventas.forms import PresentacionForm
from django.urls import reverse_lazy

class CrearPresentacion(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_presentacion/crear_presentacion.html"
    form_class=PresentacionForm
    model=Presentacion
    context_object_name="form"
    success_url=reverse_lazy('store:list_pre')

class EditarPresentacion(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_presentacion/editar_presentacion.html"
    form_class=PresentacionForm
    model=Presentacion
    context_object_name="form"
    success_url=reverse_lazy('store:list_pre')

class EliminarPresentacion(LoginRequiredMixin, DeleteView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_presentacion/eliminar_presentacion.html"
    model=Presentacion
    context_object_name="pre"
    success_url=reverse_lazy('store:list_pre')

class ListarPresentacion(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    model=Presentacion
    template_name="proces_presentacion/listar_presentacion.html"
    context_object_name="presentacion"
