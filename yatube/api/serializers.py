from rest_framework import serializers
from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #group = serializers.StringRelatedField(source='group.title')
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')