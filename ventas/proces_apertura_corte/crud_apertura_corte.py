from django.views.generic import TemplateView, ListView
from ventas.models import AperturaCorte
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse

class CrearApertura(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/crear_apertura_corte.html"
    def get_context_data(self, **kwargs):
        context=super(CrearApertura, self).get_context_data(**kwargs)
        if AperturaCorte.objects.filter(Q(ultima_apertura=True) & Q(usuario=self.request.user)).exists():
            corte_anterior=AperturaCorte.objects.get(Q(ultima_apertura=True) & Q(usuario=self.request.user))
            usuario_anterior=corte_anterior.usuario
            monto_corte_anterior=corte_anterior.monto_de_corte
            print(monto_corte_anterior)
            context['usuario_anterior']=usuario_anterior
            context['monto_corte_anterior']=monto_corte_anterior
        else:
            context['usuario_anterior']="ninguno"
            context['monto_corte_anterior']="0"
        
        return context

def proces_efectuar_apertura_caja(request):
    monto_de_apertura=request.POST.get('monto_de_apertura')
    caja_del_usuario=request.user.caja
    res=False
    datos={}
    ##poniendo en false la ultima apertura
    apertura_anterior=AperturaCorte.objects.filter(Q(usuario__caja=caja_del_usuario) & Q(ultima_apertura=True))
    apertura_anterior.update(estado_de_apertura=False,ultima_apertura=False)
    #como el campo corte se mantiene en cero ya que como ese seria el monto de apertura mas la sumatoria de todas las ventas que el usuario realizo en todo su turno
    nueva_apertura=AperturaCorte.objects.get_or_create(
        usuario=request.user, 
        monto_de_apertura=monto_de_apertura,
        monto_de_corte=0.0,
        estado_de_apertura=True,
        ultima_apertura=True
    )
    new_apertura=nueva_apertura[0]
    res_apertura=nueva_apertura[1]
    if res_apertura==True:
        res=True
        datos['res']=res
        datos['id_apertura']=new_apertura.id
    else:
        res=False
        datos['res']=res
    return JsonResponse(
        datos, safe=False
    )

def proces_verificar_si_hay_apertura_de_caja(request):
    #verifica si hay una apertura referente a la caja asignada al usuario
    apertura_activa=AperturaCorte.objects.filter(Q(usuario__caja=request.user.caja) & Q(estado_de_apertura=True))
    res=False
    print(apertura_activa)
    datos={}
    #si la hay entonces res cambia true
    if apertura_activa.exists():
        res=True
        datos['res']=res
    #de lo contrario res cambia a false
    else:
        datos['res']=res
    return JsonResponse(
        datos, safe=False
    )

    




class ListarAperturaCorte(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/listar_apertura_corte.html"
    model=AperturaCorte
    context_object_name="apertura_caja"