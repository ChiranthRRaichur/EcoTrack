from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # Use your custom login view
    path('logout/', views.logout_view, name='logout'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('score-board/', views.score_board, name='score_board'),
    path('user-history/', views.user_history, name='user_history'),
    path('submit-report/', views.submit_report, name='submit_report'),
    path('submission-status/', views.submission_status, name='submission_status'),
]




# from django.contrib.auth.views import LoginView
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('about/', views.about, name='about'),
#     path('contact/', views.contact, name='contact'),
#    path('signup/', views.signup, name='signup'),
#     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
#     # path('report-issue/', views.report_issue, name='report_issue'),
#     # path('request-pickup/', views.request_pickup, name='request_pickup'),
#     # path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
#     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     # path('admin-update-issue/<int:issue_id>/', views.admin_update_issue, name='admin_update_issue'),
#     # path('admin-update-pickup/<int:pickup_id>/', views.admin_update_pickup, name='admin_update_pickup'),
#     path('logout/', views.logout_view, name='logout'),
#     # path('add-image/', views.add_image, name='add_image'),
#     path('upload-photo/', views.upload_photo, name='upload_photo'),
#       path('login/', LoginView.as_view(template_name='login.html'), name='login'),
# ]
