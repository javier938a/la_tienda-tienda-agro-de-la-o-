from django.views.generic import TemplateView, ListView
from ventas.models import AperturaCorte, Venta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import JsonResponse

class CrearApertura(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/crear_apertura_corte.html"
    def get_context_data(self, **kwargs):
        context=super(CrearApertura, self).get_context_data(**kwargs)
        if AperturaCorte.objects.filter(Q(ultima_apertura=True) & Q(usuario__caja=self.request.user.caja)).exists():
            corte_anterior=AperturaCorte.objects.get(Q(ultima_apertura=True) & Q(usuario__caja=self.request.user.caja))
            usuario_anterior=corte_anterior.usuario
            monto_corte_anterior=corte_anterior.monto_de_corte
            print(monto_corte_anterior)
            context['usuario_anterior']=usuario_anterior
            context['monto_corte_anterior']=monto_corte_anterior
        else:
            context['usuario_anterior']="ninguno"
            context['monto_corte_anterior']="0"
        
        return context

class ViewRealizarCorteCaja(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/crear_corte_de_caja.html"
    def get_context_data(self, **kwargs):
        context=super(ViewRealizarCorteCaja, self).get_context_data(**kwargs)
        print("ID apertura: "+str(self.kwargs['pk']))
        apertura=AperturaCorte.objects.get(id=self.kwargs['pk'])
        ventas_de_esta_apertura=Venta.objects.filter(apertura_corte=apertura)
        suma_venta_de_esta_apertura=ventas_de_esta_apertura.aggregate(Sum('total_con_iva'))
        monto_de_apertura=apertura.monto_de_apertura
        suma_ventas_apertura=suma_venta_de_esta_apertura['total_con_iva__sum']
        print("Suma")
        print(type(suma_venta_de_esta_apertura))
        monto_en_caja=float(monto_de_apertura)+float(suma_ventas_apertura)
        print("Monto en caja: "+str(monto_en_caja))
        context['monto_de_apertura']=monto_de_apertura
        context['suma_ventas_apertura']=suma_ventas_apertura
        context['monto_en_caja']=monto_en_caja
        context['apertura']=apertura

        print("Monto de esta apertura: "+str(monto_de_apertura))
        print("Total de todas las ventas realizadas "+str(suma_venta_de_esta_apertura['total_con_iva__sum']))
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

#esta funcion servira para verificar si la apertura vigente pertenece al usuario logiado
#ya que si hay un usuario con una apertura vigente y entra otro usuario no podra vender
#aunque sea de la misma caja tendra que finalizar esa corte con esta apertura o el usuario
#que tiene la apertura vigente tiene que hacerla para que el nuevo usuario asignado a esta misma caja 
#pueda aperturar y seguir vendiendo
def verificar_apertura_activa_de_usuario(request):
    res=0
    nombre_usuario=""

    #si existe una apertura se obtiene el nombre del usuario que esta a cargo de la venta
    #para mostrarsela al usuario
    #primero verificamos si existe una apertura con este usuario logiado
    if AperturaCorte.objects.filter(Q(usuario=request.user) & Q(estado_de_apertura=True)).exists():
        res=1
        apertura_vigente=AperturaCorte.objects.filter(Q(usuario=request.user) & Q(estado_de_apertura=True))
        apertura=apertura_vigente[0]
        nombre_usuario=str(apertura.usuario.username)
        print(apertura_vigente)
        #despues verificamos si existe un corte a nombre de esta caja y vemos a quien le corresponde
    elif AperturaCorte.objects.filter(Q(usuario__caja=request.user.caja) & Q(estado_de_apertura=True)).exists():#de lo contrario verificamos si existe una apertura vigente a la caja a cargo de otro usuario
        res=2
        apertura_vigente=AperturaCorte.objects.filter(Q(usuario__caja=request.user.caja) & Q(estado_de_apertura=True))
        apertura=apertura_vigente[0]
        nombre_usuario=str(apertura.usuario.username)
        print(apertura_vigente)
    datos={}

    if res==1:
        datos['res']=res

    elif res==2:
        datos['res']=res
        datos['nombre_usuario']=nombre_usuario
    return JsonResponse(
        datos, safe=False
    )

 




class ListarAperturaCorte(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/listar_apertura_corte.html"
    model=AperturaCorte
    context_object_name="apertura_caja"