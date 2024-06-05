from decimal import Decimal
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from django.db.models import Q,Prefetch, Avg,Max,Min,F
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


class emailAPIView(APIView):
    def post(self, request):
        try:
            to_email = request.data.get('to_email')
            subject = 'Digital South'
            message = '\033\nSu registro se ha efectuado con éxito.\nMuchas gracias por contar con nosotros, le mantendremos informados de todas las novedades que tengamos.\n\nReciba un cordial saludo.\n\n\n Digital South©\n\033'
            send_mail(subject, message, None, [to_email])
            return Response({'message':'Correo enviado con éxito'},status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'message':'error_message'},status=status.HTTP_400_BAD_REQUEST)

class emailPagado(APIView):
    def post(self, request):
        try:
            to_email = request.data.get('to_email')
            order_id = request.data.get('order_id') 
            subject = 'Digital South'
            message = f'Su pedido con identificador {order_id} se ha efectuado con éxito.\nMuchas gracias por contar con nosotros, le mantendremos informados de todas las novedades que tengamos.\n\nReciba un cordial saludo.\n\n\n Digital South©'
            send_mail(subject, message, None, [to_email, 'rodrimix70@gmail.com'])
            return Response({'message':'Correo enviado con éxito'}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
class emailContacto(APIView):
    def post(self, request):
        try:

            username = request.data.get('email_contact') 
            email_contact = request.data.get('email_contact') 
            subject = f'Cliente {username}, {email_contact}'
            message = request.data.get('message')
            send_mail(subject, message, None, ['rodrimix70@gmail.com'])
            return Response({'message':'Correo enviado con éxito'}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)


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
      
    serializer = ServicioSerializerCreate(data=request.data)
    if serializer.is_valid():
        try:
            # Guardar la imagen
            imagen = request.data.get('imagen', None)
            if imagen:
                serializer.validated_data['imagen'] = imagen
            serializer.save()
            return Response("Servicio creado", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
def agregar_carrito(request, servicio_id):
    aniadir_servicio = Servicio.objects.get(id=servicio_id)
    pedido_usuario = Pedido.objects.filter(usuario=request.user, realizado=False).first()

    if pedido_usuario:
        servicio_carrito = CarritoUsuario.objects.filter(pedido=pedido_usuario, servicio=aniadir_servicio).first()
        if servicio_carrito:
            servicio_carrito.cantidad += 1
            servicio_carrito.save()
        else:
            CarritoUsuario.objects.create(pedido=pedido_usuario, servicio=aniadir_servicio, cantidad=1)
    else:
        pedido_usuario = Pedido.objects.create(usuario=request.user, realizado=False)
        CarritoUsuario.objects.create(pedido=pedido_usuario, servicio=aniadir_servicio, cantidad=1)

    # Recalcular el total del pedido
    pedido_usuario.total = pedido_usuario.detalles_carrito.aggregate(total=Sum(F('cantidad') * F('servicio__precio')))['total'] or 0
    pedido_usuario.save()

    return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)


@api_view(['POST'])
# @login_required   
def agregar_carrito1(request, servicio_id):
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
            pedido_usuario = Pedido.objects.create(usuario=request.user, realizado=False)
            CarritoUsuario.objects.create(pedido=pedido_usuario, servicio=aniadir_servicio, cantidad=1)
        
        return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)




# @api_view(['GET'])
# def obtener_carrito1(request):
#     try:
#         # Buscar un pedido no realizado
#         pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False)
#     except Pedido.DoesNotExist:
#         # Si no existe un pedido no realizado, crea uno nuevo
#         pedido_usuario = Pedido.objects.create(usuario=request.user, realizado=False)

#     serializer = PedidoSerializer(pedido_usuario)
#     serializer_data = serializer.data
#     total_carrito = 0
#     detalles_carrito = []

#     for item in pedido_usuario.detalles_carrito.all():
#         precio_servicio = item.servicio.precio
#         cantidad_servicio = item.cantidad
#         total_carrito += precio_servicio * cantidad_servicio
        
#         imagen = item.servicio.imagen.url if item.servicio.imagen else None
#         detalles_carrito.append({
#             "servicio_id": item.servicio.id,
#             "imagen": imagen,
#             "nombre_servicio": item.servicio.nombre,
#             "cantidad": item.cantidad,
#             "precio": item.servicio.precio,
#             "total": precio_servicio * cantidad_servicio,
#         })

#     serializer_data['detalles_carrito'] = detalles_carrito
#     serializer_data['total_carrito'] = total_carrito

