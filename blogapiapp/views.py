from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from status.commands.http_request import Post
from .models import post as Post


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
@api_view(['GET', 'POST'])
def CreatePost(request):
    data = request.data
    serializer = postserializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success: The post was Sucessfully created"}, status=201)
    else:
         return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def DeletePost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"success: The post was Successfully deleted"}, status = 200)
    except post.DoesNotExist:
        return Response({"Error: The post does not exist"}, status = 404)

@api_view(['GET'])
def GetPost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serializer = postserializer(post)
        return Response(serializer.data)
    except post.DoesNotExist:
        return Response({"Error: The post does not exist"}, status=404)


@api_view(['PUT'])
def UpdatePost(request):
    post_id = request.data.get('post_id')
    get_new_title = request.data.get('new_title')
    get_new_content = request.data.get('new_content')
    try:
        post = Post.objects.get(id=post_id)
        if get_new_title:
            post.title = get_new_title
        if get_new_content:
            post.content = get_new_content

        post.save()
        return Response({"Success: The Post is change"})
    except post.DoesNotExist:
        return Response({"Error: The post does not exist"}, status=404)
