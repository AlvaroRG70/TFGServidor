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
def usuario_obtener(request,nombreUsuario):
   
    usuario = Usuario.objects.all()
    usuario = usuario.get(username=nombreUsuario)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

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
        
# @api_view(['GET'])
# def servicio_buscar(request):
    
#     formulario = ServicioBuscarForm(request.query_params)
    
#     if formulario.is_valid():
#         texto = formulario.cleaned_data.get('textoBusqueda')
#         servicios = Servicio.objects.all()
#         servicios = servicios.filter(Q(nombre__contains=texto)).all()
#         serializer = ServicioSerializer(servicios, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET']) 
def resenia_obtener(request,resenia_id):
   
    resenia = Resenias.objects.all()
    resenia = resenia.get(id=resenia_id)
    serializer = ReseniasSerializer(resenia)
    return Response(serializer.data)
        
@api_view(['GET'])
def resenia_list(request):
    servicios = Resenias.objects.all()
    serializer = ReseniasSerializer(servicios, many=True)
    return Response(serializer.data)


#@api_view(['POST'])
# def resenia_create(request):  
#     serializers = ReseniasSerializerCreate(data=request.data)
#     if serializers.is_valid():
#         try:
#             serializers.save()
#             return Response("Reseña CREADO")
#         except Exception as error:
#             return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     else:
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)      

