from typing import List
from django.views.generic import TemplateView, ListView
from ventas.models import DevolucionVenta, Sucursal
class ListarDevolucionesVentas(ListView):
    template_name="proces_devolucion_venta/listar_devoluciones_ventas.html"
    model=DevolucionVenta
    context_object_name="devolucionVenta"


class ViewCrearDevolucionVenta(TemplateView):
    template_name="proces_devolucion_venta/crear_devolucion_venta.html"

    def get_context_data(self, **kwargs):
        context=super(ViewCrearDevolucionVenta, self).get_context_data(**kwargs)
        context['suc']=Sucursal.objects.all()
        return context
