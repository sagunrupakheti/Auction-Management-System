from django.contrib import admin

# Register your models here.
from .models import *
from .models import Item

admin.site.register(draftUser)
admin.site.register(UserProfileInfo)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Drawing)
admin.site.register(Painting)
admin.site.register(PhotographicImage)
admin.site.register(Sculpture)
admin.site.register(Carving)
admin.site.register(Bidding)
admin.site.register(Commission)
admin.site.register(jointAccountRequest)
admin.site.register(Notification)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('item_lot',)

admin.site.register(Item, ItemAdmin)
