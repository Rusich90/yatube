from rest_framework import viewsets, status
from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission, IsAuthenticated
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.filter(post=id)
#     serializer_class = CommentSerializer

class OwnResourcePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user == obj.author
        return True


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OwnResourcePermission, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET', 'POST'])
def api_comments(request, pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(post=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        post = Post.objects.get(id=pk)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comments_edit(request, pk, cpk):
    if request.method == 'GET':
        comment = Comment.objects.get(id=cpk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        comment = Comment.objects.get(id=cpk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'PATCH':
        comment = Comment.objects.get(id=cpk)
        if request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment = Comment.objects.get(id=cpk)
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)