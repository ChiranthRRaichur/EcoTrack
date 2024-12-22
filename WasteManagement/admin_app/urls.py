from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('report/<int:report_id>/update-status/', views.update_report_status, name='update_report_status'),
    path('analytics-dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
]
