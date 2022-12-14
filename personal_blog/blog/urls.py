from . import views
from django.urls import path

urlpatterns=[
    path('', views.index, name="index"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name="register"),
    path('new_post/', views.new_post, name="new-post"),
]