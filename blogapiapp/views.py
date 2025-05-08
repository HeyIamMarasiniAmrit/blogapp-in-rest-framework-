from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import post
from .serializers import postserializer


# Create your views here.
@api_view(['GET'])
def index(request):
    return Response({"sucess": "The setup was sucessful amrit"})

@api_view(['GET'])
def GetAllPosts(request):
    get_posts = post.objects.all()
    serializer = postserializer(get_posts, many=True)
    return Response(serializer.data)