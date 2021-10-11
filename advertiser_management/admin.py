from django.contrib import admin

from advertiser_management.models import Ad

# admin.site.register(Ad)
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'Title', 'Link', 'Approve']
    search_fields = ['Title']
    list_filter = ['Approve']