from rest_framework.serializers import ModelSerializer
from .models import post


class postserializer(ModelSerializer):
    class Meta:
        model = post
        fields = '__all__'
