from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (CLIENTE, 'cliente'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=1
    )
    
    # Cambios en los nombres de los accesores inversos
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='usuario_groups'  # Cambia el nombre del accesor inverso
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='usuario_user_permissions'  # Cambia el nombre del accesor inverso
    )

class Factura(models.Model):
    fecha_emision = models.DateField()
    cantidad_total = models.IntegerField()
    descuento = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class Pago(models.Model):
    METODOS_PAGO = (
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'PayPal'),
        ('efectivo', 'Efectivo'),
    )
    
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    cantidad = models.IntegerField()
    factura = models.OneToOneField(Factura, on_delete=models.CASCADE)
    
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.FloatField()
    carritos = models.ManyToManyField(Carrito, through='DetallesCarrito')

class DetallesCarrito(models.Model):
    cantidad = models.FloatField()
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
class Resenias(models.Model):
    comentario = models.TextField()
    PUNTUACION = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    puntuacion = models.IntegerField(choices=PUNTUACION)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
