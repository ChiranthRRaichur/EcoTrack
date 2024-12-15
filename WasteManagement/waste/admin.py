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