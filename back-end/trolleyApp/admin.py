from django.contrib import admin
from .models import User, Trolly, Occupied_trollies
from django import forms

# Register your models here.

class UserForm(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'user_type']
    get_readonly_fields = ['username', 'email', 'phone_number', 'user_type', 'hashed_password', 'salt']


class TrollyForm(admin.ModelAdmin):
    list_display = ['trolley_id','x', 'y', 'isOccupied', 'last_update']
    # readonly_fields = ['isOccupied', 'last_update']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('trolley_id','isOccupied', 'last_update')
        return self.readonly_fields

class OccupiedForm(admin.ModelAdmin):
    list_display = ['occupied_id','user', 'trolly']
    # readonly_fields = ['occupied_id','user', 'trolly']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('occupied_id','user', 'trolly')
        return self.readonly_fields

admin.site.register(User, UserForm)
admin.site.register(Trolly, TrollyForm)
admin.site.register(Occupied_trollies, OccupiedForm) 