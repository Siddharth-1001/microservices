from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "is_admin", "last_login", "created_at", "updated_at")
    list_filter = (
        "email",
        "is_admin",
        "last_login",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password", "user_hash")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "phone_number",
                    "gender",
                    "date_of_birth",
                    "blood_group"
                )
            },
        ),
        ("Geolocation info", {"fields": ("city", "state", "country", "ip_address")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_admin",
                    "is_staff",
                    "is_student",
                    "is_parent",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "is_admin", "last_login", "created_at", "updated_at")
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(CustomUser, UserModelAdmin)
