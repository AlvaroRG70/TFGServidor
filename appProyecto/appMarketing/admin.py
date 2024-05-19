from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario),
admin.site.register(Pedido),
admin.site.register(Servicio),
admin.site.register(CarritoUsuario),
admin.site.register(Pago),
admin.site.register(Factura),
admin.site.register(Resenias),
admin.site.register(Cliente),
admin.site.register(Trabajador)

