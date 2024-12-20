import hashlib
import math
from PIL import Image
import imagehash
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, SignupForm
from .models import WasteReport, CustomUser
from admin_app.models import WasteReportStatus


# Utility Functions
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth.
    """
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c * 1000  # Convert to meters


def get_image_hash(image_file):
    """
    Generate a hash for the given image using perceptual hashing.
    """
    image = Image.open(image_file)
    return str(imagehash.phash(image))


# Views
def home(request):
    return render(request, 'base.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def signup(request):
    """
    Handles user registration using the SignupForm.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Ensure the user is active
            user.is_staff = False  # Regular users should not have staff privileges
            user.set_password(form.cleaned_data['password1'])  # Set hashed password
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """
    Handles user login using the LoginForm.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Authenticate with email and password
            if user is not None:
                auth_login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home page
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """
    Handles user logout and redirects to the home page.
    """
    auth_logout(request)
    return redirect('home')



@login_required
def user_history(request):
    """
    Displays the logged-in user's report submission history.
    """
    user = request.user
    reports = WasteReport.objects.filter(user=user)

    history_data = []
    for report in reports:
        try:
            # Get status and comments
            report_status = WasteReportStatus.objects.get(report=report)
            status = report_status.status
            comments = report_status.comments
        except WasteReportStatus.DoesNotExist:
            status = "----"
            comments = "----"

        history_data.append({
            'waste_type': report.waste_type,
            'created_at': report.created_at,
            'status': status,
            'comments': comments
        })

    return render(request, 'userhistory.html', {'history_data': history_data})


@login_required
def score_board(request):
    """
    Displays the leaderboard of users sorted by points.
    """
    users = CustomUser.objects.all().order_by('-points')
    return render(request, 'score_board.html', {'users': users})


# @csrf_exempt
# def upload_photo(request):
#     """
#     Handles photo uploads for waste reports, including duplicate detection and point calculation.
#     """
#     if request.method == 'POST':
#         try:
#             location = request.POST.get('location', 'Unknown Location')
#             latitude = float(request.POST.get('latitude'))
#             longitude = float(request.POST.get('longitude'))
#             photo = request.FILES.get('photo')

#             if not photo:
#                 return JsonResponse({'error': 'No photo uploaded'}, status=400)

#             # Generate hash for the uploaded photo
#             photo_hash = get_image_hash(photo)

#             # Variables to track duplicates and points
#             is_duplicate = False
#             points_awarded = 10  # Default points for a unique report

#             for report in WasteReport.objects.all():
#                 existing_photo_hash = get_image_hash(report.photo)
#                 if photo_hash == existing_photo_hash:
#                     distance = haversine(latitude, longitude, report.latitude, report.longitude)
#                     if distance < 20:  # Within 20 meters
#                         is_duplicate = True
#                         points_awarded = 5  # Points for duplicate report
#                         break

#             # Save the new report
#             report = WasteReport.objects.create(
#                 user=request.user,
#                 photo=photo,
#                 photo_hash=photo_hash,
#                 location=location,
#                 latitude=latitude,
#                 longitude=longitude
#             )

#             # Update user points
#             request.user.points += points_awarded
#             request.user.save()

#             # Return a JSON response with points awarded and total points
#             return JsonResponse({
#                 'message': f'Photo uploaded successfully! You earned {points_awarded} points.',
#                 'total_points': request.user.points
#             }, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     elif request.method == 'GET':
#         # Render a basic upload form for testing
#         return render(request, 'upload_photo.html')

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def upload_photo(request):
    """
    Handles photo uploads for waste reports, including global duplicate detection and point calculation.
    """
    if request.method == 'POST':
        try:
            location = request.POST.get('location', 'Unknown Location')
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
            photo = request.FILES.get('photo')

            if not photo:
                return JsonResponse({'error': 'No photo uploaded'}, status=400)

            # Generate hash for the uploaded photo
            photo_hash = get_image_hash(photo)

            # Track global duplicate submissions
            duplicate_reports = WasteReport.objects.filter(photo_hash=photo_hash)
            submission_count = 0

            for report in duplicate_reports:
                distance = haversine(latitude, longitude, report.latitude, report.longitude)
                if distance < 20:  # Check proximity within 20 meters
                    submission_count += 1

            # Handle response based on global submission count
            if submission_count >= 2:
                return JsonResponse({
                    'message': 'This report has already been submitted twice globally. Further duplicates are not allowed.'
                }, status=400)
            elif submission_count == 1:
                points_awarded = 5
            else:
                points_awarded = 10

            # Create the new report
            WasteReport.objects.create(
                user=request.user,
                photo=photo,
                photo_hash=photo_hash,
                location=location,
                latitude=latitude,
                longitude=longitude
            )

            # Update user points
            request.user.points += points_awarded
            request.user.save()

            return JsonResponse({
                'message': f'Report submitted successfully! You earned {points_awarded} points.',
                'total_points': request.user.points
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        return render(request, 'upload_photo.html')

    return JsonResponse({'error': 'Invalid request method'}, status=405)
@login_required
def submit_report(request):
    """
    Handles waste report submission with global duplicate detection and scoring.
    """
    if request.method == 'POST':
        try:
            photo = request.FILES.get('photo')
            location = request.POST.get('location')
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))

            if not all([photo, location, latitude, longitude]):
                messages.error(request, "All fields are required to submit the report.")
                return redirect('submit_report')

            # Generate hash for the photo
            photo_hash = get_image_hash(photo)

            # Track global duplicate submissions
            duplicate_reports = WasteReport.objects.filter(photo_hash=photo_hash)
            submission_count = 0

            for report in duplicate_reports:
                distance = haversine(latitude, longitude, report.latitude, report.longitude)
                if distance < 20:  # Check proximity within 20 meters
                    submission_count += 1

            # Handle response based on global submission count
            if submission_count >= 2:
                messages.warning(request, "This report has already been submitted twice globally. Further duplicates are not allowed.")
                return redirect('submit_report')
            elif submission_count == 1:
                points_awarded = 5
            else:
                points_awarded = 10

            # Create the new report
            WasteReport.objects.create(
                user=request.user,
                photo=photo,
                photo_hash=photo_hash,
                location=location,
                latitude=latitude,
                longitude=longitude
            )

            # Update user points
            request.user.points += points_awarded
            request.user.save()

            messages.success(request, f"Report submitted successfully! You earned {points_awarded} points.")
            return redirect('user_history')

        except Exception as e:
            messages.error(request, f"Error submitting report: {str(e)}")
            return redirect('submit_report')

    return render(request, 'submit_report.html')