#     return Response(serializer_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def obtener_carrito(request):
    try:
        pedido_usuario = Pedido.objects.get(usuario=request.user, realizado=False)
    except Pedido.DoesNotExist:
        pedido_usuario = Pedido.objects.create(usuario=request.user, realizado=False)

    serializer = PedidoSerializer(pedido_usuario)
    serializer_data = serializer.data

    detalles_carrito = []

    for item in pedido_usuario.detalles_carrito.all():
        precio_servicio = item.servicio.precio
        cantidad_servicio = item.cantidad
        imagen = item.servicio.imagen.url if item.servicio.imagen else None
        detalles_carrito.append({
            "servicio_id": item.servicio.id,
            "imagen": imagen,
            "nombre_servicio": item.servicio.nombre,
            "cantidad": item.cantidad,
            "precio": item.servicio.precio,
            "total": precio_servicio * cantidad_servicio,
        })
        
    if len(detalles_carrito) == 4:
        pedido_usuario.descuento = Decimal('0.9')
        pedido_usuario.total = pedido_usuario.total *  pedido_usuario.descuento
    

    serializer_data['detalles_carrito'] = detalles_carrito
    serializer_data['total_carrito'] = pedido_usuario.total
    
    

    return Response(serializer_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def pagar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        if not pedido.detalles_carrito.exists():
            return Response({"error": "El carrito está vacío."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcular la cantidad total del pedido
        cantidad_total = sum(carrito_servicio.servicio.precio * carrito_servicio.cantidad for carrito_servicio in pedido.servicio_carrito.all())
        
        # Crear la instancia de pago
        pago = Pago.objects.create(
            fecha_pago=timezone.now(),
            cantidad=cantidad_total,
            pedido=pedido
        )
        
        # Marcar el pedido como realizado
        pedido.realizado = True
        pedido.save()
        
        return Response({"Pago realizado correctamente"}, status=status.HTTP_200_OK)
    
 
    
@api_view(['GET']) 
def pago_obtener(request,pago_id):
   
    pago = Pago.objects.all()
    pago = pago.get(pedido=pago_id)
    serializer = PagoSerializer(pago)
    return Response(serializer.data)

@api_view(['GET']) 
def pago_revisar(request,pago_id):
   
    pago = Pago.objects.all()
    pago = pago.get(pedido=pago_id)
    serializer = PagoSerializer(pago)
    return Response(serializer.data)

# @api_view(['GET', 'POST'])
# def pago_pedido(request, pedido_id):
#     if request.method == 'GET':
#         try:
#             pago = Pago.objects.get(pedido_id=pedido_id)
#             serializer = PagoSerializer(pago)
#             return Response(serializer.data)
#         except Pago.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'POST':
#         serializer = PagoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(pedido_id=pedido_id)
#             # Actualizar el estado del pedido a "realizado = True"
#             pedido = Pedido.objects.get(pk=pedido_id)
#             pedido.realizado = True
#             pedido.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def crear_pago(request, pedido_id):
#     # Verifica si el pedido existe
#     try:
#         pedido = Pedido.objects.get(pk=pedido_id, realizado=False)
#     except Pedido.DoesNotExist:
#         return Response({"error": "Pedido no encontrado o ya realizado."}, status=status.HTTP_404_NOT_FOUND)
    
#     # Crea una copia mutable de request.data
#     mutable_data = request.data.copy()
    
#     # Calcula la cantidad total del pedido
#     total_carrito = pedido.detalles_carrito.aggregate(
#         total=Sum(F('cantidad') * F('servicio__precio'))
#     )['total'] or 0
    
#     # Asigna el ID del pedido y la cantidad total del pedido al pago
#     mutable_data['pedido'] = pedido_id
#     mutable_data['cantidad'] = total_carrito

#     # Crea el serializer con los datos actualizados
#     serializer = PagoSerializer(data=mutable_data)
    
#     if serializer.is_valid():
#         try:
#             serializer.save()
#             pedido.realizado = True
#             pedido.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as error:
#             return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
        
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
        
        # Eliminar los items del carrito
        carrito_items.delete()
        
        # Recalcular el total del carrito
        total = sum(item.servicio.precio * item.cantidad for item in pedido_usuario.detalles_carrito.all())
        pedido_usuario.total = total
        pedido_usuario.save()
        
        return Response({"message": "Servicio eliminado del carrito correctamente", "total": total}, status=status.HTTP_200_OK)
    
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


@api_view(['DELETE'])
def usuario_eliminar(request,usuario_id): 
    usuario = Usuario.objects.get(id=usuario_id)
    try:
        usuario.delete()
        return Response("Servicio ELIMINADO")
    except Exception as error:
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
def buscar_servicio_por_nombre(request):
    nombre_servicio = request.query_params.get('nombre', '')
    servicios = Servicio.objects.filter(nombre__icontains=nombre_servicio)
    serializer = ServicioSerializer(servicios, many=True)
    return Response(serializer.data)    






from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            token = response.data.get('access_token')
            # Aquí puedes crear y devolver un token OAuth2
        return response
    
    
@api_view(['GET'])
def resenias_usuario(request):
    # Obtener todas las reseñas del usuario autenticado
    resenias = Resenias.objects.filter(usuario=request.user)
    serializer = ReseniasSerializer(resenias, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_obtener_pagos(request):
    # Obtener todos los pagos del usuario autenticado
    pagos = Pago.objects.filter(pedido__usuario=request.user)
    serializer = PagoSerializer(pagos, many=True)
    return Response(serializer.data)




class CheckUsernameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if Usuario.objects.filter(username=username).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)

class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if Usuario.objects.filter(email=email).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)
