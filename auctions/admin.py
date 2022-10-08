from django.contrib import admin

from auctions.models import Bid, Listing, Comment, User, Wishlist

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'created_by', 'category')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'wishlist_of')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid_price', 'bid_on', 'bid_by', 'current_highest')

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Wishlist, WishlistAdmin)

