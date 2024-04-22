from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario),
admin.site.register(Pedido),
admin.site.register(Servicio),
admin.site.register(DetallesCarrito),
admin.site.register(Pago),
admin.site.register(Factura),
admin.site.register(Resenias)
