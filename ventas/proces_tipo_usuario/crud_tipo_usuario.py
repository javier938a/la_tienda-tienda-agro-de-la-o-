from pyexpat import model
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from ventas.models import TipoUsuario
from ventas.forms import TipoUsuarioForm
from django.urls import reverse_lazy


class CrearTipoUsuario(CreateView):
    template_name="proces_tipo_usuario/crear_tipo_usuario.html"
    form_class=TipoUsuarioForm
    model=TipoUsuario
    context_object_name="form"
    success_url=reverse_lazy('store:list_tipo_user')

class EditarTipoUsuario(UpdateView):
    template_name="proces_tipo_usuario/editar_tipo_usuario.html"
    form_class=TipoUsuarioForm
    model=TipoUsuario
    context_object_name="form"
    success_url=reverse_lazy('store:list_tipo_user')

class EliminarTipoUsuario(DeleteView):
    template_name="proces_tipo_usuario/eliminar_tipo_usuario.html"
    model=TipoUsuario
    context_object_name="tipo_usuario"
    success_url=reverse_lazy('store:list_tipo_user')

class ListarTipoUsuario(ListView):
    template_name="proces_tipo_usuario/listar_tipo_usuario.html"
    context_object_name="tipo_usuario"
    model=TipoUsuario


