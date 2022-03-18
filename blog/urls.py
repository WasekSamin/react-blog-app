from django.urls import path

from .views import *

app_name = "blog"
urlpatterns = [
    path("category-list/", CategoryList.as_view(), name="category-list"),
    path("category-detail/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    path("tag-list/", TagList.as_view(), name="tag-list"),
    path("tag-detail/<int:pk>/", TagDetail.as_view(), name="tag-detail"),
    path("blog-list/", BlogList.as_view(), name="blog-list"),
    path("blog-detail/<int:pk>/", BlogDetail.as_view(), name="blog-detail"),
]