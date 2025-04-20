from django.contrib import admin
from .models import (
    AboutModel,
    WhyUsModel,
    TypeModel,
    UserExperienceModel,
    ContactModel,
    SocialMedia,
    ContactMessage
)

class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1 
    readonly_fields = ['icon_preview']

    def icon_preview(self, obj):
        if obj.icon:
            return f'<img src="{obj.icon.url}" width="40" height="40" style="object-fit: contain;" />'
        return ""
    icon_preview.allow_tags = True
    icon_preview.short_description = "Ko‘rinishi"

@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email']
    inlines = [SocialMediaInline]

@admin.register(AboutModel)
class AboutModelAdmin(admin.ModelAdmin):
    list_display = ['description']
    search_fields = ['description']


@admin.register(WhyUsModel)
class WhyUsModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_per_page = 10


@admin.register(TypeModel)
class TypeModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title']
    list_per_page = 10


@admin.register(UserExperienceModel)
class UserExperienceModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    list_per_page = 10


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'phone', 'message']
    readonly_fields = ['created_at']
    list_filter = ['created_at']
    list_per_page = 20
