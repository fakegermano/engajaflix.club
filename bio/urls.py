from django.urls import path

from . import views

app_name = "bio"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profile/edit/', views.ProfileEditView.as_view(), name="edit_profile"),
    path('list/', views.UserListView.as_view(), name="user_list"),
]
