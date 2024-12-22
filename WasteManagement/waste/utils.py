# waste/utils.py
import math
import imagehash
from PIL import Image
from django.db.models import Count

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

def sync_user_points(user):
    """
    Recalculates and updates user points based on their waste reports.
    """
    # Import here to avoid circular import
    from waste.models import WasteReport
    
    # Get all reports for the user
    user_reports = WasteReport.objects.filter(user=user)
    
    total_points = 0
    processed_hashes = set()
    
    # Group reports by photo_hash and location to properly calculate points
    for report in user_reports.order_by('created_at'):
        if report.photo_hash not in processed_hashes:
            similar_reports = WasteReport.objects.filter(photo_hash=report.photo_hash)
            submission_count = 0
            
            for similar_report in similar_reports:
                if haversine(report.latitude, report.longitude, 
                           similar_report.latitude, similar_report.longitude) < 20:
                    submission_count += 1
                    
            if submission_count == 1:
                total_points += 10  # First submission
            elif submission_count == 2:
                total_points += 5   # Second submission
                
            processed_hashes.add(report.photo_hash)
    
    user.points = total_points
    user.save()
    return total_points