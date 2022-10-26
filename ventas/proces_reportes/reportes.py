import os
os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
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
from ventas.models import Venta

from django.db.models import Sum, Q
from django.http import JsonResponse


class ViewSelectReporteVentas(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="reportes/view_select_reporte_ventas.html"

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
        context['fecha_inicial']=fecha_inicial
        context['fecha_final']=fecha_final
        todas_las_ventas=None
        total_iva=0.0
        total_sin_iva=0.0
        total_con_iva=0.0
        if fecha_inicial==fecha_final:
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
            todas_las_ventas=Venta.objects.filter(Q(fecha_venta__gte=fecha_inicial) & Q(fecha_venta__lte=fecha_final))
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
    tipo_usuario=str(request.user.tipo_usuario)
    reporte_ventas_hoy=None
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
                'y':venta.total_con_iva
            })
        print("se imprimio..")
        print(datos)
    
    return JsonResponse(datos, safe=False)





