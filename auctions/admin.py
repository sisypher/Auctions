from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "category", "image", "user")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "comment", "user")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "listing", "user")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)