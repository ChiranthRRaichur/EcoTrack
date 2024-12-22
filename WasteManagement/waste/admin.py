# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import  CustomUser
# from .models import WasteReport

# # Register the WasteReport model
# class WasteReportAdmin(admin.ModelAdmin):
#     list_display = ('user', 'waste_type', 'location', 'priority', 'created_at')
#     search_fields = ('user__username', 'location', 'waste_type')
#     list_filter = ('waste_type', 'priority')

# # Register the model with the admin site
# admin.site.register(WasteReport, WasteReportAdmin)


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     pass


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WasteReport

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'username', 'points', 'is_staff', 'is_active')
    # Fields to search in the admin search bar
    search_fields = ('email', 'username')
    # Filters for the right-hand sidebar
    list_filter = ('is_staff', 'is_active')

    # Fieldsets for adding/editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'points', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Fields for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    ordering = ('email',)


# Waste Report Admin
@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user', 'waste_type', 'location', 'priority', 'latitude', 'longitude', 'created_at')
    # Fields to search in the admin search bar
    search_fields = ('user__email', 'location', 'waste_type')
    # Filters for the right-hand sidebar
    list_filter = ('waste_type', 'priority', 'created_at')
    # Read-only fields to prevent accidental edits
    readonly_fields = ('created_at',)

    # Custom fieldsets for WasteReport model
    fieldsets = (
        (None, {'fields': ('user', 'photo', 'photo_hash', 'waste_type', 'location', 'priority', 'description')}),
        ('Location Info', {'fields': ('latitude', 'longitude')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )



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
