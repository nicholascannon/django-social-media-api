from django.urls import path

from .views import (
    PostListCreateAPIView,
    PostDetailAPIView,
    PinPostAPIView,
    CommentListCreateAPIView,
    CommentDestroyAPIView
)

urlpatterns = [
    path('', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('<uuid>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('<uuid>/pin/', PinPostAPIView.as_view(), name='pin_post'),
    path('<uuid>/comment/', CommentListCreateAPIView.as_view(),
         name='comment_list_create'),
    path('<post_uuid>/comment/<comment_uuid>/',
         CommentDestroyAPIView.as_view(), name='delete_comment'),
    # path('recent/', , name='recent_posts'),
    # path('user/<uuid>/', , name='get_user_posts')
]
