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

# from django.views.decorators.http import require_http_methods
# from django.contrib.auth.decorators import login_required

# @login_required
# @require_http_methods(["GET", "POST"])
# def upload_photo(request):
#     if request.method == 'POST':
#         try:
#             # Extract form data
#             location = request.POST.get('location', 'Unknown Location')
#             waste_type = request.POST.get('waste_type', 'General')
#             description = request.POST.get('description', '')
#             contact_information = request.POST.get('contactInformation', '')
#             nearby_landmarks = request.POST.get('nearbyLandmarks', '')
#             priority = request.POST.get('priority', 'low')
            
#             # Check if photo is uploaded
#             if 'photo' not in request.FILES:
#                 return JsonResponse({'error': 'No photo uploaded'}, status=400)
            
#             photo = request.FILES['photo']

#             # Create and save the waste report
#             waste_report = WasteReport.objects.create(
#                 user=request.user,
#                 photo=photo,
#                 location=location,
#                 waste_type=waste_type,
#                 description=description,
#                 priority=priority,
#                 contact_information=contact_information,
#                 nearby_landmarks=nearby_landmarks,
            
#             )

#             return JsonResponse({
#                 'message': 'Photo uploaded successfully!', 
#                 'report_id': waste_report.id
#             }, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     # GET request - render upload form
#     return render(request, 'upload_photo.html')



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





# from django.db import IntegrityError
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from django.contrib.auth.decorators import login_required
# from .forms import LoginForm, SignupForm
# # from .forms ReportIssueForm, RequestPickupForm,AddImageForm, UpdateIssueForm
# # from .models import WasteIssue, PickupRequest,  WasteReport
# from django.http import HttpRequest
# from django.contrib.auth.views import LoginView

# def home(request):
#     return render(request, 'base.html')

# def about(request):
#     return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')

# #photo click and upload
# def upload_photo(request):
#     return render(request, 'upload_photo.html')


# #photo click and upload
# # @login_required
# # def upload_photo(request):
# #     if request.method == 'POST':
# #         photo = request.FILES.get('photo')
# #         location = request.POST.get('location')
# #         waste_type = request.POST.get('waste_type')

# #         if photo and location and waste_type:
# #             WasteReport.objects.create(
# #                 user=request.user,
# #                 photo=photo,
# #                 location=location,
# #                 waste_type=waste_type
# #             )
# #             return redirect('user_dashboard')  # Redirect to user dashboard after submission

# #     return render(request, 'upload_photo.html')


# # def login(request: HttpRequest):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             print(f"Attempting to authenticate user: {email}") 
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 if user.is_staff:
#                     return redirect('admin_dashboard')
#                 else:
#                     return redirect('user_dashboard')
#             else:
#                 print("Authentication failed")  
#                 form.add_error(None, "Invalid email or password")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# #built in login logic
# class CustomLoginView(LoginView):
#     template_name = 'login.html'

#     def get_success_url(self):
#         return self.request.GET.get('next') or '/'


# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the user
#             return redirect('login')  # Redirect to login page after signup
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})


# # @login_required
# # def report_issue(request):
# #     if request.method == 'POST':
# #         form = ReportIssueForm(request.POST)
# #         if form.is_valid():
# #             try:
# #                 pickup = form.save(commit=False)
# #                 pickup.requested_by = request.user
# #                 pickup.save()
# #                 return redirect('user_dashboard')
# #             except IntegrityError as e:
# #                 form.add_error(None, "An error occurred: Foreign key constraint failed.")
# #                 print(f"IntegrityError: {e}")
# #     else:
# #         form = ReportIssueForm()
# #     return render(request, 'user/report_issue.html', {'form': form})

# # @login_required
# # def request_pickup(request):
# #     if request.method == 'POST':
# #         form = RequestPickupForm(request.POST)
# #         if form.is_valid():
# #             try:
# #                 pickup = form.save(commit=False)
# #                 pickup.requested_by = request.user
# #                 pickup.save()
# #                 return redirect('user_dashboard')
# #             except IntegrityError as e:
# #                 form.add_error(None, "An error occurred: Foreign key constraint failed.")
# #                 print(f"IntegrityError: {e}")
# #     else:
# #         form = RequestPickupForm()
# #     return render(request, 'user/request_pickup.html', {'form': form})

# # @login_required
# # def user_dashboard(request):
# #     user = request.user
# #     issues = WasteIssue.objects.filter(reported_by=user)
# #     pickups = PickupRequest.objects.filter(requested_by=user)
# #     return render(request, 'user/user_dashboard.html', {'issues': issues, 'pickups': pickups})

# @login_required
# def admin_dashboard(request):
#     if not request.user.is_staff:
#         return redirect('login')  
#     # issues = WasteIssue.objects.all()
#     # pickups = PickupRequest.objects.all()
#     return render(request, 'admin/admin_dashboard.html', {'issues': issues, 'pickups': pickups})

# @login_required
# def admin_update_issue(request, issue_id):
#     if not request.user.is_staff:
#         return redirect('login')

#     issue = get_object_or_404(WasteIssue, id=issue_id)

#     if request.method == 'POST':
#         form = UpdateIssueForm(request.POST, instance=issue)
#         if form.is_valid():
#             form.save()  # Save the form data, which updates the issue instance
#             return redirect('admin_dashboard')  # Redirect to admin dashboard after successful update
#     else:
#         form = UpdateIssueForm(instance=issue)

#     return render(request, 'admin/admin_update_issue.html', {'form': form, 'issue': issue})

# # @login_required
# # def admin_update_pickup(request, pickup_id):
# #     if not request.user.is_staff:
# #         return redirect('login')  
# #     pickup = PickupRequest.objects.get(id=pickup_id)
# #     if request.method == 'POST':
       
# #         return redirect('admin_dashboard')
# #     return render(request, 'admin/admin_update_pickup.html', {'pickup': pickup})
# # def add_image(request):
# #     if request.method == 'POST':
# #         form = AddImageForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('user_dashboard')
# #     else:
# #         form = AddImageForm()
# #     return render(request, 'user/add_image.html', {'form': form})

# def logout_view(request):
#     auth_logout(request)
#     return redirect('home')
