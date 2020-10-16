from .models import Post, Community, Profile, Comment, Stock, Share

from django.contrib import admin

# Register your models here.
class CommunityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class ShareInLine(admin.TabularInline):
    model = Share
    extra = 1

class StockAdmin(admin.ModelAdmin):
    inlines = [
        ShareInLine
    ]

admin.site.register(Post)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Stock, StockAdmin)