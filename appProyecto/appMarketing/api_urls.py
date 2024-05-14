from django.urls import path

from .api_views import *

urlpatterns = [
    
    path('usuario/obtener/<str:nombreUsuario>', usuario_obtener),
    
    path('servicios', servicio_list),
    path('servicios/<int:servicio_id>', servicio_obtener),
    path('servicios/crear', servicio_create),
    path('servicios/editar/<int:servicio_id>',servicio_editar),
    path('servicios/eliminar/<int:servicio_id>',servicio_eliminar),
    
    path('resenias', resenia_list),
    path('resenias/<int:resenia_id>', resenia_obtener),
    path('resenias/create/<int:usuario_id>/<int:servicio_id>', resenia_create),
    path('resenia/editar/<int:resenia_id>',resenia_editar),
    path('resenia/eliminar/<int:resenia_id>',resenia_eliminar),
    
    path('servicios/aniadir_carrito/<int:servicio_id>',agregar_carrito),
    path('servicios/ver_carrito',obtener_carrito),
    path('servicios/eliminar_carrito/<int:servicio_id>',eliminar_carrito),
    
    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
    
]