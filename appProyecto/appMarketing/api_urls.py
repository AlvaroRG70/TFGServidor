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
    path('resenia/usuario',resenias_usuario),
    
    
    path('servicios/aniadir_carrito/<int:servicio_id>',agregar_carrito),
    path('servicios/ver_carrito',obtener_carrito),
    path('servicios/eliminar_carrito/<int:servicio_id>',eliminar_carrito),
    
    path('servicios/pagar/<int:pedido_id>',pagar_pedido),
    path('obtener/pago/<int:pago_id>',pago_obtener),
    path('revisar/pago/<int:pago_id>',pago_obtener),
    

    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
    path('usuario/eliminar/<int:usuario_id>',usuario_eliminar),
    path('usuario/pagos',usuario_obtener_pagos),
    
    
    
    path('send-email', emailAPIView.as_view(), name='send-email'),
    path('email/pagado', emailPagado.as_view(), name='pagado-email'),
    path('email/contacto', emailContacto.as_view(), name='pagado-email'),
    
        
    path('servicio/buscar', buscar_servicio_por_nombre),       
    
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'), 
    
    path('check-username', CheckUsernameView.as_view(), name='check-username'),
    path('check-email', CheckEmailView.as_view(), name='check-email'),
    
    
]