from django.urls import path

from . import views as v
from .views import AddUserToWatchedVideo

urlpatterns = [
    path('video/create', v.VideoCreateAPIView.as_view()),
    path('video/all', v.VideoListAPIView.as_view()),
    path('video/<int:pk>', v.VideoDetailAPIView.as_view()),
    path('add-user/<int:video_id>', AddUserToWatchedVideo.as_view(), name='add_user_to_watched_video'),
]
