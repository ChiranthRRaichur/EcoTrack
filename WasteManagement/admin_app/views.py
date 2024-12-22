# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from waste.models import WasteReport  # Importing WasteReport from the waste app
# from django.core.paginator import Paginator
# from .models import WasteReportStatus
# from admin_app import models 
# from django.contrib import messages
# from waste.models import WasteReport, CustomUser
# from waste.utils import sync_user_points
# from django.contrib.auth.decorators import user_passes_test

# def is_admin(user):
#     return user.is_authenticated and user.is_superuser

# # Admin Login
# def admin_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None and user.is_staff:
#             login(request, user)
#             return redirect('admin_dashboard')
#         else:
#             messages.error(request, 'Invalid credentials or user not authorized as admin.')
#             return redirect('admin_login')
    
#     return render(request, 'admin_app/admin_login.html')

# @login_required
# def dashboard(request):
#     if not request.user.is_staff:
#         return redirect('home')

#     query = request.GET.get('q', '')
#     reports_list = WasteReport.objects.filter(
#         user__username__icontains=query
#     ) | WasteReport.objects.filter(
#         waste_type__icontains=query
#     )

#     # Paginate reports (10 per page)
#     paginator = Paginator(reports_list, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Fetch the status for each report using filter (to avoid DoesNotExist error)
#     report_statuses = {}
#     for report in page_obj:
#         try:
#             report_status = WasteReportStatus.objects.filter(report=report).latest('updated_at')
#             report_statuses[report.id] = report_status
#         except WasteReportStatus.DoesNotExist:
#             report_statuses[report.id] = None  # No status found, set it to None

#     return render(request, 'admin_app/admin_dashboard.html', {'page_obj': page_obj, 'report_statuses': report_statuses})



# @login_required
# def update_report_status(request, report_id):
#     if not request.user.is_staff:
#         return redirect('home')
    
#     report = get_object_or_404(WasteReport, id=report_id)
    
#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         comments = request.POST.get('comments', '')  # Optional comments
        
#         if new_status in ['pending', 'in_progress', 'completed', 'rejected']:
#             # Create a new WasteReportStatus
#             WasteReportStatus.objects.create(report=report, status=new_status, comments=comments)
#             messages.success(request, 'Report status updated successfully.')
#         else:
#             messages.error(request, 'Invalid status selected.')
    
#     return redirect('admin_dashboard')




# # Report Details View
# @login_required
# def report_detail(request, report_id):
#     if not request.user.is_staff:
#         return redirect('home')  # Redirect non-admin users to the home page
    
#     # Fetch the report from WasteReport in the waste app
#     report = get_object_or_404(WasteReport, id=report_id)
    
#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         if new_status in ['pending', 'in_progress', 'completed', 'rejected']:
#             report.status = new_status  # Update the status
#             report.save()
#             messages.success(request, f"Report status updated to {new_status.capitalize()}.")
#             return redirect('admin_dashboard')  # Redirect to the dashboard after updating

#     return render(request, 'admin_app/report_detail.html', {'report': report})


# from django.db.models import Count
# from django.shortcuts import render
# from .models import WasteReport


# def analytics_dashboard(request):
#     # User Contributions
#     user_contributions = WasteReport.objects.values('user__username').annotate(contribution_count=Count('id'))

#     # Waste Type Distribution
#     waste_type_distribution = WasteReport.objects.values('waste_type').annotate(count=Count('id'))

#     # Location Data (Latitude and Longitude)
#     location_data = WasteReport.objects.values('latitude', 'longitude', 'user__username', 'waste_type')

#     context = {
#         'user_contributions': list(user_contributions),
#         'waste_type_distribution': list(waste_type_distribution),
#         'location_data': list(location_data),
#     }
#     return render(request, 'admin_app/analytics_dashboard.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from waste.models import WasteReport  # Importing WasteReport from the waste app
from django.core.paginator import Paginator
from .models import WasteReportStatus
from admin_app import models 
from django.contrib import messages
from waste.models import WasteReport, CustomUser
from waste.utils import sync_user_points
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_superuser

# Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or user not authorized as admin.')
            return redirect('admin_login')
    
    return render(request, 'admin_app/admin_login.html')

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    query = request.GET.get('q', '')
    reports_list = WasteReport.objects.filter(
        user__username__icontains=query
    ) | WasteReport.objects.filter(
        waste_type__icontains=query
    )

    # Paginate reports (10 per page)
    paginator = Paginator(reports_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch the status for each report using filter (to avoid DoesNotExist error)
    report_statuses = {}
    for report in page_obj:
        try:
            report_status = WasteReportStatus.objects.filter(report=report).latest('updated_at')
            report_statuses[report.id] = report_status
        except WasteReportStatus.DoesNotExist:
            report_statuses[report.id] = None  # No status found, set it to None

    return render(request, 'admin_app/admin_dashboard.html', {'page_obj': page_obj, 'report_statuses': report_statuses})



@login_required
def update_report_status(request, report_id):
    if not request.user.is_staff:
        return redirect('home')
    
    report = get_object_or_404(WasteReport, id=report_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        comments = request.POST.get('comments', '')  # Optional comments
        
        if new_status in ['pending', 'in_progress', 'completed', 'rejected']:
            # Create a new WasteReportStatus
            WasteReportStatus.objects.create(report=report, status=new_status, comments=comments)
            messages.success(request, 'Report status updated successfully.')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('admin_dashboard')




# Report Details View
@login_required
def report_detail(request, report_id):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users to the home page
    
    # Fetch the report from WasteReport in the waste app
    report = get_object_or_404(WasteReport, id=report_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in_progress', 'completed', 'rejected']:
            report.status = new_status  # Update the status
            report.save()
            messages.success(request, f"Report status updated to {new_status.capitalize()}.")
            return redirect('admin_dashboard')  # Redirect to the dashboard after updating

    return render(request, 'admin_app/report_detail.html', {'report': report})


from django.db.models import Count
from django.shortcuts import render
from .models import WasteReport


# @login_required
# def analytics_dashboard(request):
#     """
#     Analytics dashboard showing insights for waste type distribution and scatter map.
#     """
#     # User Contributions
#     user_contributions = (
#         WasteReport.objects.values('user__username')
#         .annotate(contribution_count=Count('id'))
#         .order_by('-contribution_count')
#     )

#     # Waste Type Distribution
#     waste_type_distribution = (
#         WasteReport.objects.values('waste_type')
#         .annotate(count=Count('id'))
#         .order_by('-count')
#     )

#     # Collect latitudes and longitudes for scatter map
#     location_data = list(
#         WasteReport.objects.values('latitude', 'longitude', 'location', 'waste_type')
#     )

#     context = {
#         'user_contributions': list(user_contributions),
#         'waste_type_distribution': list(waste_type_distribution),
#         'location_data': location_data,
#     }
#     return render(request, 'admin_app/analytics_dashboard.html', context)

def analytics_dashboard(request):
    # User Contributions
    user_contributions = WasteReport.objects.values('user__username').annotate(contribution_count=Count('id'))

    # Waste Type Distribution
    waste_type_distribution = WasteReport.objects.values('waste_type').annotate(count=Count('id'))

    # Location Data (Latitude and Longitude)
    location_data = WasteReport.objects.values('latitude', 'longitude', 'user__username', 'waste_type')

    context = {
        'user_contributions': list(user_contributions),
        'waste_type_distribution': list(waste_type_distribution),
        'location_data': list(location_data),
    }
    return render(request, 'admin_app/analytics_dashboard.html', context)