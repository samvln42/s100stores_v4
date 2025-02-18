from django.contrib import admin

from .models import (
    StoreModel,
    OrderModel,
    ReviewModel,
    CategoryModel,
    ImageModel,
    GoodsModel,
    FilteringModel,
    PolicyModel,
    Order,
    OrderItem,
    ProductImage,
    BankAccount,
    Review,
    SizeModel,
    ColorModel,
    WebInfo,
    NoticeModel,
    Stocked,
    StockedImage,
    Mode3D,
    StoreBanner,
)


@admin.register(StoreModel)
class StoreAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = (
        "name",
        "seller",
        "address",
    )

    search_fields = (
        "name",
        "seller",
    )


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = ("name",)

    search_fields = ("name",)


@admin.register(GoodsModel)
class GoodsAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = (
        "category",
        "store",
        "name",
        "price",
    )

    search_fields = ("name", "store")

    list_filter = ("category",)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = ("goods", "price", "user", "ordered_at")

    search_fields = ("user", "goods")


@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("goods", "user", "star")

    search_fields = ("user", "goods")

    list_filter = ("star",)


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = ("goods", "image")

    search_fields = ("goods",)


@admin.register(FilteringModel)
class FilteringModelAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = ("id", "filter", "option")
    list_display_links = ("filter", "option")

    search_fields = ("filtering",)


@admin.register(PolicyModel)
class FilteringModelAdmin(admin.ModelAdmin):
    """Board Admin Definition"""

    list_display = ("id", "category")
    list_display_links = ("category",)

    search_fields = ("category",)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImage)
admin.site.register(BankAccount)
admin.site.register(Review)
admin.site.register(SizeModel)
admin.site.register(ColorModel)
admin.site.register(WebInfo)
admin.site.register(NoticeModel)

@admin.register(Stocked)
class StockedAdmin(admin.ModelAdmin):
    list_display = ['store', 'created_at', 'updated_at']
    list_filter = ['store', 'created_at']
    search_fields = ['store__name']

@admin.register(StockedImage)
class StockedImageAdmin(admin.ModelAdmin):
    list_display = ('stocked', 'position', 'image')
    list_filter = ('position',)
    search_fields = ('stocked__store__name',)
    
@admin.register(Mode3D)
class Mode3DAdmin(admin.ModelAdmin):
    list_display = ('store', 'is_enabled')
    list_filter = ('is_enabled',)
    search_fields = ('store__name',)


@admin.register(StoreBanner)
class StoreBannerAdmin(admin.ModelAdmin):
    list_display = ('store', 'image')
    list_filter = ('store',)
    search_fields = ('store__name',)

