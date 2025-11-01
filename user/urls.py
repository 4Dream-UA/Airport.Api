from django.urls import path
from user.views import UserManageView


urlpatterns = [
    path("me/", UserManageView.as_view(), name="manage"),
]

app_name = "user"
