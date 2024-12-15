# admin_app/admin.py
from django.contrib import admin
from .models import WasteReportApproval, WasteReportHistory

# Register the WasteReportApproval model with custom display options
class WasteReportApprovalAdmin(admin.ModelAdmin):
    list_display = ('report', 'status', 'points_awarded', 'blockchain_verified', 'user_email')
    list_filter = ('status', 'blockchain_verified')
    search_fields = ('report__user__username', 'report__location', 'report__waste_type')

    def user_email(self, obj):
        return obj.report.user.email
    user_email.short_description = 'User Email'

# Register the WasteReportHistory model with custom display options
class WasteReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('report', 'action_taken', 'timestamp', 'notes', 'user_email')
    list_filter = ('action_taken',)
    search_fields = ('report__report__user__username', 'action_taken', 'notes')

    def user_email(self, obj):
        return obj.report.report.user.email
    user_email.short_description = 'User Email'

# Register the models with the admin site
admin.site.register(WasteReportApproval, WasteReportApprovalAdmin)
admin.site.register(WasteReportHistory, WasteReportHistoryAdmin)


from .models import WasteReportStatus

class WasteReportStatusAdmin(admin.ModelAdmin):
    list_display = ('report', 'status', 'comments', 'updated_at')
    search_fields = ('report__user__username', 'status', 'comments')
    list_filter = ('status',)
    ordering = ('-updated_at',)

# Register the WasteReportStatus model
admin.site.register(WasteReportStatus, WasteReportStatusAdmin)
