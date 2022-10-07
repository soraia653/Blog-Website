from email.quoprimime import body_check
from turtle import title
import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from django.contrib.auth import get_user_model
from blog.models import *

# define query schema
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'published_date', 'status', 'slug_title')

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(graphene.ObjectType):

    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(UserType, username=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    post_by_key = graphene.Field(PostType, post_key=graphene.ID())
    posts_by_slug = graphene.List(PostType, slug=graphene.String())


    def resolve_all_posts(root, info):
        return Post.objects.all()
    
    def resolve_author_by_username(root, info, username):
        return User.objects.get(username=username)
    
    def resolve_posts_by_author(root, info, username):
        return Post.objects.filter(author__username=username)
    
    def resolve_post_by_key(root, info, post_key):
        return Post.objects.get(pk=post_key)
    
    def resolve_posts_by_slug(root, info, slug):
        return Post.objects.filter(slug_title=slug)

schema = graphene.Schema(query=Query)