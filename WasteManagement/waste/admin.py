from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  CustomUser
from .models import WasteReport

# Register the WasteReport model
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'waste_type', 'location', 'priority', 'created_at')
    search_fields = ('user__username', 'location', 'waste_type')
    list_filter = ('waste_type', 'priority')

# Register the model with the admin site
admin.site.register(WasteReport, WasteReportAdmin)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


# from django.contrib import admin
# from .models import ReportSubmission  # Import the ReportSubmission model

# # Register the ReportSubmission model
# @admin.register(ReportSubmission)
# class ReportSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'report', 'hash_value', 'submission_count')  # Fields to display in the list view
#     search_fields = ('user__username', 'report__location')  # Fields to search in the admin interface
#     list_filter = ('submission_count',)  # Allows filtering based on submission_count

#     # Optional: Add additional customizations to the admin interface
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Example: You could filter the queryset based on some condition (e.g., only submissions with more than 1 submission)
#         return queryset.filter(submission_count__gt=1)
