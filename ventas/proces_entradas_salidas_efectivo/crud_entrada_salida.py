from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from ventas.models import EntradaSalidaEfectivo, User, Caja
from django.db.models import Q
from django.urls import reverse_lazy
from ventas.forms import EntradaSalidaEfectivoForm

class CrearEntradaSalida(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_entrada_salida_efectivo/agregar_entrada_salida_efectivo.html"
    model=EntradaSalidaEfectivo
    form_class=EntradaSalidaEfectivoForm
    context_object_name='form'
    success_url=reverse_lazy('store:entrada_salida')

    def get_context_data(self, **kwargs):
        context=super(CrearEntradaSalida, self).get_context_data(**kwargs)
        context.get('form').fields.get('usuario').empty_label=None
        context.get('form').fields.get('usuario').queryset=User.objects.filter(id=self.request.user.id)
        context.get('form').fields.get('caja').empty_label=None
        context.get('form').fields.get('caja').queryset=Caja.objects.filter(id=self.request.user.caja.id)
        return context

class EditarEntradaSalida(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name='proces_entrada_salida_efectivo/editar_entrada_salida_efectivo.html'
    model=EntradaSalidaEfectivo
    form_class=EntradaSalidaEfectivoForm
    context_object_name='form'
    success_url=reverse_lazy('store:entrada_salida')

    def get_context_data(self, **kwargs):
        context=super(EditarEntradaSalida, self).get_context_data(**kwargs)
        context.get('form').fields.get('usuario').empty_label=None
        context.get('form').fields.get('usuario').queryset=User.objects.filter(id=self.request.user.id)
        context.get('form').fields.get('caja').empty_label=None
        context.get('form').fields.get('caja').queryset=Caja.objects.filter(id=self.request.user.caja.id)
        return context

class EliminarEntradaSalida(LoginRequiredMixin, DeleteView):
    login_url='/ventas/login/'
    redirect_field_name='redirect_to'
    template_name='proces_entrada_salida_efectivo/eliminar_entrada_salida_efectivo.html'
    model=EntradaSalidaEfectivo
    context_object_name='entrada_salida_efectivo'
    success_url=reverse_lazy('store:entrada_salida')

class DetalleEntradaSalida(LoginRequiredMixin, DetailView):
    login_url='/ventas/login/'
    redirect_field_name='redirect_to'
    template_name='proces_entrada_salida_efectivo/detalle_entrada_salida_efectivo.html'
    model=EntradaSalidaEfectivo
    context_object_name='entrada_salida_efectivo'
      

class ListarEntradasSalidas(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_entrada_salida_efectivo/listar_entrada_salida_efectivo.html"
    model=EntradaSalidaEfectivo
    context_object_name="entradas_salidas"

    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha_hora')



