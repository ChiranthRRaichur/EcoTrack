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
from .utils import get_image_hash, haversine

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
            waste_type = request.POST.get('waste_type', 'General')  # Default to "General" if not provided

            if not all([photo, location, latitude, longitude, waste_type]):
                return HttpResponseRedirect(
                    f"{reverse('submission_status')}?alert_type=danger&message=All+fields+are+required+to+submit+the+report."
                )

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
                return HttpResponseRedirect(
                    f"{reverse('submission_status')}?alert_type=warning&message=This+report+has+already+been+submitted+twice+globally.+Further+duplicates+are+not+allowed."
                )
            elif submission_count == 1:
                points_awarded = 5
                message = f"Duplicate report submitted successfully! You earned {points_awarded} points."
            else:
                points_awarded = 10
                message = f"Report submitted successfully! You earned {points_awarded} points."

            # Create the new report
            WasteReport.objects.create(
                user=request.user,
                photo=photo,
                photo_hash=photo_hash,
                location=location,
                waste_type=waste_type,
                latitude=latitude,
                longitude=longitude
            )

            # Update user points
            request.user.points += points_awarded
            request.user.save()

            # Redirect with success message
            return HttpResponseRedirect(
                f"{reverse('submission_status')}?alert_type=success&message={message.replace(' ', '+')}"
            )

        except Exception as e:
            # Redirect with error message
            return HttpResponseRedirect(
                f"{reverse('submission_status')}?alert_type=danger&message=Error:+{str(e).replace(' ', '+')}"
            )

    # Redirect GET requests to `upload_photo`
    return HttpResponseRedirect(reverse('upload_photo'))


# @login_required
# def submit_report(request):
#     """
#     Handles waste report submission with global duplicate detection and scoring.
#     """
#     if request.method == 'POST':
#         try:
#             photo = request.FILES.get('photo')
#             location = request.POST.get('location')
#             latitude = float(request.POST.get('latitude'))
#             longitude = float(request.POST.get('longitude'))
#             waste_type = request.POST.get('waste_type', 'General')  # Default to "General" if not provided

#             if not all([photo, location, latitude, longitude, waste_type]):
#                 messages.error(request, "All fields are required to submit the report.")
#                 return redirect('submit_report')

#             # Generate hash for the photo
#             photo_hash = get_image_hash(photo)

#             # Track global duplicate submissions
#             duplicate_reports = WasteReport.objects.filter(photo_hash=photo_hash)
#             submission_count = 0

#             for report in duplicate_reports:
#                 distance = haversine(latitude, longitude, report.latitude, report.longitude)
#                 if distance < 20:  # Check proximity within 20 meters
#                     submission_count += 1

#             # Handle response based on global submission count
#             if submission_count >= 2:
#                 messages.warning(request, "This report has already been submitted twice globally. Further duplicates are not allowed.")
#                 return redirect('submit_report')
#             elif submission_count == 1:
#                 points_awarded = 5
#             else:
#                 points_awarded = 10

#             # Create the new report
#             WasteReport.objects.create(
#                 user=request.user,
#                 photo=photo,
#                 photo_hash=photo_hash,
#                 location=location,
#                 waste_type=waste_type,  # Save the waste type
#                 latitude=latitude,
#                 longitude=longitude
#             )

#             # Update user points
#             request.user.points += points_awarded
#             request.user.save()

#             messages.success(request, f"Report submitted successfully! You earned {points_awarded} points.")
#             return redirect('user_history')

#         except Exception as e:
#             messages.error(request, f"Error submitting report: {str(e)}")
#             return redirect('submit_report')

#     return render(request, 'submit_report.html')


from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
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
            waste_type = request.POST.get('waste_type', 'General')  # Default to "General" if not provided
            photo = request.FILES.get('photo')

            if not photo:
                # Redirect with error message
                return HttpResponseRedirect(
                    f"{reverse('submission_status')}?alert_type=danger&message=No+photo+uploaded."
                )

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
                return HttpResponseRedirect(
                    f"{reverse('submission_status')}?alert_type=warning&message=This+report+has+already+been+submitted+twice+globally.+Further+duplicates+are+not+allowed."
                )
            elif submission_count == 1:
                points_awarded = 5
                message = f"Duplicate report submitted successfully! You earned {points_awarded} points."
            else:
                points_awarded = 10
                message = f"Report submitted successfully! You earned {points_awarded} points."

            # Create the new report
            WasteReport.objects.create(
                user=request.user,
                photo=photo,
                photo_hash=photo_hash,
                location=location,
                waste_type=waste_type,
                latitude=latitude,
                longitude=longitude
            )

            # Update user points
            request.user.points += points_awarded
            request.user.save()

            # Redirect with success message
            return HttpResponseRedirect(
                f"{reverse('submission_status')}?alert_type=success&message={message.replace(' ', '+')}"
            )

        except Exception as e:
            # Redirect with error message
            return HttpResponseRedirect(
                f"{reverse('submission_status')}?alert_type=danger&message=Error:+{str(e).replace(' ', '+')}"
            )

    return render(request, 'upload_photo.html')

@login_required
def submission_status(request):
    """
    Renders the submission status page with dynamic messages.
    """
    alert_type = request.GET.get('alert_type', 'info')  # Default to 'info' if not provided
    message = request.GET.get('message', 'No status available.')
    return render(request, 'submission_status.html', {'alert_type': alert_type, 'message': message})


# def add_waste_data():
#     print("Simulating adding data to Hyperledger Fabric...")
#     print("Data added:")

# # Dummy function to query waste data
# def query_waste_data(waste_id):
#     print(f"Simulating querying data for waste ID: {waste_id}")
#     print("Queried data:")

# # Dummy function to detect duplicate reports
# def detect_duplicate_report(new_report):
#     print("Simulating checking for duplicate reports...")
#     existing_reports = [
#         {
#             "id": "1",
#             "location": "Bengaluru",
#             "description": "Overflowing garbage bin",
#             "timestamp": "2024-12-20T15:00:00Z",
#             "reported_by": "User456"
#         }
#     ]

#     for report in existing_reports:
#         if report["location"] == new_report["location"] and report["description"] == new_report["description"]:
#             print("Duplicate report detected:", report)
#             return True

#     print("No duplicate report found.")
#     return False

# # Demonstrate adding, querying, and detecting duplicate waste data
# if __name__ == "__main__":
#     print("Adding data to Hyperledger Fabric...")
#     add_waste_data()

#     print("\nQuerying data from Hyperledger Fabric...")
#     query_waste_data("1")

#     print("\nDetecting duplicate reports...")
#     duplicate_found = detect_duplicate_report()
#     if duplicate_found:
#         print("Duplicate report exists.")
#     else:
#         print("Report is unique.")
