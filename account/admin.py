from django.contrib import admin
from account.models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role')
    search_fields = ('email', 'user_id')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Chapter)
admin.site.register(MuxData)
admin.site.register(UserProgress)
admin.site.register(Purchase)
admin.site.register(StripeCustomer)
admin.site.register(Logging)