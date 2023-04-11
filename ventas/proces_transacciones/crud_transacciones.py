from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from ventas.models import Transaccion
from django.http import JsonResponse

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
            'total':"$"+str(transaccion.total),
            'action':action
        })
    return JsonResponse({
        'draw':int(draw),
        'iTotalRecords':totalRecordWithFilter,
        'iTotalDisplayRecords':totalRecords,
        'data':data
    }, safe=False)