from django.contrib import admin

from .models import Speak

# adds a search box the the admin, and displays the username for associated posts
class SpeakAdmin(admin.ModelAdmin):
    list_display =['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Speak


admin.site.register(Speak, SpeakAdmin)
