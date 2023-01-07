from django.views.generic import TemplateView, ListView
from ventas.models import AperturaCorte, Venta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse
from django.http import JsonResponse
import django.utils.timezone as timezone

class CrearApertura(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/crear_apertura_corte.html"
    def get_context_data(self, **kwargs):
        context=super(CrearApertura, self).get_context_data(**kwargs)
        #promero verificamos si hay una apertura anterior que haya quedado como ultima apertura
        #con estado de apertura=False y estado de ultima_apertura=True
        #si existe es porque ya se creo un corte con esa apertura
        if AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).filter(Q(ultima_apertura=True) & Q(estado_de_apertura=False) & Q(usuario__caja=self.request.user.caja)).exists():
            #luego verificamos si este corte no es el corte global o el ultimo corte hecho en el dia 
            #ya que de ser asi no se tomaria en cuenta para realizar esta apertura ya que corresponde 
            #a un nuevo inicio del dia y el dueño decidira con cuanto efectivo necesita iniciar el dia
            if AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).filter(Q(ultima_apertura=True) & Q(estado_de_apertura=False) & Q(corte_global=True) & Q(usuario__caja=self.request.user.caja)).exists():
                context['usuario_anterior']="ninguno"
                context['monto_corte_anterior']="0"
            else:#si no existe entonces agarramos esa ultima apertura y tomamos el valor
                #del monto de apertura anterior para indicar al usuario que eso debe de tener en caja
                corte_anterior=AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).get(Q(ultima_apertura=True) & Q(usuario__caja=self.request.user.caja))
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
        suma_venta_de_esta_apertura=ventas_de_esta_apertura.aggregate(Sum('total_sin_iva'))
        monto_de_apertura=apertura.monto_de_apertura
        suma_ventas_apertura=suma_venta_de_esta_apertura['total_sin_iva__sum']
        print("Suma")
        if suma_ventas_apertura == None:
            suma_ventas_apertura=0.0
        print(suma_ventas_apertura)
        print(type(suma_venta_de_esta_apertura))
        monto_en_caja=float(monto_de_apertura)+float(suma_ventas_apertura)
        print("Monto en caja: "+str(monto_en_caja))
        context['monto_de_apertura']=round(monto_de_apertura, 2)
        context['suma_ventas_apertura']= round(suma_ventas_apertura, 2)
        context['monto_en_caja']= round(monto_en_caja, 2)
        context['apertura']=apertura

        print("Monto de esta apertura: "+str(monto_de_apertura))
        print("Total de todas las ventas realizadas "+str(suma_venta_de_esta_apertura['total_sin_iva__sum']))
        return context

