from django.urls import path
from user.views import UserManageView, UserCreateAPIView


urlpatterns = [
    path("me/", UserManageView.as_view(), name="manage"),
    path("registration/", UserCreateAPIView.as_view(), name="create"),
]

app_name = "user"
