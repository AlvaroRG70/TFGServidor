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



        
        

class ReseniasSerializer(serializers.ModelSerializer):

    usuario = ClienteSerializer()

    class Meta:
        model = Resenias
        fields = ('id', 'puntuacion', 'comentario', 'usuario')      
        
        
class ServicioSerializer(serializers.ModelSerializer):
        
    resenia = ReseniasSerializer(read_only=True, many=True)
    
    class Meta:
        model = Servicio
        fields = ('id', 'nombre', 'descripcion', 'precio', 'resenia')
        
class ServicioSerializerCreate(serializers.ModelSerializer):

 
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio']
    
    def validate_nombre(self,nombre):
        ServicioNombre = Servicio.objects.filter(nombre=nombre).first()
        if(not ServicioNombre is None):
             if(not self.instance is None and ServicioNombre.id == self.instance.id):
                 pass
             else:
                raise serializers.ValidationError('Ya existe un servicio con ese nombre')
        
        return nombre
    
    def validate_precio(self,precio):
        if precio < 0:
             raise serializers.ValidationError('tiene que ser positivo')
        return precio
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
             raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
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
    
        


    


class PedidoSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer()
    servicio_carrito = ServicioSerializer(read_only=True, many=True)
    
    class Meta:
        model = Pedido
        fields = ('id', 'realizado', 'usuario', 'servicio_carrito')
        

        

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
    
    
