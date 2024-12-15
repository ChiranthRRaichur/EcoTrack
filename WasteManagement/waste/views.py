import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import WasteReport
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.crypto import get_random_string 
from .forms import WasteReportForm
from .models import CustomUser
from admin_app.models import WasteReportStatus

def home(request):
    return render(request, 'base.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')



# class CustomLoginView(LoginView):
#     template_name = 'login.html'

#     def get_success_url(self):
#         return self.request.GET.get('next') or '/'
    

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')  # Redirect to the home page after logout



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Authenticate with email and password
            if user is not None:
                auth_login(request, user)  # Log the user in
                return redirect('home')  # Redirect to the mobile home page
            else:
                form.add_error(None, "Invalid email or password")  # Add an error if authentication fails
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from .models import WasteReport

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import WasteReport

@csrf_exempt
def upload_photo(request):
    if request.method == 'POST':
        try:
            location = request.POST.get('location', 'Unknown Location')
            waste_type = request.POST.get('waste_type', 'General')
            description = request.POST.get('description', '')
            contact_information = request.POST.get('contactInformation', '')
            nearby_landmarks = request.POST.get('nearbyLandmarks', '')
            priority = request.POST.get('priority', 'low')

            # Modify latitude and longitude handling
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            # Convert to float only if the value is not empty or None
            if latitude and latitude.strip():
                try:
                    latitude = float(latitude)
                except ValueError:
                    latitude = None
            else:
                latitude = None

            if longitude and longitude.strip():
                try:
                    longitude = float(longitude)
                except ValueError:
                    longitude = None
            else:
                longitude = None

            # Check if photo is uploaded
            if 'photo' not in request.FILES:
                return JsonResponse({'error': 'No photo uploaded'}, status=400)
            
            photo = request.FILES['photo']  # Get the photo from request

            # Create and save the waste report
            waste_report = WasteReport.objects.create(
                user=request.user,  # Assuming user is logged in
                photo=photo,
                location=location,
                waste_type=waste_type,
                description=description,
                contact_information=contact_information,
                nearby_landmarks=nearby_landmarks,
                priority=priority,
                latitude=latitude,
                longitude=longitude
            )

            return JsonResponse({
                'message': 'Photo uploaded successfully!', 
                'report_id': waste_report.id
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET request - render upload form
    return render(request, 'upload_photo.html')

@login_required
def user_history(request):
    # Fetch the logged-in user
    user = request.user
    
    # Fetch all reports submitted by the user
    reports = WasteReport.objects.filter(user=user)

    # Prepare the history data with status and comments
    history_data = []
    for report in reports:
        try:
            # Get the status and comments from WasteReportStatus
            report_status = WasteReportStatus.objects.get(report=report)
            status = report_status.status
            comments = report_status.comments
        except WasteReportStatus.DoesNotExist:
            # If no status exists, default to "----"
            status = "----"
            comments = "----"

        # Add data to the history_data list
        history_data.append({
            'waste_type': report.waste_type,
            'created_at': report.created_at,
            'status': status,
            'comments': comments
        })

    return render(request, 'userhistory.html', {'history_data': history_data})

def score_board(request):
    users = CustomUser.objects.all().order_by('-points')  # Sort by points (highest first)
    context = {'users': users}
    return render(request, 'score_board.html', context)

def approve_photo(photo_id, approved=True, is_duplicate=False):
    photo = WasteReport.objects.get(id=photo_id)
    user = photo.user
    if approved:
        if is_duplicate:
            user.points += 5  # Award 5 points for duplicate photo
        else:
            user.points += 10  # Award 10 points for unique, valid photo
        user.save()