@api_view(['POST'])
def resenia_create(request, usuario_id, servicio_id):  
    # Verifica si el usuario y el servicio existen
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        servicio = Servicio.objects.get(id=servicio_id)
    except (Usuario.DoesNotExist, Servicio.DoesNotExist):
        return Response("Usuario o servicio no encontrado", status=status.HTTP_404_NOT_FOUND)

    # Crea una copia mutable de request.data
    mutable_data = request.data.copy()

    # Agrega los IDs de usuario y servicio a la copia mutable
    mutable_data['usuario'] = usuario_id
    mutable_data['servicio'] = servicio_id

    # Crea el serializer con los datos actualizados
    serializer = ReseniasSerializerCreate(data=mutable_data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Reseña CREADA", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def resenia_editar(request,resenia_id):
    servicio = Resenias.objects.get(id=resenia_id)
    serializers = ReseniasSerializerEdit(data=request.data,instance=servicio)
    if serializers.is_valid():
        try:        
            serializers.save()
            return Response("Resenia EDITADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def resenia_eliminar(request,resenia_id): 
    servicio = Resenias.objects.get(id=resenia_id)
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
                    cliente = Cliente.objects.create(usuario=user)

                    cliente.save()
                elif(rol == Usuario.TRABAJADOR):
                    grupo = Group.objects.get(name='Trabajadores') 
                    grupo.user_set.add(user)    
                    trabajador = Trabajador.objects.create(trabajador=user)

                    trabajador.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    


# @api_view(['POST'])
# def agregar_carrito(request, servicio_id):
# #    if(request.user.is_authenticated):
#         if request.method == 'POST':
#             aniadir_servicio = Servicio.objects.get(id=servicio_id)
#             pedido_usuario = Pedido.objects.select_related("usuario").prefetch_related("servicio_carrito").filter(usuario=request.user, realizado=False).first()
            
            
#             if (pedido_usuario):
#                 servicio_carrito = CarritoUsuario.objects.select_related("pedido", "servicio").filter(carrito = pedido_usuario, servicio = aniadir_servicio)
#                 if (servicio_carrito):                    
#                     servicio_sumar = CarritoUsuario.objects.get(carrito=pedido_usuario, servicio = aniadir_servicio)
#                     servicio_sumar.cantidad_producto += 1
#                     servicio_sumar.save()
#                 else:
#                     CarritoUsuario.objects.create(carrito=pedido_usuario, servicio = aniadir_servicio, cantidad_producto=1)

#             else:
#                 Pedido.objects.create(usuario=request.user, realizado=False)
#                 pedido_usuario = Pedido.objects.get(usuario = request.user, realizado=False)
#                 CarritoUsuario.objects.create(carrito=pedido_usuario, servicio = aniadir_servicio,cantidad_producto = 1)
            
#             return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)

#    else:
#      return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
# @login_required   
def agregar_carrito(request, servicio_id):
    if request.method == 'POST':
        aniadir_servicio = Servicio.objects.get(id=servicio_id)
        pedido_usuario = Pedido.objects.select_related("usuario").prefetch_related("servicio_carrito").filter(usuario=request.user, realizado=False).first()
        
        if pedido_usuario:
            servicio_carrito = CarritoUsuario.objects.filter(pedido=pedido_usuario, servicio=aniadir_servicio).first()
            if servicio_carrito:
                servicio_carrito.cantidad += 1
                servicio_carrito.save()
            else:
                CarritoUsuario.objects.create(pedido=pedido_usuario, servicio=aniadir_servicio, cantidad=1)
        else:
            Pedido.objects.create(usuario=request.user, realizado=False)
            pedido_usuario = Pedido.objects.create(usuario=request.user, realizado=False)
            CarritoUsuario.objects.create(pedido=pedido_usuario, servicio=aniadir_servicio, cantidad=1)
        
        return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)





@api_view(['GET'])
def obtener_carrito(request):
    try:
        pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False) 
        serializer = PedidoSerializer(pedido_usuario)
        serializer_data = serializer.data
        total_carrito = 0
        detalles_carrito = []
        
        for item in pedido_usuario.detalles_carrito.all():  # Utiliza el nombre correcto
            precio_servicio = item.servicio.precio
            cantidad_servicio = item.cantidad
            total_carrito += precio_servicio * cantidad_servicio
            detalles_carrito.append({
                "servicio_id": item.servicio.id,
                "nombre_servicio": item.servicio.nombre,
                "cantidad": item.cantidad,
                "precio": item.servicio.precio,
                "total": precio_servicio * cantidad_servicio,
            })
        
        serializer_data['detalles_carrito'] = detalles_carrito
        serializer_data['total_carrito'] = total_carrito
        
        return Response(serializer_data, status=status.HTTP_200_OK)
    
    except Pedido.DoesNotExist:
        pedido_usuario = Pedido.objects.create(usuario=request.user, realizado=False)
        serializer = PedidoSerializer(pedido_usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
#    else:
#        return Response("Necesita iniciar sesion", status=status.HTTP_405_METHOD_NOT_ALLOWED



        
        
        
# @api_view(['GET'])
# def obtener_carrito(request):
# #    if(request.user.is_authenticated):
        
#         try:
#             pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False) 
#             serializer = PedidoSerializer(pedido_usuario)
#             serializer = serializer.data
#             total_carrito = 0
#             for servicios in pedido_usuario.detallescarrito_set.all():
#                 precio_servicio = servicios.servicio.precio
#                 cantidad_servicio = servicios.cantidad_producto
#                 total_carrito += precio_servicio * cantidad_servicio
            
#             serializer_mejorado['total_carrito'] = total_carrito
            
#             return Response(serializer_mejorado)
        
#         except Pedido.DoesNotExist:
#             Pedido.objects.create(usuario=request.user, realizado=False)
#             pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False)
#             serializer_mejorado=PedidoSerializer(pedido_usuario)
#             return Response(serializer_mejorado.data)


@api_view(['DELETE'])
def eliminar_carrito(request, servicio_id):
    try:
        eliminar_servicio = Servicio.objects.get(id=servicio_id)
        pedido_usuario = Pedido.objects.select_related("usuario").prefetch_related("servicio_carrito").filter(usuario=request.user, realizado=False).first()
        
        if not pedido_usuario:
            return Response({"error": "No hay un pedido activo para este usuario"}, status=status.HTTP_404_NOT_FOUND)

        carrito_items = CarritoUsuario.objects.select_related("pedido", "servicio").filter(pedido=pedido_usuario, servicio=eliminar_servicio)
        
        if not carrito_items.exists():
            return Response({"error": "El servicio no está en el carrito"}, status=status.HTTP_404_NOT_FOUND)
        
        carrito_items.delete()
        return Response({"message": "Servicio eliminado del carrito correctamente"}, status=status.HTTP_200_OK)
    
    except Servicio.DoesNotExist:
        return Response({"error": "El servicio no existe"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 #   else:
 #       return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)










@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

# def obtener_usuario_token(request):
#     # Obtener el token del usuario desde la solicitud (probablemente lo envíes en el encabezado de autorización)
#     token = request.auth
#     if token is None:
#         return Response({"error": "Token de autorización no proporcionado"}, status=400)

#     try:
#         # Obtener el modelo AccessToken correspondiente al token
#         modelo_token = AccessToken.objects.get(token=token)
#     except AccessToken.DoesNotExist:
#         return Response({"error": "Token de autorización no válido"}, status=400)

#     try:
#         # Obtener el usuario correspondiente al token
#         usuario = Usuario.objects.get(id=modelo_token.user_id)
#     except Usuario.DoesNotExist:
#         return Response({"error": "No se encontró el usuario correspondiente al token"}, status=400)

#     # Serializar y devolver los datos del usuario
#     serializer = UsuarioSerializer(usuario)
#     return Response(serializer.data)