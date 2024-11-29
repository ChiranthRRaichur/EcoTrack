from django.db import models
from django.conf import settings
from waste.models import WasteReport  # Importing WasteReport from the waste app

# Approval model to track waste report statuses and points
class WasteReportApproval(models.Model):
    report = models.OneToOneField(WasteReport, on_delete=models.CASCADE)  # Linking waste report
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    points_awarded = models.IntegerField(default=0)
    blockchain_verified = models.BooleanField(default=False)  # True if the image is verified as unique by blockchain
    # submitted_at = models.DateTimeField(auto_now_add=True)  # To store the submission timestamp
    
    def __str__(self):
        return f"{self.report.user.username} - {self.status}"

    def get_report_details(self):
        # Helper method to get the full details of the report, can be used in admin dashboard view
        return f"Location: {self.report.location}, Waste Type: {self.report.waste_type}, Submitted At: {self.submitted_at}"

# Optionally, you could also add a model for tracking the review and history of reports.
class WasteReportHistory(models.Model):
    report = models.ForeignKey(WasteReportApproval, on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=50, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('In Progress', 'In Progress')])
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to the current time
    
    def __str__(self):
        return f"{self.report.report.user.username} - {self.action_taken} on {self.timestamp}"
