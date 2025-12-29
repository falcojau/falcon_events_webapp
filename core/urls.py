"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from falcon_events.views import HomeView, EventListView, JoinEventView, RegistrationUserView, logout_view
from falcon_events.views import UserLoginView, EventDetailView, CategoryDetailView, MyEventsViews, CancelRegistrationView
from falcon_events.views import ContactView, CalendarView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('events/event_list/', EventListView.as_view(), name='event_list'),
    path('events/event_detail/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/join/<int:pk>/', JoinEventView.as_view(), name='event_join'),
    path('events/my_events/', MyEventsViews.as_view(), name='my_events'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('registration/cancel/<int:pk>/', CancelRegistrationView.as_view(), name='cancel_registration'),

    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    path('register/', RegistrationUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('contact/', ContactView.as_view(), name='contact')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)