from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)        
    image = serializers.ImageField(required=False, use_url=True)
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image', 'created_by', 'updated_by', 'created_at', 'updated_at', 'token')        
    
    def create(self, validated_data):        
        print(validated_data)
        user = Token.objects.get(key=validated_data['token']).user                
        item = Item(
            name=validated_data['name'],
            description=validated_data['description'],
            created_by=user 
        )
        item.save()
        return item

    def update(self, instance, validated_data):        
        print(validated_data)
        user = Token.objects.get(key=validated_data['token']).user   
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.updated_by = user
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance