from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('videos', views.Videos, basename='videos')
urlpatterns = [
   path('job/',views.job),
   path('update_status/',views.Status.as_view()),
] + router.urls