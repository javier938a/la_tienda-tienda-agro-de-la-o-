from django.urls import reverse_lazy, reverse
from ventas.models import Producto, User, DetalleCargaProductos
from ventas.forms import ProductoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.db.models import Q

class CrearProducto(LoginRequiredMixin, CreateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"

    template_name="proces_producto/crear_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

    def get_context_data(self, **kwargs):
        context=super(CrearProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None #Eliminando el '------'
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)#filtrando que solo se muestre el usuario logiado
        return context

class DetalleProducto(LoginRequiredMixin, DetailView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/detalle_producto.html"
    model=Producto
    context_object_name="producto"


class EditarProducto(LoginRequiredMixin, UpdateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/editar_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

    def get_context_data(self, **kwargs):
        context=super(EditarProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)
        return context

class EliminarProducto(LoginRequiredMixin, DeleteView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/eliminar_producto.html"
    model=Producto
    context_object_name="prod"
    success_url=reverse_lazy("store:list_prod")
    res=False
    def get_context_data(self, **kwargs):
        context=super(EliminarProducto, self).get_context_data(**kwargs)
        producto=Producto.objects.get(id=self.kwargs['pk'])
        if DetalleCargaProductos.objects.filter(producto=producto).exists():
            self.res=True
        context['res']=self.res
        return context
    

class ListarProductos(LoginRequiredMixin, TemplateView):
    login_url="/ventas/login/"
    redirect_field_name="redirect_to"
    template_name="proces_producto/listar_producto.html"


def verificar_producto_si_esta_cargado(request):
    id_producto=request.POST.get('id_producto')
    producto=Producto.objects.get(id=id_producto)
    res=False
    if DetalleCargaProductos.objects.filter(producto=producto).exists():
        res=True
    datos={
        'res':res,
    }
    return JsonResponse(
        datos, safe=False
    )
    
def obtener_lista_productos_json(request):
    #print(request.POST)
    data=[]
    productos=None
    draw=request.POST.get('draw')
    ##row seria el numero de pagina que el usuario presiona al buscar un registro
    row=request.POST.get('start')
    #rowperpage seria el numero de registros que debe mostrar la tabla
    rowperpage=request.POST.get('length')
    columnIndex=request.POST.get('order[0][column]')
    print(columnIndex)
    columnName=request.POST.get('columns['+columnIndex+'][data]')
    columnSortOrder=request.POST.get('order[0][dir]')
    print(columnSortOrder)
    print("columnane")
    print("Valor de start: "+row)
    print("Valor de length: "+rowperpage)
    print(columnName)


    print(request.POST)
    searchValue=request.POST.get('search[value]')
    #condiciones de busqueda para filtrar los datos
    codiciones_de_busqueda=None
    print("Entro valor de busqueda es: "+str(searchValue))
    if searchValue!='':
        print("Entro valor de busqueda es: "+searchValue)
        codiciones_de_busqueda=Q(descripcion__icontains=searchValue) | Q(nombre_producto__icontains=searchValue) | Q(codigo_barra=searchValue) | Q(categoria__categoria__icontains=searchValue) | Q(fecha_de_registro__date__contains=searchValue)

    #contanto el numero total de registros
    #totalRecords seria el numero de registros que hay en la base de datos
    totalRecords=Producto.objects.all().count()
    print("total de registros: "+str(totalRecords))

    ## numero de registros filtrados
    ##TotalRecordWidthFilter seria el numero de registros filtrados
    totalRecordWidthFilter=0
    ##primero verificamos se esta realizando una busqueda si nos es asi no hay que hacer ningun filtro
    if codiciones_de_busqueda is not None:##si hay condiciones porque se esta buscando pues hacemos el filtro
        if int(row)>=int(rowperpage):
            productos=Producto.objects.filter(codiciones_de_busqueda).order_by('-fecha_de_registro')[int(row):int(rowperpage)+int(row)]
        else:
           productos=Producto.objects.filter(codiciones_de_busqueda).order_by('-fecha_de_registro')[int(row):int(rowperpage)] 
        totalRecordWidthFilter = productos.count()
    else:
        #si row que el numero pagina es mayor o igual que el rowperpage que es el numero de registros que debe de mostrar en lapgina
        if int(row)>=int(rowperpage):#entonces ordenamos los registros en forma ascendente por fecha y solo mostramos los primeros registros delimitados entre  row y roperpage
                                    #pero le sumamos row para que tome los siguientes 10 cada vez que el usuario mande la peticion de la siguiente pagina ya que roperpage siempre mostrara los primeros 10 registros ya que es la cantidad de registros a mostrar 
                                    #si le sumamos el row obtenemos los siguientes registros ya que ese va contando de 10 en 10 o de 25 en 25 etc
                                    #si el numero de fijas que debe mostrar que por defecto es 10 que aqui lo definen con star es mayor el numero de filas que sigue se le suma rowperpage row para que siga con las siguientes
            productos=Producto.objects.all().order_by('-fecha_de_registro')[int(row):int(rowperpage)+int(row)]
        else:
            productos=Producto.objects.all().order_by('-fecha_de_registro')[int(row):int(rowperpage)]#de lo contrario muestra solos los primeros 10 o los primeros registros que selecciona el usuario
        
        totalRecordWidthFilter=productos.count()#se obtiene el numero total de productos registrados
    


    for producto in productos:
        url_editar=reverse('store:editar_prod', args=[producto.id])
        url_eliminar=reverse('store:del_prod', args=[producto.id])
        url_detalle=reverse('store:det_prod', args=[producto.id])
        action="""
                <div class="btn-group">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Action
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="%s">Editar</a></li>
                        <li><a class="dropdown-item" href="%s">Eliminar</a></li>
                        <li><a class="dropdown-item" href="%s">Detalle</a></li>
                    </ul>
                </div>
        """%(url_editar, url_eliminar, url_detalle)
        if producto.codigo_barra==None:            
            data.append({'id':producto.id,'codigo_barra':'No Existe','producto':producto.nombre_producto, 'fecha_de_registro':producto.fecha_de_registro, 'descripcion':str(producto.descripcion),'usuario':str(producto.usuario), 'categoria':str(producto.categoria), 'action':action })
        else:
            data.append({'id':producto.id,'codigo_barra':producto.codigo_barra,'producto':producto.nombre_producto, 'fecha_de_registro':producto.fecha_de_registro, 'descripcion':str(producto.descripcion), 'usuario':str(producto.usuario), 'categoria':str(producto.categoria), 'action':action })
    
    return JsonResponse(
        {
            "draw":int(draw),
            "iTotalRecords":totalRecordWidthFilter,
            'iTotalDisplayRecords':totalRecords,
            'data':data
        }, 
        safe=False
    )