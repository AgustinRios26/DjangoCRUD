from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializar campo para probar nuestra APIView"""
    name = serializers.CharField(max_length=10)
    
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializar objeto de perfil de usuario"""
    
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email' , 'name', 'password')
        extra_kwargs = {
            'password':{
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
        
    def create(self, validated_data):
        """ Crear y retornar un nuevo usuario """
        user = models.UserProfile.objects.create_user(
            email= validated_data['email'],
            name= validated_data['name'],
            password= validated_data['password']
            )
        
        return user
    
    def update(self, instance, validated_data):
        """ Actualizamos la cuenta del usuario """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
            
        return super().update(instance, validated_data)
        
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Es el serializador de profile feed Items"""
    class Meta:
        model = models.ProfileFeedItem        
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}