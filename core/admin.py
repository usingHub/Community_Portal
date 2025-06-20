from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Request, Offer, Category


# Optional: Customize admin display for Request and Offer
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'category', 'location')
    search_fields = ('title', 'description', 'location', 'user__username')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'category', 'location')
    search_fields = ('title', 'description', 'location', 'user__username')


# Register everything
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Category)
