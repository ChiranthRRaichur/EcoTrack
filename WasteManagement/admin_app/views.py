from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from admin_app.models import WasteReportApproval
from waste.models import WasteReport  # Assuming the WasteReport model contains user-submitted data
from django.contrib import messages
from django.http import HttpResponse


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Ensure that the user is an admin
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
        else:
            messages.error(request, 'Invalid credentials or user not authorized as admin.')
            return redirect('admin_login')
    
    return render(request, 'admin_app/admin_login.html')


 # Fetch reports and include filtering based on approval status if needed
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users to the home page
    reports = WasteReportApproval.objects.all().order_by('-id')
    return render(request, 'admin_app/admin_dashboard.html', {'reports': reports})



def report_detail(request, report_id):
    report_approval = get_object_or_404(WasteReportApproval, id=report_id)
    # Simulating blockchain check (to be replaced with actual logic)
    is_duplicate = False  # Replace this with the logic to check for duplicate using blockchain
    return render(request, 'admin_app/report_detail.html', {
        'report_approval': report_approval,
        'is_duplicate': is_duplicate
    })


@login_required
def approve_report(request, report_id):
    report_approval = get_object_or_404(WasteReportApproval, id=report_id)
    if request.method == 'POST' and request.POST['action'] == 'approve':
        report_approval.status = 'Approved'
        report_approval.points_awarded = 10  # Awarding points after approval
        report_approval.save()
    return redirect('admin_dashboard')  # Redirect back to the dashboard

@login_required
def reject_report(request, report_id):
    report_approval = get_object_or_404(WasteReportApproval, id=report_id)
    if request.method == 'POST' and request.POST['action'] == 'reject':
        report_approval.status = 'Rejected'
        report_approval.save()
    return redirect('admin_dashboard')  # Redirect back to the dashboard