class ViewCierreDeCaja(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/crear_cierre_de_caja.html"
    def get_context_data(self, **kwargs):
        context=super(ViewCierreDeCaja, self).get_context_data(**kwargs)
        apertura=AperturaCorte.objects.get(id=self.kwargs['pk'])
        monto_de_cierre=apertura.monto_de_corte
        id_apertura=apertura.id
        context['id_apertura']=id_apertura
        context['monto_de_cierre']=monto_de_cierre
        return context 


def efectuar_cierre_de_caja(request):
    idapertura=request.POST.get('id_apertura')
    res=False
    AperturaCorte.objects.filter(id=idapertura).update(
        nombre_usuario_cierre=str(request.user),
        corte_global=True
    )  
    res=True
    data={
        'res':res
    }     

    return JsonResponse(
        data,
        safe=False
    )



def efectuar_corte_de_caja(request):
    id_apertura=request.POST.get('id_apertura')
    monto_de_corte=float(request.POST.get('monto_de_corte'))
    diferencia_de_corte=float(request.POST.get('diferencia_de_corte'))
    observacion=""
    fecha_y_hora_de_corte=timezone.now()
    res=False
    if diferencia_de_corte==0:
        observacion="La caja esta cuadrada diferencia es "+str(diferencia_de_corte)
    elif diferencia_de_corte>0:
        observacion="La caja no esta cuadrada hay un faltante de "+str(diferencia_de_corte)
    elif diferencia_de_corte<0:
        observacion="La caja no esta cuadrada hay un sobrante de "+str(diferencia_de_corte)
    
    AperturaCorte.objects.filter(id=id_apertura).update(
        monto_de_corte=monto_de_corte,
        fecha_de_corte=fecha_y_hora_de_corte,
        estado_de_apertura=False,
        diferencia_de_corte=diferencia_de_corte,
        nombre_usuario_corte=str(request.user),
        observacion=observacion
    )
    res=True
    print("Hola!!!")

    datos={
        'res':res,
    }
    print(datos)
    return JsonResponse(
        datos, safe=False
    )

def proces_efectuar_apertura_caja(request):
    monto_de_apertura=request.POST.get('monto_de_apertura')
    caja_del_usuario=request.user.caja
    diferencia_de_apertura=request.POST.get('diferencia_de_apertura')
    res=False
    datos={}
    ##poniendo en false la ultima apertura
    apertura_anterior=AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(Q(usuario__caja=caja_del_usuario) & Q(ultima_apertura=True))
    apertura_anterior.update(estado_de_apertura=False,ultima_apertura=False)
    #como el campo corte se mantiene en cero ya que como ese seria el monto de apertura mas la sumatoria de todas las ventas que el usuario realizo en todo su turno
    nueva_apertura=AperturaCorte.objects.get_or_create(
        sucursal=request.user.sucursal,
        usuario=request.user, 
        monto_de_apertura=monto_de_apertura,
        monto_de_corte=0.0,
        estado_de_apertura=True,
        ultima_apertura=True,
        corte_global=False,
        diferencia_de_apertura=diferencia_de_apertura,
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
    apertura_activa=AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(Q(usuario__caja=request.user.caja) & Q(estado_de_apertura=True))
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
    if AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(Q(usuario=request.user) & Q(estado_de_apertura=True)).exists():
        res=1
        apertura_vigente=AperturaCorte.objects.filter(Q(usuario=request.user) & Q(estado_de_apertura=True))
        apertura=apertura_vigente[0]
        nombre_usuario=str(apertura.usuario.username)
        print(apertura_vigente)
        #despues verificamos si existe un corte a nombre de esta caja y vemos a quien le corresponde
    elif AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(Q(usuario__caja=request.user.caja) & Q(estado_de_apertura=True)).exists():#de lo contrario verificamos si existe una apertura vigente a la caja a cargo de otro usuario
        res=2
        apertura_vigente=AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(Q(usuario__caja=request.user.caja) & Q(estado_de_apertura=True))
        apertura=apertura_vigente[0]
        nombre_usuario=str(apertura.usuario.username)
        print(apertura_vigente)
    else:
        res=3
    datos={}

    if res==1:
        datos['res']=res

    elif res==2:
        datos['res']=res
        datos['nombre_usuario']=nombre_usuario
    else:
        datos['res']=res
    return JsonResponse(
        datos, safe=False
    )

class ListarAperturaCorte(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_apertura_corte/listar_apertura_corte.html"
    context_object_name="apertura_caja"
    def get_context_data(self, **kwargs):
        context=super(ListarAperturaCorte, self).get_context_data(**kwargs)
        apertura_activa=None
        apertura_de_corte=None
        es_corte_de_caja=0#servira para saber si el ultimo corte de caja hecho en el dia
        if AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).filter(Q(estado_de_apertura=True) & Q(usuario=self.request.user) & Q(corte_global=False)).exists():
            es_corte_de_caja=1
            apertura_activa= AperturaCorte.objects.get(Q(sucursal=self.request.user.sucursal) & Q(estado_de_apertura=True) & Q(usuario__caja=self.request.user.caja) & Q(corte_global=False))
        elif AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).filter(Q(estado_de_apertura=True) & Q(usuario__caja=self.request.user.caja)).exists():
            es_corte_de_caja=1
            apertura_activa= AperturaCorte.objects.get(Q(sucursal=self.request.user.sucursal) & Q(estado_de_apertura=True) & Q(usuario__caja=self.request.user.caja))
        elif AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).filter(Q(estado_de_apertura=False) & Q(ultima_apertura=True) & Q(corte_global=False) & Q(usuario=self.request.user)).exists():
            es_corte_de_caja=2
            apertura_de_corte= AperturaCorte.objects.get(Q(sucursal=self.request.user.sucursal) & Q(estado_de_apertura=False) & Q(ultima_apertura=True) & Q(corte_global=False) & Q(usuario=self.request.user))
        elif AperturaCorte.objects.filter(sucursal=self.request.user.sucursal).filter(Q(estado_de_apertura=False) & Q(ultima_apertura=True) & Q(corte_global=False) & Q(usuario__caja=self.request.user.caja)).exists():
            es_corte_de_caja=2
            apertura_de_corte=AperturaCorte.objects.get(Q(sucursal=self.request.user.sucursal) & Q(estado_de_apertura=False) & Q(ultima_apertura=True) & Q(corte_global=False) & Q(usuario__caja=self.request.user.caja))
        else:
            es_corte_de_caja=3

        if es_corte_de_caja==1:
            context['es_corte_de_caja']=es_corte_de_caja
            context['apertura_activa']=apertura_activa
        elif es_corte_de_caja==2:
            context['es_corte_de_caja']=es_corte_de_caja
            context['apertura_de_corte']=apertura_de_corte
        elif es_corte_de_caja==3:
            context['es_corte_de_caja']=es_corte_de_caja
        return context


