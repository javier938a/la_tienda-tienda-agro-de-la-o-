from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_weasyprint.utils import django_url_fetcher
import functools
import ssl
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django.conf import settings
from barcode import Gs1_128
import io
from barcode.writer import ImageWriter
import base64

class ViewGenerarCodigoBarra(TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name='proces_crear_codigo_barra/view_crear_codigo_barra.html'

#generando el pdf con el codigo de barra

class DetalleCodigoBarra(TemplateView):
    template_name="proces_crear_codigo_barra/print_codigo_barra.html"

class CustomCodigoBarraTemplateResponse(WeasyTemplateResponse):
    def get_url_fetcher(self):
        context=ssl.create_default_context()
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)

class PrintViewCodigoBarra(WeasyTemplateResponseMixin, DetalleCodigoBarra):
    
    
    pdf_stylesheets=[
        str(settings.STATIC_ROOT) + '/assets/css/estilos_codigo_barra/codigo_barra.css'
    ]
    pdf_attachment=False

    response_class=CustomCodigoBarraTemplateResponse

    def get_context_data(self, **kwargs):
        context=super(PrintViewCodigoBarra, self).get_context_data(**kwargs)
        
        codigo = self.request.GET.get('codigo')
        print("hola codigo: "+codigo)
    
        espacio_vacio=io.BytesIO()
        
        Gs1_128(codigo, writer=ImageWriter()).write(espacio_vacio)
        
        espacio_vacio.seek(0)
        imagen_str64=base64.b64encode(espacio_vacio.getvalue()).decode()
        context['codigo_barra_64']=imagen_str64
        
        return context