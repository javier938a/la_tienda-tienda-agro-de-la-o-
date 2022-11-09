from django.views.generic import TemplateView, ListView
from ventas.models import AperturaCorte
from django.contrib.auth.mixins import LoginRequiredMixin

class CrearApertura(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/crear_apertura_corte.html"
    def get_context_data(self, **kwargs):
        corte_anterior=AperturaCorte.objects.latest('fecha_de_corte')
        usuario_anterior=corte_anterior.usuario
        monto_corte_anterior=corte_anterior.monto_de_corte
        print(monto_corte_anterior)
        
        context=super(CrearApertura, self).get_context_data(**kwargs)

        context['usuario_anterior']=usuario_anterior
        context['monto_corte_anterior']=monto_corte_anterior
        
        return context

def proces_efectuar_apertura_caja(request):
    pass

class ListarAperturaCorte(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/listar_apertura_corte.html"
    model=AperturaCorte
    context_object_name="apertura_caja"