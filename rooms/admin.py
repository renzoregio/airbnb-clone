from django.contrib import admin
from django.utils.html import mark_safe
from . import models
from reviews import models as review_models


@admin.register(models.RoomType, models.Facility, models.HouseRule, models.Amenity)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):
    model = models.Photo


class ReviewInline(admin.TabularInline):
    model = review_models.Review


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = [PhotoInline, ReviewInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        (
            "Check-in and Check-out Time",
            {
                "fields": ("check_in", "check_out", "instant_book"),
            },
        ),
        (
            "Spaces",
            {
                "classes": ("collapse",),
                "fields": (
                    "guests",
                    "beds",
                    "baths",
                    "bedrooms",
                ),
            },
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Final Details", {"classes": ("collapse",), "fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "host__superhost",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "city",
        "country",
    )

    search_fields = ["^city", "^host__username", "^country"]

    filter_horizontal = ["amenities", "facilities", "house_rules"]

    raw_id_fields = ("host",)

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Number of Amenities"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Number of Photos"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Model Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width=50px height=50px src={obj.file.url}/>")

    get_thumbnail.short_description = "Thumbnail"
