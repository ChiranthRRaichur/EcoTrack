from django.contrib import admin
from .models import WasteReportApproval, WasteReportHistory
from django.contrib import admin
from .models import WasteReport

class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'waste_type', 'location', 'priority', 'contact_information', 'nearby_landmarks', 'created_at')
    search_fields = ('user__username', 'location', 'waste_type', 'contact_information', 'nearby_landmarks')
    list_filter = ('waste_type', 'priority')


# Register the WasteReportApproval model
class WasteReportApprovalAdmin(admin.ModelAdmin):
    list_display = ('report', 'status', 'points_awarded', 'blockchain_verified', 'user_email')
    list_filter = ('status', 'blockchain_verified')
    search_fields = ('report__user__username', 'report__location', 'report__waste_type')

    def user_email(self, obj):
        return obj.report.user.email
    user_email.short_description = 'User Email'

class WasteReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('report', 'action_taken', 'timestamp', 'notes', 'user_email')
    list_filter = ('action_taken',)
    search_fields = ('report__report__user__username', 'action_taken', 'notes')

    def user_email(self, obj):
        return obj.report.report.user.email
    user_email.short_description = 'User Email'



# Register the WasteReport model with custom admin
admin.site.register(WasteReport, WasteReportAdmin)
# Register the models with the admin site
admin.site.register(WasteReportApproval, WasteReportApprovalAdmin)
admin.site.register(WasteReportHistory, WasteReportHistoryAdmin)
