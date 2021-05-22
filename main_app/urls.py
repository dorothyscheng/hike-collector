from django.urls import path
from . import views
from .views import HikeCreateView, HikeUpdateView, HikeDeleteView

app_name = 'hikes'
urlpatterns = [
    path('', views.home, name='home'),
    path('hikes/add/', HikeCreateView.as_view(), name='add'),
    path('hikes/', views.index, name='index'),
    path('hikes/<pk>/update', HikeUpdateView.as_view(), name='update'),
    path('hikes/<pk>/delete', HikeDeleteView.as_view(), name='delete'),
    path('hikes/<int:hike_id>/', views.detail, name='detail')
]