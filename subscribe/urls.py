from django.urls import path

from .views import *

app_name = "subscribe"
urlpatterns = [
    path("subscribe-list/", SubscribeList.as_view(), name="subscribe-list"),
    path("subscribe-detail/<int:pk>/",
         SubscribeDetail.as_view(), name="subscribe-detail"),
]
