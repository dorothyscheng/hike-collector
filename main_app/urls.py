from django.urls import path
from . import views, views_user, views_review
from .views import HikeCreateView, HikeUpdateView, HikeDeleteView
from .views_user import UserDeleteView
from .views_review import ReviewDeleteView

app_name = 'hikes'
urlpatterns = [
    path('', views.home, name='home'),

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
    path('accounts/signup/', views_user.signup, name='signup'),
    path('user/<int:user_id>/', views_user.profile, name='profile'),
    path('user/<int:user_id>/update/', views_user.update_user, name='update_user'),
    path('user/<pk>/delete/', UserDeleteView.as_view(), name='delete_user'),

    # Reviews paths
    path('reviews/<int:hike_id>/add/', views_review.add_review, name='add_review'),
    path('reviews/<int:review_id>/update/', views_review.update_review, name='update_review'),
    path('reviews/<pk>/delete/', ReviewDeleteView.as_view(), name='delete_review'),
]