def obtener_lista_apertura_cortes_json(request):
    data=[]
    sucursal=request.user.sucursal
    aperturas_cortes=None#AperturaCorte.objects.filter(Q(usuario__sucursal=sucursal)).order_by('-fecha_de_apertura')
    draw=request.POST.get('draw')
    start=request.POST.get('start')
    length=request.POST.get('length')
    searchValue=request.POST.get('search[value]')
    condiciones_de_busqueda=None
    if searchValue!='':
        condiciones_de_busqueda=Q(fecha_de_apertura__icontains=searchValue) | Q(usuario__username__icontains=searchValue) | Q(sucursal__descripcion__icontains=searchValue) | Q(observacion__icontains=searchValue) | Q(nombre_usuario_corte__icontains=searchValue) | Q(nombre_usuario_cierre__icontains=searchValue) | Q(observacion__icontains=searchValue)
    totalRecords=AperturaCorte.objects.all().count()

    totalRecordWithFilter=0
    if condiciones_de_busqueda is not None:
        if int(start)>=int(length):
            aperturas_cortes=AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(condiciones_de_busqueda).order_by('-fecha_de_apertura')[int(start):int(length)+int(start)]
        else:
            aperturas_cortes=AperturaCorte.objects.filter(sucursal=request.user.sucursal).filter(condiciones_de_busqueda).order_by('-fecha_de_apertura')[int(start):int(length)]

        totalRecordWithFilter=aperturas_cortes.count()
    else:
        if int(start)>=int(length):
            aperturas_cortes=AperturaCorte.objects.all().order_by('-fecha_de_apertura')[int(start):int(length)+int(start)]
        else:
            aperturas_cortes=AperturaCorte.objects.all().order_by('-fecha_de_apertura')[int(start):int(length)]
        totalRecordWithFilter=aperturas_cortes.count()
    for apertura in aperturas_cortes:
        url_realizar_corte=reverse('store:realizar_corte', args=[apertura.id])
        url_cierre_caja=reverse('store:cierre_caja', args=[apertura.id])
        action="""
                <div class="btn-group">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                        <ul class="dropdown-menu">                                                        
                            
                        </ul>
                </div>
            """
        if apertura.estado_de_apertura==True and apertura.usuario.caja.numero_de_caja==request.user.caja.numero_de_caja:
            action="""
                    <div class="btn-group">
                            <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                                Action
                            </button>
                            <ul class="dropdown-menu">                                                        
                                <li><a class="dropdown-item" href="%s">Hacer corte</a></li>
                            </ul>
                    </div>
                    """%(url_realizar_corte)
        if apertura.estado_de_apertura==False and apertura.ultima_apertura==True:
            action="""
                    <div class="btn-group">
                            <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                                Action
                            </button>
                            <ul class="dropdown-menu">                                                        
                                <li><a class="dropdown-item" href="%s">Cierre de caja</a></li>
                            </ul>
                    </div>
                    """%(url_cierre_caja)

        campos={}
        campos['id']=str(apertura.id)
        campos['caja']=str(apertura.usuario.caja)
        campos['usuario']=str(apertura.usuario)
        campos['fecha_de_apertura']=str(timezone.localtime(apertura.fecha_de_apertura))
        campos['monto_de_apertura']=str(apertura.monto_de_apertura)
        if apertura.diferencia_de_apertura==None:
            campos['diferencia_de_apertura']='0'
        else:
            campos['diferencia_de_apertura']=apertura.diferencia_de_apertura
        
        if apertura.fecha_de_corte==None:
            campos['fecha_de_corte']='No hay Corte'
        else:
            campos['fecha_de_corte']=apertura.fecha_de_corte

        if apertura.monto_de_corte==None:
            campos['monto_de_corte']='0'
        else:
            campos['monto_de_corte']=apertura.monto_de_corte
        if apertura.diferencia_de_corte==None:
            campos['diferencia_de_corte']='0'
        else:
            campos['diferencia_de_corte']=apertura.monto_de_corte
        if apertura.nombre_usuario_corte==None:
            campos['nombre_usuario_de_corte']=''
        else:
            campos['nombre_usuario_de_corte']=apertura.nombre_usuario_corte
        if apertura.estado_de_apertura==True:
            campos['estado_apertura']='Activo'
        else:
            campos['estado_apertura']='Finalizado'
        if apertura.corte_global==True:
            campos['corte_global']="Es cierre de caja"
        else:
            campos['corte_global']="No es cierre de caja"
        if apertura.ultima_apertura==True:
            campos['ultima_apertura']="Si"
        else:
            campos['ultima_apertura']="No"
        
        campos['action']=action

        data.append(campos)
    return JsonResponse({
        'draw':int(draw),
        'iTotalRecords':totalRecordWithFilter,
        'iTotalDisplayRecords':totalRecords,
        'data':data
    }, safe=False)
