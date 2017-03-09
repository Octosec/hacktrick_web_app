from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import Profile, Instructor
from hijack_admin.admin import HijackUserAdminMixin

class ProfileInline(admin.StackedInline):
    model = Instructor
    max_num = 1
    can_delete = True
    min_num = 1

    def get_min_num(self, request, obj=None, **kwargs):
        if obj:
            if obj.user_type == 2:
                return self.min_num
        return None


@admin.register(Profile)
class ProfileAdmin(UserAdmin, HijackUserAdminMixin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'hijack_field')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Extra'), {'fields': ('user_type', 'institution', 'phone_number')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    inlines = [ProfileInline]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'institution']
