#import os
#os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
from ast import Not
from datetime import timezone
from django.utils import timezone as ti
from datetime import datetime
from django.utils.timezone import make_aware
from django_weasyprint.utils import django_url_fetcher
import functools
import ssl
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.views.generic import DetailView, ListView, TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from ventas.models import Venta, AperturaCorte
from ventas.models import Sucursal
from ventas.models import User

from django.db.models import Sum, Q
from django.http import JsonResponse


class ViewSelectReporteVentas(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="reportes/view_select_reporte_ventas.html"
    
    def get_context_data(self, **kwargs):
        context=super(ViewSelectReporteVentas, self).get_context_data(**kwargs)
        sucursales=Sucursal.objects.all()
        usuarios=User.objects.all()
        context['usuarios']=usuarios
        context['sucursales']=sucursales
        return context

class ViewSelectReporteAperturas(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="reportes/view_reporte_aperturas.html"
    
    def get_context_data(self, **kwargs):
        context=super(ViewSelectReporteAperturas, self).get_context_data(**kwargs)
        sucursales=Sucursal.objects.all()
        context['sucursales']=sucursales
        return context


class DetalleReporteAperturas(TemplateView):
    template_name="reportes/reporte_aperturas.html"

class CustomAperturaTemplateReponse(WeasyTemplateResponse):
    def get_url_fetcher(self):
        context=ssl.create_default_context()
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)

class PrintViewReporteAperturas(WeasyTemplateResponseMixin, DetalleReporteAperturas):
    model=AperturaCorte
    context_object_name='apertura_corte'

    pdf_stylesheets=[
        str(settings.STATIC_ROOT) + '/assets/css/estilos_reporte_apertura/reporte_apertura.css',
    ]
    pdf_attachment=False

    response_class=CustomAperturaTemplateReponse

    def get_context_data(self, **kwargs):
        context=super(PrintViewReporteAperturas, self).get_context_data(**kwargs)
        tipo_reporte=self.request.GET['tipo_reporte']
        fecha_inicio=self.request.GET['fecha_inicial']
        fecha_final=self.request.GET['fecha_final'] 
        aperturas=None
        context['fecha_inicial']=fecha_inicio
        context['fecha_final']=fecha_final
        if tipo_reporte=="0":
            if fecha_inicio==fecha_final:
                aperturas=AperturaCorte.objects.filter(Q(fecha_de_apertura__date=fecha_inicio)).order_by("-fecha_de_apertura")
            else:
                aperturas=AperturaCorte.objects.filter(Q(fecha_de_apertura__gte=fecha_inicio) & Q(fecha_de_apertura__lte=fecha_final)).order_by("-fecha_de_apertura")
        elif tipo_reporte=="1":
                id_sucursal=self.request.GET['id_sucursal']
                
                if int(id_sucursal)>0:
                    sucursal=Sucursal.objects.get(id=id_sucursal)
                    if fecha_inicio==fecha_final:
                        aperturas=AperturaCorte.objects.filter(Q(usuario__sucursal=sucursal)).filter(Q(fecha_de_apertura__date=fecha_inicio)).order_by("-fecha_de_apertura")
                    else:
                        aperturas=AperturaCorte.objects.filter(Q(usuario__sucursal=sucursal)).filter(Q(fecha_de_apertura__gte=fecha_inicio) & Q(fecha_de_apertura__lte=fecha_final)).order_by("-fecha_de_apertura")
                else:
                    if fecha_inicio==fecha_final:
                        aperturas=AperturaCorte.objects.filter(Q(fecha_de_apertura__date=fecha_inicio)).order_by("-fecha_de_apertura")
                    else:
                        aperturas=AperturaCorte.objects.filter(Q(fecha_de_apertura__gte=fecha_inicio) & Q(fecha_de_apertura__lte=fecha_final)).order_by("-fecha_de_apertura") 

        context['apertura_corte']=aperturas

        return context

class DetalleReporteVentas(TemplateView):
    template_name="reportes/reporte_ventas.html"


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    def get_url_fetcher(self):
        context=ssl.create_default_context()
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)

