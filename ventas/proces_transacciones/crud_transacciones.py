from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from ventas.models import Transaccion, Denominaciones, TipoTransaccion
from django.http import JsonResponse

class ViewCrearTransaccion(LoginRequiredMixin, TemplateView):
    template_name="proces_transacciones/crear_transaccion.html"
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"

    def get_context_data(self, **kwargs):
        context=super(ViewCrearTransaccion, self).get_context_data(**kwargs)
 
        
        tipo_transacciones=TipoTransaccion.objects.all()
        deno_1=Denominaciones.objects.get(Q(denominacion='$1') & Q(tipo_denominacion__tipo_denominacion="Billete"))
        deno_2=Denominaciones.objects.get(Q(denominacion='$2') & Q(tipo_denominacion__tipo_denominacion="Billete"))
        deno_5=Denominaciones.objects.get(Q(denominacion='$5') & Q(tipo_denominacion__tipo_denominacion="Billete"))
        deno_10=Denominaciones.objects.get(Q(denominacion='$10') & Q(tipo_denominacion__tipo_denominacion="Billete"))
        deno_20=Denominaciones.objects.get(Q(denominacion='$20') & Q(tipo_denominacion__tipo_denominacion="Billete"))
        deno_50=Denominaciones.objects.get(Q(denominacion='$50') & Q(tipo_denominacion__tipo_denominacion="Billete"))
        deno_100=Denominaciones.objects.get(Q(denominacion='$100') & Q(tipo_denominacion__tipo_denominacion="Billete"))

        deno_1_moneda=Denominaciones.objects.get(Q(denominacion='$1') & Q(tipo_denominacion__tipo_denominacion="Moneda"))
        deno_01_moneda=Denominaciones.objects.get(Q(denominacion='$0.01') & Q(tipo_denominacion__tipo_denominacion="Moneda"))
        deno_05_moneda=Denominaciones.objects.get(Q(denominacion='$0.05') & Q(tipo_denominacion__tipo_denominacion="Moneda"))
        deno_010_moneda=Denominaciones.objects.get(Q(denominacion='$0.10') & Q(tipo_denominacion__tipo_denominacion="Moneda"))
        deno_025_moneda=Denominaciones.objects.get(Q(denominacion='$0.25') & Q(tipo_denominacion__tipo_denominacion="Moneda"))
        deno_050_moneda=Denominaciones.objects.get(Q(denominacion='$0.50') & Q(tipo_denominacion__tipo_denominacion="Moneda"))
        
        context['deno_1']=deno_1
        context["deno_2"]=deno_2
        context["deno_5"]=deno_5
        context["deno_10"]=deno_10
        context["deno_20"]=deno_20
        context["deno_50"]=deno_50
        context["deno_100"]=deno_100

        context["deno_1_moneda"]=deno_1_moneda
        context["deno_01_moneda"]=deno_01_moneda
        context["deno_05_moneda"]=deno_05_moneda
        context["deno_010_moneda"]=deno_010_moneda
        context["deno_025_moneda"]=deno_025_moneda
        context["deno_050_moneda"]=deno_050_moneda
        context["tipo_transacciones"]=tipo_transacciones
        return context


class ListarTransacciones(LoginRequiredMixin, ListView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_transacciones/listar_transacciones.html"
    context_object_name="transacciones"
    model=Transaccion


def obtener_listas_transacciones_json(request):
    data=[]
    transacciones=None
    draw=request.POST.get('draw')
    start=request.POST.get('start')
    length=request.POST.get('length')
    searchValue=request.POST.get('search[value]')
    sucursal_usuario=request.user.sucursal
    tipo_usuario=str(request.user.tipo_usuario)
    condiciones_de_busqueda=None
    totalRecords=0
    totalRecordWithFilter=0
    if searchValue!='':
        condiciones_de_busqueda=Q(fecha_transaccion__date__icontains=searchValue) | Q(usuario__username__icontains=searchValue) | Q(nombre_cliente__icontains=searchValue) | Q(apellido_cliente__icontains=searchValue)
    if tipo_usuario=="administrador":
        totalRecords=Transaccion.objects.all().count()
    else:
        totalRecords=Transaccion.objects.filter(Q(sucursal=sucursal_usuario)).count()

    if condiciones_de_busqueda is not None:
        if int(start)>=int(length):
            if tipo_usuario=="administrador":
                transacciones=Transaccion.objects.filter(condiciones_de_busqueda).order_by("-fecha_transaccion")[int(start):int(length)+int(start)]
            else:
                transacciones=Transaccion.objects.filter(Q(sucursal=sucursal_usuario)).filter(condiciones_de_busqueda).order_by("-fecha_transaccion")[int(start):int(length)+int(start)]
        else:
            if tipo_usuario=="administrador":
                transacciones=Transaccion.objects.filter(condiciones_de_busqueda).order_by("-fecha_transaccion")[int(start):int(length)]
            else:
                transacciones=Transaccion.objects.filter(Q(sucursal=sucursal_usuario)).filter(condiciones_de_busqueda).order_by('-fecha_transaccion')[int(start):int(length)]
        totalRecordWithFilter=transacciones.count()
    else:
        if int(start)>=int(length):
            if tipo_usuario=="administrador":
                transacciones=Transaccion.objects.all().order_by('-fecha_transaccion')[int(start):int(length)+int(start)]
            else:
                transacciones=Transaccion.objects.filter(Q(sucursal=sucursal_usuario)).order_by('-fecha_transaccion')[int(start):int(length)]
            totalRecordWithFilter=transacciones.count()
        else:
            if tipo_usuario=="administrador":
                transacciones=Transaccion.objects.all().order_by('-fecha_transaccion')[int(start):int(length)]
            else:
                transacciones=Transaccion.objects.filter(Q(sucursal=sucursal_usuario)).order_by('-fecha_transaccion')[int(start):int(length)]
        totalRecordWithFilter=transacciones.count()
    
    for transaccion in transacciones:
        url_detalle=""
        action="""
                <div class="btn-group">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="%s">Detalle de venta</a></li>
                    </ul>
                </div> 
              """%(url_detalle)    
        data.append({
            'id':str(transaccion.id),
            'usuario':str(transaccion.usuario),
            'fecha_transaccion':timezone.localtime(transaccion.fecha_transaccion),
            'tipo_de_transaccion':str(transaccion.tipo_transacion),
            'sucursal':str(sucursal_usuario),
            'nombre_cliente':str(transaccion.nombre_cliente),
            'apellido_cliente':str(transaccion.apellido_cliente),
            'concepto':str(transaccion.concepto),
            'total':"$"+str(transaccion.total),
            'action':action
        })
    return JsonResponse({
        'draw':int(draw),
        'iTotalRecords':totalRecordWithFilter,
        'iTotalDisplayRecords':totalRecords,
        'data':data
    }, safe=False)