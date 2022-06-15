from pyexpat import model
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from ventas.models import User
from ventas.forms import UserForm
from django.urls import reverse_lazy


class DetalleUsuario(DetailView):
    model=User
    template_name="proces_usuario/detalle_usuario.html"
    context_object_name="usuario"

class CrearUsuario(CreateView):
    template_name="proces_usuario/crear_usuario.html"
    model=User
    form_class=UserForm
    context_object_name="form"
    success_url=reverse_lazy('store:user')

class EditarUsuario(UpdateView):
    template_name="proces_usuario/editar_usuario.html"
    model=User
    form_class=UserForm
    context_object_name="form"
    success_url=reverse_lazy("store:user")

class EliminarUsuario(DeleteView):
    template_name="proces_usuario/eliminar_usuario.html"
    model=User
    context_object_name="user"
    success_url=reverse_lazy("store:user")

class ListarUsuarios(ListView):
    template_name='proces_usuario/listar_usuario.html'
    model=User
    context_object_name="entity"
    '''
    def paginar(self, listado, page):
        parte_de_lista=None
        paginador=None
        datos={}
        try:
            paginador=Paginator(listado, 20)
            parte_de_lista=paginador.page(page)
            datos['paginador']=paginador
            datos['parte_de_lista']=parte_de_lista
        except:
            raise Http404
        return datos
    '''

    def get_context_data(self, **kwargs) :
        context = super(ListarUsuarios, self).get_context_data(**kwargs)
        '''
        user=self.request.user
        page=self.request.GET.get('page', 1)
        if user.is_authenticated:
            clave = self.request.GET.get('clave')
            if clave is not None:
                usuarios=User.objects.filter(Q(username__icontains=clave))
                datos=self.paginar(usuarios, page)
                context['entity']=datos.get('parte_de_lista')
                context['paginator']=datos.get('paginador')
            else:
                usuarios=User.objects.all()
                datos=self.paginar(usuarios, page)
                context['entity']=datos.get('parte_de_lista')
                context['paginator']=datos.get('paginador')
        '''

            

        return context

    