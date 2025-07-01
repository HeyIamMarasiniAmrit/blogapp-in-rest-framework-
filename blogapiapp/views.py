from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import post as Post
from .serializers import postserializer
from django.db.models import Q


# ✅ Basic API Check
@api_view(['GET'])
def index(request):
    return Response({"success": "The setup was successful, Amrit"})
    

# ✅ Get All Posts with Pagination
@api_view(['GET'])
def GetAllPosts(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    posts = Post.objects.all().order_by('-created_at')
    result_page = paginator.paginate_queryset(posts, request)
    serializer = postserializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
    

# ✅ Create Post
@api_view(['POST'])
def CreatePost(request):
    serializer = postserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": "The post was successfully created"}, status=201)
    return Response(serializer.errors, status=400)
    

# ✅ Get a Single Post by ID
@api_view(['GET'])
def GetPost(request):
    post_id = request.query_params.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serializer = postserializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"error": "The post does not exist"}, status=404)
        

# ✅ Update Post
@api_view(['PUT'])
def UpdatePost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serializer = postserializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "The post was updated successfully"})
        return Response(serializer.errors, status=400)
    except Post.DoesNotExist:
        return Response({"error": "The post does not exist"}, status=404)

# ✅ Delete Post
@api_view(['DELETE'])
def DeletePost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"success": "The post was successfully deleted"})
    except Post.DoesNotExist:
        return Response({"error": "The post does not exist"}, status=404)

# ✅ Search Posts by Title or Content
@api_view(['GET'])
def SearchPosts(request):
    query = request.query_params.get('q', '')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    serializer = postserializer(posts, many=True)
    return Response(serializer.data)

# ✅ Toggle Publish Status
@api_view(['PUT'])
def TogglePublish(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.is_published = not post.is_published
        post.save()
        return Response({"success": f"Post publish status toggled to {post.is_published}"})
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

# ✅ Like Post
@api_view(['POST'])
def LikePost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return Response({"success": f"Post liked. Total likes: {post.likes}"})
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)


