from django.contrib import admin


from users.models import User


@admin.register(User)
class AdminRegisterUser(admin.ModelAdmin):
    list_filter = ('id', 'email')
