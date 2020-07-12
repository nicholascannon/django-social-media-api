from django.urls import path

from .views import (
    PostListCreateAPIView,
    PostDetailAPIView
)

urlpatterns = [
    path('', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('<uuid>/', PostDetailAPIView.as_view(), name='post_detail'),
    # path('<uuid>/pin/', , name='pin_post'),
    # path('<uuid>/report/', , name='report_post'),
    # path('<uuid>/comment/', , name='post_comment'),
    # path('<post_uuid>/comment/<comment_uuid>/',
    #      , name='delete_comment'),
    # path('recent/', , name='recent_posts'),
    # path('user/<uuid>/', , name='get_user_posts')
]
