from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from uno import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('<str:instance>/detect', views.detect, name='detect'),
    path('<str:instance>/alert', views.alert_list, name='alert'),
    path('<str:instance>/relief', views.relief_page, name='relief'),
    path('<str:instance>/feedback', views.feedback_list, name='feedback'),
    path('support', TemplateView.as_view(template_name='support.html'), name='support'),

    path('get_coordinates', views.get_coordinates, name='get_coordinates'),
    path('send_alert', views.send_alert, name='send_alert'),
    path('<str:instance>/route', views.route_solve, name='routesolve'),
    path('<str:instance>/video_feed/<int:vid>/', views.video_feed, name='video_feed'),
    path('check_video_status', views.check_video_status, name='check_video_status'),
    path('check_covid_status', views.check_covid_status, name='check_covid_status'),
    path('check_fire_status', views.check_fire_status, name='check_fire_status'),
]
