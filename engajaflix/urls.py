"""engajaflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from bio.views import (
    CustomLoginView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    RegisterView,
    ComingSoonView,
)

urlpatterns = [
    path('verification/', include('verify_email.urls')),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', RegisterView.as_view(), name="register"),
    path('soon/', ComingSoonView.as_view(), name="coming_soon"),
    path('bio/', include('bio.urls')),
    path('', include('missions.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += [path('admin/', admin.site.urls, name="admin")]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)