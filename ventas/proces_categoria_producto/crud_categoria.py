from ventas.models import Categoria
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from ventas.forms import CategoriaProductoForm
from ventas.models import Categoria

class CrearCategoriaProducto(CreateView):
    template_name="proces_categoria/crear_categoria_producto.html"
    model=Categoria
    form_class=CategoriaProductoForm
    context_object_name="form"
    success_url=reverse_lazy('store:list_cate')

class EditarCategoriaProducto(UpdateView):
    template_name="proces_categoria/editar_categoria_producto.html"
    model=Categoria
    form_class=CategoriaProductoForm
    context_object_name="form"
    success_url=reverse_lazy('store:list_cate')

class EliminarCategoriaProducto(DeleteView):
    template_name="proces_categoria/eliminar_categoria_producto.html"
    model=Categoria
    context_objec_name="cate"
    success_url=reverse_lazy('store:list_cate')

class ListarCategoriasProducto(ListView):
    model=Categoria
    template_name="proces_categoria/listar_categoria_producto.html"
    context_object_name="categorias"
