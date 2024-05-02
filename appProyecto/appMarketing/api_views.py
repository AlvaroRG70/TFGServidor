from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from django.db.models import Q,Prefetch, Avg,Max,Min,F
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView



@api_view(['GET'])
def servicio_list(request):
    servicios = Servicio.objects.all()
    serializer = ServicioSerializer(servicios, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def servicio_obtener(request,servicio_id):
   
    servicio = Servicio.objects.all()
    servicio = servicio.get(id=servicio_id)
    serializer = ServicioSerializer(servicio)
    return Response(serializer.data)


@api_view(['POST'])
def servicio_create(request):  
    serializers = ServicioSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Servicio CREADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['PUT'])
def servicio_editar(request,servicio_id):
    servicio = Servicio.objects.get(id=servicio_id)
    serializers = ServicioSerializer(data=request.data,instance=servicio)
    if serializers.is_valid():
        try:    
            serializers.save()
            return Response("Servicio EDITADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def servicio_eliminar(request,servicio_id): 
        servicio = Servicio.objects.get(id=servicio_id)
        try:
            servicio.delete()
            return Response("Servicio ELIMINADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework import generics
from rest_framework.permissions import AllowAny
from oauth2_provider.models import AccessToken   


class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = int(request.data.get('rol'))
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"), 
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    clientes = Cliente.objects.create( usuario = user)
                    clientes.save()
                elif(rol == Usuario.TRABAJADOR):
                    grupo = Group.objects.get(name='Trabajadores') 
                    grupo.user_set.add(user)    
                    trabajadores = Trabajador.objects.create(usuario = user)
                    trabajadores.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['POST'])
def agregar_carrito(request, servicio_id):
#    if(request.user.is_authenticated):
        if request.method == 'POST':
            aniadir_servicio = Servicio.objects.get(id=servicio_id)
            pedido_usuario = Pedido.objects.select_related("usuario").prefetch_related("servicio_carrito").filter(usuario=request.user, realizado=False).first()
            
            
            if (pedido_usuario):
                servicio_carrito = DetallesCarrito.objects.select_related("pedido", "servicio").filter(carrito = pedido_usuario, servicio = aniadir_servicio)
                if (servicio_carrito):                    
                    servicio_sumar = DetallesCarrito.objects.get(carrito=pedido_usuario, servicio = aniadir_servicio)
                    servicio_sumar.cantidad_producto += 1
                    servicio_sumar.save()
                else:
                    DetallesCarrito.objects.create(carrito=pedido_usuario, servicio = aniadir_servicio, cantidad_producto=1)

            else:
                Pedido.objects.create(usuario=request.user, realizado=False)
                pedido_usuario = Pedido.objects.get(usuario = request.user, realizado=False)
                DetallesCarrito.objects.create(carrito=pedido_usuario, servicio = aniadir_servicio,cantidad_producto = 1)
            
            return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)

#    else:
#      return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def obtener_carrito(request):
#    if(request.user.is_authenticated):
        
        try:
            pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False) 
            serializer = PedidoSerializer(pedido_usuario)
            serializer = serializer.data
            total_carrito = 0
            for servicios in pedido_usuario.detallescarrito_set.all():
                precio_servicio = servicios.servicio.precio
                cantidad_servicio = servicios.cantidad_producto
                total_carrito += precio_servicio * cantidad_servicio
            
            serializer_mejorado['total_carrito'] = total_carrito
            
            return Response(serializer_mejorado)
        
        except Pedido.DoesNotExist:
            Pedido.objects.create(usuario=request.user, realizado=False)
            pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False)
            serializer_mejorado=PedidoSerializer(pedido_usuario)
            return Response(serializer_mejorado.data)
        
#    else:
#        return Response("Necesita iniciar sesion", status=status.HTTP_405_METHOD_NOT_ALLOWED


@api_view(['DELETE'])
def eliminar_carrito(request, producto_id):
#    if(request.user.is_authenticated):
        if request.method == 'DELETE':
            try:
                eliminar_servicio = Servicio.objects.get(id=servicio_id)
                pedido_usuario = Pedido.objects.select_related("usuario").prefetch_related("servicio_carrito").filter(usuario=request.user, realizado=False).first()      
                DetallesCarrito.objects.select_related("pedido", "servicio").filter(carrito = pedido_usuario, servicio = eliminar_servicio).delete()       
                return Response({"Producto eliminado del carrito correctamente"}, status=status.HTTP_200_OK)
            
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 #   else:
 #       return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)










@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)