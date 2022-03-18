from django.urls import path

from .views import *

app_name = "contact"
urlpatterns = [
    path("contact-list/", ContactList.as_view(), name="contact-list"),
    path("contact-detail/<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
]