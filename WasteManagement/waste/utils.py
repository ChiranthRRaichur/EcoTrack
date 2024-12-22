# waste/utils.py
from waste.models import WasteReport
from waste.views import haversine


def sync_user_points(user):
    """
    Recalculates and updates user points based on their waste reports.
    """
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