from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ventas.models import Caja
from ventas.forms import CajaForm


class ListarCajas(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    model=Caja
    template_name="proces_caja/listar_caja.html"
    context_object_name="cajas"


class CrearCaja(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_caja/crear_caja.html"
    model=Caja
    form_class=CajaForm
    context_object_name='form'
    success_url=reverse_lazy('store:list_caja')

class EditarCaja(LoginRequiredMixin, UpdateView):
    login_url='/ventas/login/'
    redirect_field_name="redirect_to"
    template_name="proces_caja/editar_caja.html"
    model=Caja
    form_class=CajaForm
    context_object_name='form'
    success_url=reverse_lazy('store:list_caja')

class EliminarCaja(LoginRequiredMixin, DeleteView):
    login_url='/ventas/login/'
    redirect_field_name='redirect_to'
    template_name='proces_caja/eliminar_caja.html'
    model=Caja
    context_object_name='caja'
    success_url=reverse_lazy('store:list_caja')