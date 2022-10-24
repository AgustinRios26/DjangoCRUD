from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import viewsets
from profiles_api import serializers, models, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated



class HelloApiView(APIView):
    """ API View de Prueba"""
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        """Retornar lista de caracteristicas del APIView"""
        an_apiview = [
            'Usamos metodos HTTP como funciones (get, post, patch, put, delete)', 'Es similar a una vista tradicional de Django', 'Nos da el mayor control sobre la logica de nuestra aplicacion', 'Esta mapeado manualmente a los URLs',
        ]
        
        return Response({'message': 'Hello', 'an_apiview': an_apiview })
    
    def post(self, request):
        """Crea un mensaje con nuestro nombre"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response ({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Actualizar un objeto"""
        return Response({'method': 'PUT'})
    def patch(self, request, pk=None):
        """Actualizar un objeto parcialmente"""
        return Response({'method': 'PATCH'})
    def delete(self, request, pk=None):
        """Borrar un objeto"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API viewset"""
    serializer_class = serializers.HelloSerializer


    def list(self, request):
        a_viewset = [
            'Usa acciones (list, create, retrieve, update, partial_update)',
            'Automaticamente mapea a los URLs usando Routers', 'Provee mas funcionalidad con menos codigo'
        ]
        
        return Response({'message': 'Hola', 'a_viewset': a_viewset })
    
    def create(self, request):
        """Crear nuevo mensaje"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response ({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Obtenemos el objecto por su ID"""
        return Response({'http_method': 'GET'})
    def update(self, request, pk=None):
        """Actualiza un objeto"""
        return Response({'http_method': 'PUT'})
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente el objeto"""
        return Response({'http_method': 'PATCH'})
    def destroy(self, request, pk=None):
        """Destruye un objeto"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Crear y actualizar perfiles """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')
        
class UserLoginApiView(ObtainAuthToken):
    """Crear tokens de autenticacion de usuario"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Maneja el crear, leer y actualizar el prfile feed"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer    
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    
    def perform_create(self, serializer):
        """" Setear el perfil de usuario para el usuario que esta logeado """
        serializer.save(user_profile=self.request.user)

    