from django.urls import path
from . import views
from .views import HikeCreateView

app_name = 'hikes'
urlpatterns = [
    path('', views.home, name='home'),
    path('hikes/add/', HikeCreateView.as_view(), name='add'),
    path('hikes/', views.index, name='index'),
    path('hikes/<int:hike_id>/', views.detail, name='detail')
]