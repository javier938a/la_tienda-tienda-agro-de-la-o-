from django.urls import reverse_lazy
from ventas.models import Producto, User
from ventas.forms import ProductoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

class CrearProducto(CreateView):
    template_name="proces_producto/crear_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context=super(CrearProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None #Eliminando el '------'
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)#filtrando que solo se muestre el usuario logiado
        return context

class EditarProducto(UpdateView):
    template_name="proces_producto/editar_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context=super(EditarProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)
        return context

class EliminarProducto(DeleteView):
    template_name="proces_producto/eliminar_producto.html"
    model=Producto
    context_object_name="prod"
    success_url=reverse_lazy("store:list_prod")

class ListarProductos(ListView):
    template_name="proces_producto/listar_producto.html"
    model=Producto
    context_object_name="producto"

    