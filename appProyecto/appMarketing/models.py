from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



class Usuario(AbstractUser):
    TRABAJADOR = 1
    CLIENTE = 2
    ROLES = (
        (TRABAJADOR, 'trabajador'),
        (CLIENTE, 'cliente'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=2
    )
    

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente_rel', unique=True)
    def __str__(self):
        return self.usuario.username
      
class Trabajador(models.Model):
    trabajador = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='trabajador_rel', unique=True)  
    
 
class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.FloatField()
    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    realizado = models.BooleanField(default=False)
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio_carrito = models.ManyToManyField(Servicio)

class DetallesCarrito(models.Model):
    cantidad = models.IntegerField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)


class Pago(models.Model):
    METODOS_PAGO = (
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'PayPal'),
        ('efectivo', 'Efectivo'),
    )
    
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    cantidad = models.IntegerField()
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    
class Factura(models.Model):
    fecha_emision = models.DateField()
    cantidad_total = models.IntegerField()
    descuento = models.IntegerField()
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    


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
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='resenias',null=True, blank=True)

    
