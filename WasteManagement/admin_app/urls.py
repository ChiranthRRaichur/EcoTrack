from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),  # Custom login page
    path('admin-dashboard/', views.dashboard, name='admin_dashboard'),  # Dashboard after login
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),  # View individual reports
]
