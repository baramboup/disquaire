from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from .models import Booking, Contact, Album, Artist

# Register your models here.

# class AdminURLMixin(object):
#     content_type = ContentType.objects.get_for_model(obj.__class__, for_concrete_model=False)
#     def get_admin_url(self, obj):
#         return reverse("admin:store_%s_change" % (content_type.model),args=(obj.id,))
    
   

# admin:{{ store }}_{{ Booking }}_change
# admin:store_booking_change

class BookingInLine(admin.TabularInline):
# class BookingInLine(admin.TabularInline, AdminURLMixin):    
    readonly_fields = ["created_at", "album_link", "contacted"]
    model = Booking
    fieldsets = [
        (None, {'fields': ['album', 'contacted']})
    ]
    extra = 0
    verbose_name = "Reservation"
    verbose_name_plural = "Reservations"

    def has_add_permission(self, request):
        return False 

class AlbumArtistInLine(admin.TabularInline):
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inLines = [BookingInLine, ]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inLines = [AlbumArtistInLine, ]  


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title'] 


@admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
class BookingAdmin(admin.ModelAdmin):    
    readonly_fields = ["created_at", "contact_link", "album_link", "contacted"]
    list_filter = ['created_at', 'contacted'] 

    def has_add_permission(self, request):
        return False   

    def contact_link(self, booking):
        url = self.get_admin_url(booking.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.contact.name))   


    def album_link(self, booking):
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))   