
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("units/<int:id>/", views.unit, name="units"),
    path("courses/<int:id>/", views.course, name="courses"),
    path("departments/", views.department, name="departments"),
    path("documents/<int:id>/", views.document, name="documents"),
    path('contrib/user-login/', views.user_login, name='user-login'),
    path('contrib/user-register/', views.user_register, name='user-register'),
    path('contrib/user-logout/', views.user_logout, name='user-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contrib/courses/<int:id>/', views.user_courses, name='user-courses'),
    path('contact', views.contact, name='contact')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)