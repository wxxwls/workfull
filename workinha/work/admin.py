from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Post, qna, InjuryApplication

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('id', 'email', 'username', 'birth_date', 'gender', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'gender')
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal Info', {'fields': ('username',  'birth_date', 'gender', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'username', 'birth_date', 'gender', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('id', 'email', 'username')
    ordering = ('id',)




admin.site.register(MyUser, MyUserAdmin)

admin.site.register(Post)
admin.site.register(qna)
admin.site.register(InjuryApplication)