class PrintViewReporteVentas(WeasyTemplateResponseMixin, DetalleReporteVentas):
    model=Venta
    context_object_name='ventas'
    
    pdf_stylesheets=[
        str(settings.STATIC_ROOT) + '/assets/css/estilos_reporte_venta/reporte_venta.css',
    ]
    
    pdf_attachment=False
    
    response_class=CustomWeasyTemplateResponse

    def get_context_data(self, **kwargs):
        context=super(PrintViewReporteVentas, self).get_context_data(**kwargs)
        fecha_inicial=self.request.GET['fecha_inicial']
        fecha_final=self.request.GET['fecha_final']
        tipo_reporte=self.request.GET['tipo_reporte']
        id_usuario=self.request.GET['id_usuario']
        id_sucursal=self.request.GET['id_sucursal']
        context['fecha_inicial']=fecha_inicial
        context['fecha_final']=fecha_final
        todas_las_ventas=None
        total_iva=0.0
        total_sin_iva=0.0
        total_con_iva=0.0
        if fecha_inicial==fecha_final:
            todas_las_ventas=None
            if tipo_reporte=="2" and id_usuario!="0":
                usuario_responsable=User.objects.get(id=id_usuario)
                todas_las_ventas=Venta.objects.filter(Q(fecha_venta__date=fecha_inicial) & Q(usuario=usuario_responsable))
            elif tipo_reporte=="1" and id_sucursal!="0":
                sucursal=Sucursal.objects.get(id=id_sucursal)
                todas_las_ventas=Venta.objects.filter(Q(fecha_venta__date=fecha_inicial) & Q(sucursal=sucursal))
            elif tipo_reporte=="0":
                todas_las_ventas=Venta.objects.filter(Q(fecha_venta__date=fecha_inicial))
            print("Estas...")
            print(todas_las_ventas)
            context['ventas']=todas_las_ventas
            total_iva_sum_dic=todas_las_ventas.aggregate(Sum('total_iva'))#obteniendo la suma total del iva
            total_sin_iva_dic=todas_las_ventas.aggregate(Sum('total_sin_iva'))#obteniendo la suma total sin iva
            total_sin_iva=total_sin_iva_dic['total_sin_iva__sum']
            total_iva=total_iva_sum_dic['total_iva__sum']
            total_con_iva_dic=todas_las_ventas.aggregate(Sum('total_con_iva'))##obteniendo la suma de el total del total con iva
            total_con_iva=total_con_iva_dic['total_con_iva__sum']
            if total_iva is not None and total_sin_iva is not None and total_con_iva is not None:
                context['total_iva_sum']=round(total_iva, 2)
                context['total_sin_iva_sum']=round(total_sin_iva, 2)
                context['total_con_iva_sum']= round(total_con_iva, 2)
            else:
                context['total_iva_sum']=""
                context['total_sin_iva_sum']=""
                context['total_con_iva_sum']= ""

        else:
            todas_las_ventas=None
            if tipo_reporte=="2" and id_usuario!="0":
                usuario_responsable=User.objects.get(id=id_usuario)
                todas_las_ventas=Venta.objects.filter(Q(fecha_venta__gte=fecha_inicial) & Q(fecha_venta__lte=fecha_final) & Q(usuario=usuario_responsable))
            elif tipo_reporte=="1" and id_sucursal!=0:
                sucursal=Sucursal.objects.get(id=id_sucursal)
                todas_las_ventas=Venta.objects.filter(Q(fecha_venta__gte=fecha_inicial) & Q(fecha_venta__lte=fecha_final) & Q(sucursal=sucursal))
            elif tipo_reporte=="0":
                todas_las_ventas=Venta.objects.filter(Q(fecha_venta__gte=fecha_inicial) & Q(fecha_venta__lte=fecha_final))
            print("hello!!")
            print(todas_las_ventas)
            if todas_las_ventas!=None:
                total_iva_sum_dic=todas_las_ventas.aggregate(Sum('total_iva'))#obteniendo la suma total del iva
                total_sin_iva_dic=todas_las_ventas.aggregate(Sum('total_sin_iva'))#obteniendo la suma total sin iva
                total_sin_iva=total_sin_iva_dic['total_sin_iva__sum']
                total_iva=total_iva_sum_dic['total_iva__sum']
                total_con_iva_dic=todas_las_ventas.aggregate(Sum('total_con_iva'))##obteniendo la suma de el total del total con iva
                total_con_iva=total_con_iva_dic['total_con_iva__sum']
                if total_iva is not None and total_sin_iva is not None and total_con_iva is not None:
                    context['ventas']=todas_las_ventas
                    context['total_iva_sum']=round(total_iva, 2)
                    context['total_sin_iva_sum']=round(total_sin_iva, 2)
                    context['total_con_iva_sum']= round(total_con_iva, 2)
                else:
                    context['ventas']=""
                    context['total_iva_sum']=""
                    context['total_sin_iva_sum']=""
                    context['total_con_iva_sum']= ""
        return context


class DownloadView(WeasyTemplateResponseMixin, DetalleReporteVentas):
    pdf_filename="reporte_venta.pdf"

class DynamicNameView(WeasyTemplateResponseMixin, DetalleReporteVentas):
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )


def grafico_reporte_ventas(request):
    fecha_hoy=ti.now().strftime("%Y-%m-%d")
    reporte_ventas_hoy=None
    if str(request.user)!="AnonymousUser":
        
        tipo_usuario=str(request.user.tipo_usuario)
       
        if tipo_usuario != None:
            if tipo_usuario=="administrador":
                reporte_ventas_hoy=Venta.objects.filter(Q(fecha_venta__date=fecha_hoy))
            elif tipo_usuario=="usuario":
                sucursal_usuario=request.user.sucursal
                reporte_ventas_hoy=Venta.objects.filter(Q(fecha_venta__date=fecha_hoy)).filter(Q(sucursal=sucursal_usuario))

    datos=[]
    if reporte_ventas_hoy!=None:
        for venta in reporte_ventas_hoy:
            datos.append({
                'x':venta.fecha_venta,
                'y':venta.total_sin_iva
            })
        print("se imprimio..")
        print(datos)
    
    return JsonResponse(datos, safe=False)





