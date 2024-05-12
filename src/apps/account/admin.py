from django.utils.translation import gettext_lazy as _
from django.contrib import admin


from .models import User, VerificationToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ["email"]
    list_display = ["email", "phone_number", "is_verified", "is_staff"]
    list_filter = ["is_staff", "is_active", "is_superuser", "groups"]
    search_fields = ["email", "first_name", "last_name"]
    date_hierarchy = "date_joined"
    readonly_fields = ["id"]

    fieldsets = (
        (None, {"fields": ("id","email")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "avatar")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "is_verified", "groups", "user_permissions")},
        ),
        # (_("Important dates"), {"fields": ("date_joined",)}),
    )
    add_fieldset = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    
    

admin.site.register(VerificationToken)