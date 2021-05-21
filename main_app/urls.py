from django.urls import path
from . import views

app_name = 'hikes'
urlpatterns = [
    path('', views.home, name='home'),
    path('hikes/', views.index, name='index'),
    path('hikes/<int:hike_id>/', views.detail, name='detail')
]