"""
URL configuration for GoNoGo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views
from events import views as events_views


urlpatterns = [
    path('login/', include('authentication.urls')),
    path('api/signup/', auth_views.signup_view, name='signup'),
    path('admin/', admin.site.urls),
    path("", auth_views.home_view, name="home"),
    path("signup/", auth_views.signup_view, name="sign_up_page"),
    path("dashboard/", events_views.events_dashboard, name="events_dashboard"),
    path("new_event/", events_views.new_event, name="new_event")
]
