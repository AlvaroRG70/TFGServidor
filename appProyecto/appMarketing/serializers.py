from rest_framework import serializers
from .models import *
from datetime import date

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
   
        

class   ReseniasSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer()
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)

    class Meta:
        model = Resenias
        fields = ('id', 'puntuacion', 'comentario', 'usuario', 'servicio', 'servicio_nombre')    
        
class ReseniasSerializerEdit(serializers.ModelSerializer):


    class Meta:
        model = Resenias
        fields = ('id', 'puntuacion', 'comentario')    
        
        
class ServicioSerializer(serializers.ModelSerializer):        
    
    resenias = ReseniasSerializer(many=True, read_only=True)
    
    class Meta:
        model = Servicio
        fields = ('id','imagen', 'nombre', 'descripcion', 'precio', 'resenias')
        
class PaqueteServiciosSerializer(serializers.ModelSerializer):        
    
    servicios = ServicioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Servicio
        fields = ('id', 'nombre', 'descripcion', 'precio', 'servicios')
        
        
class ServicioSerializerCreate(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)  # Permitir que la imagen sea opcional

    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
    
    def validate_nombre(self, nombre):
        # Validación personalizada si es necesario
        return nombre
    
    def validate_precio(self, precio):
        # Validación personalizada si es necesario
        if precio < 0:
            raise serializers.ValidationError('precio negativo')
        return precio
    
    def validate_descripcion(self, descripcion):
        # Validación personalizada si es necesario
        
        return descripcion

    def create(self, validated_data):
        imagen = validated_data.pop('imagen', None)
        servicio = Servicio.objects.create(**validated_data)
        if imagen:
            servicio.imagen = imagen
            servicio.save()
        return servicio
    
class PaqueteServiciosSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'servicios']
    
    def validate_nombre(self, nombre):
        # Validación personalizada si es necesario
        return nombre
    
    def validate_precio(self, precio):
        # Validación personalizada si es necesario
        return precio
    
    def validate_descripcion(self, descripcion):
        # Validación personalizada si es necesario
        return descripcion


    
    
    

class ReseniasSerializerCreate(serializers.ModelSerializer):

 
    class Meta:
        model = Resenias
        fields = ['puntuacion', 'comentario', 'usuario', 'servicio']

    
    def validate_puntuacion(self,puntuacion):
        if puntuacion < 0 or puntuacion > 5:
             raise serializers.ValidationError('número entre 0 y 5')
        return puntuacion
    
    def validate_comentario(self,comentario):
        if len(comentario) < 0:
             raise serializers.ValidationError('No puede estar vacío')
        return comentario
    
        


class CarritoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoUsuario
        fields = ['cantidad', 'servicio']


class PedidoSerializer(serializers.ModelSerializer):
    
    
    detalles_carrito = CarritoUsuarioSerializer(many=True, read_only=True)
    usuario = UsuarioSerializer()
    servicio_carrito = ServicioSerializer(read_only=True, many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Pedido
        fields = ('id', 'realizado', 'usuario', 'servicio_carrito', 'detalles_carrito', 'total','descuento')
        

        
        
class PagoSerializer(serializers.ModelSerializer):

    pedido = PedidoSerializer()
    
    class Meta:
        model = Pago
        fields = ('id', 'fecha_pago', 'cantidad', 'pedido')
        

class PagoSerializerCreate(serializers.ModelSerializer):

    pedido = PedidoSerializer()

    class Meta:
        model = Pago
        fields = ['id', 'fecha_pago', 'cantidad', 'pedido']

        

class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username
    
    def validate_email(self,email):
        correo = Usuario.objects.filter(email=email).first()
        if(not correo is None):
             if(not self.instance is None and correo.id == self.instance.id):
                 pass
             else:
                raise serializers.ValidationError('Ya existe un usuario con ese correo')
        
        return email
    
    def validate_password1(self,password1):
        if len(password1) < 8:
             raise serializers.ValidationError('tiene que ser mayor que 8')
        return password1
    
    
