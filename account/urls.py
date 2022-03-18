from django.urls import path

from .views import *

app_name = "account"
urlpatterns = [
    path("account-list/", AccountList.as_view(), name="account-list"),
    path("account-detail/<int:pk>/", AccountDetail.as_view(), name="account-detail")
]