from django.urls import path
from . import views
from .views import HikeCreateView, HikeUpdateView, HikeDeleteView, ReviewDeleteView, UserDeleteView

app_name = 'hikes'
urlpatterns = [
    path('', views.home, name='home'),
    
    path('accounts/signup/', views.signup, name='signup'),

    # Hikes paths
    path('hikes/add/', HikeCreateView.as_view(), name='add'),
    path('hikes/', views.index, name='index'),
    path('hikes/<pk>/update/', HikeUpdateView.as_view(), name='update'),
    path('hikes/<pk>/delete/', HikeDeleteView.as_view(), name='delete'),
    path('hikes/<int:hike_id>/add_photo/', views.add_photo, name='add_photo'),
    path('hikes/<int:hike_id>/favorite/', views.favorite, name='favorite'),
    path('hikes/<int:hike_id>/completed/', views.completed, name='completed'),
    path('hikes/<int:hike_id>/', views.detail, name='detail'),

    # User paths
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('user/<pk>/delete/', UserDeleteView.as_view(), name='delete_user'),

    # Reviews paths
    path('reviews/<int:hike_id>/add/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/update/', views.update_review, name='update_review'),
    path('reviews/<pk>/delete/', ReviewDeleteView.as_view(), name='delete_review'),
]