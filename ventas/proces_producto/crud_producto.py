from django.urls import reverse_lazy
from ventas.models import Producto, User, DetalleCargaProductos
from ventas.forms import ProductoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse

class CrearProducto(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"

    template_name="proces_producto/crear_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

    def get_context_data(self, **kwargs):
        context=super(CrearProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None #Eliminando el '------'
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)#filtrando que solo se muestre el usuario logiado
        return context

class DetalleProducto(LoginRequiredMixin, DetailView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/detalle_producto.html"
    model=Producto
    context_object_name="producto"

class EditarProducto(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/editar_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

    def get_context_data(self, **kwargs):
        context=super(EditarProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)
        return context

class EliminarProducto(LoginRequiredMixin, DeleteView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/eliminar_producto.html"
    model=Producto
    context_object_name="prod"
    success_url=reverse_lazy("store:list_prod")
    res=False
    def get_context_data(self, **kwargs):
        context=super(EliminarProducto, self).get_context_data(**kwargs)
        producto=Producto.objects.get(id=self.kwargs['pk'])
        if DetalleCargaProductos.objects.filter(producto=producto).exists():
            self.res=True
        context['res']=self.res
        return context
    

class ListarProductos(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/listar_producto.html"
    model=Producto
    context_object_name="producto"

    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha_de_registro')

def verificar_producto_si_esta_cargado(request):
    id_producto=request.POST.get('id_producto')
    producto=Producto.objects.get(id=id_producto)
    res=False
    if DetalleCargaProductos.objects.filter(producto=producto).exists():
        res=True
    datos={
        'res':res,
    }
    return JsonResponse(
        datos, safe=False
    )
    