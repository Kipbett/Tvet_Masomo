
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
    path('contrib/dashboard/', views.dashboard, name='dashboard'),
    path('contrib/courses/<int:id>/', views.user_courses, name='user-courses'),
    path('contrib/units/<int:id>/', views.user_units, name='user-units'),
    path('contrib/documents/<int:id>/', views.user_resources, name='user-documents'),
    path('contrib/add-course/', views.add_course, name='add-course'),
    path('contrib/add-unit/<int:id>/', views.add_unit, name='add-unit'),
    path('contrib/add-document/<int:id>', views.add_document, name='add-document'),
    path('tvet-ai/', views.ai_home, name='tvet-ai'),
    path('learning-plan/', views.selection_view, name='learning-plan'),
    path('session-plan/', views.session_plan, name='session-plan'),
    path('ajax/get-courses/', views.get_courses, name='get_courses'),
    path('ajax/get-units/', views.get_units, name='get_units'),
    path('ajax/get-documents/', views.get_documents, name='get_documents'),
    # path('api/check-stk-status/', views.check_stk_status, name='check-stk-status-api'),
    path("callback/", views.process_stk_callback, name="stk-callback"),
    path('payment-wait/', views.payment_wait, name='payment-wait'),
    path('check-transaction-status/', views.check_transaction_status, name='check-transaction-status'),
    path('contact', views.contact, name='contact'),
    path('ai/forms/', views.upload_form, name='ai'),
    path("results/", views.show_results, name="show_results"),
    
    path("upload-and-start/", views.upload_and_start, name="upload_and_start"),
    path("check-task-status/<str:task_id>/", views.check_task_status, name="check_task_status"),
    path("download/<str:filename>/", views.download_file, name="download_file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)