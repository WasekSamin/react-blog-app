from django.urls import path

from .views import *

app_name = "message"
urlpatterns = [
    path("comment-list/", CommentList.as_view(), name="comment-list"),
    path("comment-detail/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
    path("reply-list/", ReplyList.as_view(), name="reply-list"),
    path("reply-detail/<int:pk>/", ReplyDetail.as_view(), name="reply-detail"),
    path("react-blog-list/", ReactBlogList.as_view(), name="react-blog-list"),
    path("react-blog-detail/<int:pk>/", ReactBlogDetail.as_view(), name="react-blog-detail"),
    path("react-number-on-blog-list/", ReactNumberOnBlogList.as_view(), name="react-number-on-blog-list"),
    path("react-number-on-blog-detail/<int:pk>/", ReactNumberOnBlogDetail.as_view(), name="react-number-on-blog-detail"),
]