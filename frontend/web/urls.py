from django.urls import path
from . import views
#File created by myself

urlpatterns = [
    path('', views.home, name='index'),
    path('load/', views.massive_load, name='massive'),
    path('clean/', views.reset_load, name='reset'),
]