# admin_app/models.py
from django.db import models
from waste.models import WasteReport  # Import the existing WasteReport model


from django.db import models
from waste.models import WasteReport  # Importing WasteReport from the waste app

class WasteReportStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ]
    
    report = models.ForeignKey(WasteReport, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(null=True, blank=True)  # Admin can add comments here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.report.id} - {self.status}"





# Approval model to track waste report statuses and points
class WasteReportApproval(models.Model):
    report = models.OneToOneField(WasteReport, on_delete=models.CASCADE)  # Linking waste report
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    points_awarded = models.IntegerField(default=0)
    blockchain_verified = models.BooleanField(default=False)  # True if the image is verified as unique by blockchain
    
    def __str__(self):
        return f"{self.report.user.username} - {self.status}"

    def get_report_details(self):
        # Helper method to get the full details of the report
        return f"Location: {self.report.location}, Waste Type: {self.report.waste_type}, Submitted At: {self.report.created_at}"


class WasteReportHistory(models.Model):
    report = models.ForeignKey(WasteReport, on_delete=models.CASCADE)  # Link to the WasteReport
    action_taken = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Rejected', 'Rejected')])
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp when the action is performed
    notes = models.TextField(null=True, blank=True)  # Optional field for notes from the admin

    def __str__(self):
        return f"Status: {self.action_taken} for Report ID: {self.report.id} at {self.timestamp}"


