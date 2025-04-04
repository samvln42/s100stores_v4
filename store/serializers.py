import math
import uuid
import base64
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.files.base import ContentFile
from django.db import models

from store.models import (
    StoreModel,
    GoodsModel,
    ReviewModel,
    OrderModel,
    ImageModel,
    SizeModel,
    ColorModel,
    CategoryModel,
    ProductImage,
    Order,
    OrderItem,
    BankAccount,
    Review,
    WebInfo,
    NoticeModel,
    Stocked,
    StockedImage,
    StoreBanner,
    Mode3D,
    Mode3DImage,
)
from users.models import UserModel

from users.serializers import UserSerializer


def format_with_commas(n):
    return "{:,}".format(int(n))


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("id", "name", "image")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class GoodsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    store_name = serializers.CharField(source='store.name')
    store_address = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_store_address(self, obj):
        return obj.store.address if obj.store else None

    def get_sizes(self, obj):
        return [size.name for size in obj.size.all()]

    def get_colors(self, obj):
        return [color.name for color in obj.color.all()]

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None

    class Meta:
        model = GoodsModel
        fields = [
            'id', 'store', 'store_name', 'store_address', 'category',
            'name', 'price', 'description', 'x_axis', 'y_axis',
            'sizes', 'colors', 'image', 'created_at', 'updated_at'
        ]


class UpdateStoreSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        name = attrs.get("name")
        if name:
            if len(name) > 15:
                raise ValidationError(
                    "Please write your store name in 15 characters or less."
                )
        return attrs

    class Meta:
        model = StoreModel
        fields = "__all__"
        extra_kwargs = {
            "seller": {"required": False},
        }


class OnlyStoreInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        exclude = ["seller"]


class StoreSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField()
    seller = UserSerializer()

    def get_seller(self, obj):
        return obj.seller.email

    def get_goods_set(self, obj):
        goods = GoodsModel.objects.filter(store_id=obj.id)
        return GoodsSerializer(goods, many=True).data

    class Meta:
        model = StoreModel
        fields = "__all__"


# old review
# class ReviewSerializer(serializers.ModelSerializer):
#     profile_image = serializers.SerializerMethodField()
#     created_at = serializers.SerializerMethodField()
#     nickname = serializers.SerializerMethodField()

#     def validate(self, attrs):
#         review = attrs.get("review")
#         if review:
#             if len(review) < 10:
#                 raise ValidationError("Please register your review with at least 10 characters.")
#         return attrs

#     def get_profile_image(self, obj):
#         user = UserModel.objects.get(id=obj.user.id)
#         if not user.profile_image:
#             return None
#         else:
#             return user.profile_image.url

#     def get_created_at(self, obj):
#         return obj.created_at.strftime("%Y.%m.%d")

#     def get_nickname(self, obj):
#         return obj.user.nickname

#     class Meta:
#         # model = ReviewModel
#         model = Review
#         exclude = ["updated_at", "product"]
#         extra_kwargs = {
#             "user": {"required": False},
#             "product": {"required": False},
#         }


# new review
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Review
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class GoodsDetailSerializer(serializers.ModelSerializer):
    """
    Replace store with name
    Create a review set for the product
    """

    store_name = serializers.SerializerMethodField()
    store_user_id = serializers.SerializerMethodField()
    review_set = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    image_set = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    format_price = serializers.SerializerMethodField()
    star_avg = serializers.SerializerMethodField()
    store_image = serializers.SerializerMethodField()
    store_id = serializers.SerializerMethodField()

    def get_store_name(self, obj):
        return obj.store.name

    def get_store_id(self, obj):
        return obj.store.id

    def get_review_set(self, obj):
        # review = ReviewModel.objects.filter(goods_id=obj.id).order_by("-created_at")
        review = Review.objects.filter(product_id=obj.id).order_by("-created_at")
        serializer = ReviewSerializer(review, many=True)
        return serializer.data

    def get_category(self, obj):
        return obj.category.name

    def get_sizes(self, obj):
        sizes = SizeModel.objects.filter(product=obj)
        serializer = SizeSerializer(sizes, many=True)
        return serializer.data

    def get_colors(self, obj):
        colors = ColorModel.objects.filter(product=obj)
        serializer = ColorSerializer(colors, many=True)
        return serializer.data

    def get_image_set(self, obj):
        images = ProductImage.objects.filter(product_id=obj.id)
        serializer = ProductImageSerializer(images, many=True)
        image_set = [i["image"] for i in serializer.data]
        return image_set

    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj).first()
        serializer = ProductImageSerializer(images)
        images = serializer.data.get("image")
        return images

    def get_address(self, obj):
        address = obj.store.address
        # address = obj.store.address.split(' ')[:2]
        # address = ' '.join(address)
        return address

    def get_store_user_id(self, obj):
        return obj.store.seller.id

    # def get_price(self, obj):
    #     return str(format_with_commas(obj.price))

    def get_price(self, obj):
        return obj.price

    def get_store_image(self, obj):
        return (
            obj.store.seller.profile_image.url
            if obj.store.seller.profile_image
            else False
        )

    def get_star_avg(self, obj):
        review = Review.objects.filter(product_id=obj.id).values("rating")
        total = 0
        for i in review:
            total += i["rating"]

        return math.ceil(total / review.count()) if total != 0 else 0

    def get_format_price(self, obj):
        return str(format_with_commas(obj.price))

    class Meta:
        model = GoodsModel
        exclude = ["created_at", "updated_at"]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"
        extra_kwargs = {
            "goods": {"required": False},
        }

# Order
class OrderItemSerializer(serializers.ModelSerializer):
    product = GoodsSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "color", "size"]


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    user = UserSerializer()

    def get_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "tel",
            "total_prices",
            "account_name",
            "province",
            "district",
            "shipping_company",
            "branch",
            "created_at",
            "status",
            "items",
            "china_url",
            "lao_url",
            "order_bill",
        ]


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "color", "size"]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    def create(self, validated_data):
        order_items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "tel",
            "total_prices",
            "account_name",
            "province",
            "district",
            "shipping_company",
            "branch",
            "created_at",
            "status",
            "items",
        ]


class PendingOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "tel",
            "total_prices",
            "account_name",
            "province",
            "district",
            "shipping_company",
            "branch",
            "created_at",
            "status",
            "items",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.status != "Pending":
            return None  # Skip orders that are not pending
        return data


class ProcessingOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "tel",
            "total_prices",
            "account_name",
            "province",
            "district",
            "shipping_company",
            "branch",
            "created_at",
            "status",
            "items",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.status != "Processing":
            return None  # Skip orders that are not processing
        return data


class DeliveredOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "tel",
            "total_prices",
            "account_name",
            "province",
            "district",
            "shipping_company",
            "branch",
            "created_at",
            "status",
            "items",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.status != "Delivered":
            return None  # Skip orders that are not Delivered
        return data


class ShippedOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "tel",
            "total_prices",
            "account_name",
            "province",
            "district",
            "shipping_company",
            "branch",
            "created_at",
            "status",
            "items",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.status != "Shipped":
            return None  # Skip orders that are not Shipped
        return data


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "color", "size"]


class OrderUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Update order fields
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        return instance

    class Meta:
        model = Order
        fields = ["status"]


class OrderUpdateChinaUrlSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Update order fields
        instance.china_url = validated_data.get("china_url", instance.china_url)
        instance.save()

        return instance

    class Meta:
        model = Order
        fields = ["china_url"]


class OrderUpdateLaoUrlSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Update order fields
        instance.lao_url = validated_data.get("lao_url", instance.lao_url)
        instance.save()

        return instance

    class Meta:
        model = Order
        fields = ["lao_url"]


class OrderUpdateBillSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Update order fields
        instance.order_bill = validated_data.get("order_bill", instance.order_bill)
        instance.save()

        return instance

    class Meta:
        model = Order
        fields = ["order_bill"]


class PostSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="product name")
    price = serializers.IntegerField(help_text="product price")

    review = serializers.CharField(help_text="Review contents")

    search = serializers.CharField(help_text="What to search for")

    goods_id = serializers.IntegerField(help_text="Product ID to order")


class OnlyStoreGoodsSerializer(serializers.ModelSerializer):
    """
    Replace store with name
    Create a review set for the product
    """

    review_set = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()
    order_set = serializers.SerializerMethodField()
    goods_id = serializers.SerializerMethodField()
    image_set = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    format_price = serializers.SerializerMethodField()
    star_avg = serializers.SerializerMethodField()
    x_axis = serializers.ListField(child=serializers.FloatField(), required=False)
    y_axis = serializers.ListField(child=serializers.FloatField(), required=False)

    def get_store(self, obj):
        return obj.store.name

    def get_review_set(self, obj):
        # review = ReviewModel.objects.filter(goods_id=obj.id).order_by("-created_at")
        review = Review.objects.filter(product_id=obj.id).order_by("-created_at")
        serializer = OnlyStoreReviewSerializer(review, many=True)
        return serializer.data

    # def get_category(self, obj):
    #     return obj.category.name

    def get_order_set(self, obj):
        order = OrderModel.objects.filter(goods_id=obj.id).order_by("-ordered_at")
        serializer = OrderSerializer(order, many=True)
        return serializer.data

    def get_goods_id(self, obj):
        return obj.id

    def get_image_set(self, obj):
        images = ProductImage.objects.filter(product_id=obj.id)
        serializer = ProductImageSerializer(images, many=True)
        image_set = [i["image"] for i in serializer.data]
        return image_set

    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj).first()
        serializer = ProductImageSerializer(images)
        images = serializer.data.get("image")
        return images

    def get_format_price(self, obj):
        return str(format_with_commas(obj.price))

    def get_star_avg(self, obj):
        review = Review.objects.filter(product_id=obj.id).values("rating")
        total = 0
        for i in review:
            total += i["rating"]

        return math.ceil(total / review.count()) if total != 0 else 0

    class Meta:
        model = GoodsModel
        fields = [
            "star_avg",
            "goods_id", 
            "review_set",
            "category",
            "order_set",
            "name",
            "price",
            "format_price",
            "image_set",
            "images",
            "description",
            "x_axis",
            "y_axis"
        ]


class OnlyStoreReviewSerializer(serializers.ModelSerializer):
    review_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    goods_id = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    user_profile = serializers.SerializerMethodField()

    def get_review_id(self, obj):
        return obj.id

    def get_user_name(self, obj):
        return obj.user.nickname

    def get_goods_id(self, obj):
        return obj.id

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y.%m.%d")

    def get_user_profile(self, obj):
        return obj.user.profile_image.url if obj.user.profile_image else None

    class Meta:
        model = Review
        exclude = ["updated_at", "product", "id"]
        extra_kwargs = {
            "user": {"required": False},
            "product": {"required": False},
        }


class GoodsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsModel
        fields = [
            'name', 'price', 'description', 'x_axis', 'y_axis'  # เปลี่ยนจาก latitude, longitude
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        # Update coordinates if provided
        x_axis_data = validated_data.get('x_axis')
        y_axis_data = validated_data.get('y_axis')
        
        if x_axis_data is not None:
            instance.x_axis = x_axis_data
        if y_axis_data is not None:
            instance.y_axis = y_axis_data
            
        instance.save()
        return instance


class CreateProductSerializer(serializers.ModelSerializer):
    sizes = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False
    )
    colors = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False
    )
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = GoodsModel
        fields = [
            "name",
            "description",
            "price",
            "category",
            "store",
            "sizes",
            "colors",
            "images",
        ]

    def create(self, validated_data):
        sizes_data = validated_data.pop("sizes", [])
        colors_data = validated_data.pop("colors", [])
        images_data = validated_data.pop("images", [])

        product = GoodsModel.objects.create(**validated_data)

        for size_name in sizes_data:
            size = SizeModel.objects.create(product=product, name=size_name)

        for color_name in colors_data:
            color = ColorModel.objects.create(product=product, name=color_name)

        for image_file in images_data:
            image = ProductImage.objects.create(product=product, image=image_file)

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sizes = instance.size_set.all()
        colors = instance.color_set.all()
        images = instance.images.all()

        representation["sizes"] = SizeSerializer(sizes, many=True).data
        representation["colors"] = ColorSerializer(colors, many=True).data
        representation["images"] = ProductImageSerializer(images, many=True).data

        return representation


# class UpdateProductSerializer(serializers.ModelSerializer):
#     sizes = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
#     colors = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
#     images = serializers.ListField(child=serializers.ImageField(), required=False)
#     latitude = serializers.FloatField(required=False)
#     longitude = serializers.FloatField(required=False)

#     class Meta:
#         model = GoodsModel
#         fields = ['name', 'description', 'price', 'category', 'sizes', 'colors', 'images']

#     def update(self, instance, validated_data):
#         sizes_data = validated_data.pop('sizes', None)
#         colors_data = validated_data.pop('colors', None)
#         images_data = validated_data.pop('images', None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         if sizes_data is not None:
#             instance.size.all().delete()  # Clear existing sizes
#             for size_name in sizes_data:
#                 SizeModel.objects.create(product=instance, name=size_name)

#         if colors_data is not None:
#             instance.color.all().delete()  # Clear existing colors
#             for color_name in colors_data:
#                 ColorModel.objects.create(product=instance, name=color_name)

#         if images_data is not None:
#             instance.images.all().delete()  # Clear existing images
#             for image_file in images_data:
#                 ProductImage.objects.create(product=instance, image=image_file)

#         return instance


class UpdateProductSerializer(serializers.ModelSerializer):
    sizes = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    colors = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    x_axis = serializers.ListField(child=serializers.FloatField(), required=False, min_length=2, max_length=2)
    y_axis = serializers.ListField(child=serializers.FloatField(), required=False, min_length=2, max_length=2)

    class Meta:
        model = GoodsModel
        fields = [
            "name",
            "description",
            "price",
            "category",
            "sizes",
            "colors",
            "images",
            "x_axis",
            "y_axis"
        ]

    def update(self, instance, validated_data):
        sizes_data = validated_data.pop("sizes", None)
        colors_data = validated_data.pop("colors", None)
        images_data = validated_data.pop("images", None)
        x_axis_data = validated_data.pop("x_axis", None)
        y_axis_data = validated_data.pop("y_axis", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if sizes_data is not None:
            instance.size.all().delete()
            for size_name in sizes_data:
                SizeModel.objects.create(product=instance, name=size_name)

        if colors_data is not None:
            instance.color.all().delete()
            for color_name in colors_data:
                ColorModel.objects.create(product=instance, name=color_name)

        if images_data is not None:
            instance.images.all().delete()
            for image_file in images_data:
                ProductImage.objects.create(product=instance, image=image_file)

        if x_axis_data is not None:
            instance.x_axis = x_axis_data

        if y_axis_data is not None:
            instance.y_axis = y_axis_data

        return instance


# bank account
class BankAccountSerializer(serializers.ModelSerializer):
    # Assuming 'store' is a ForeignKey field in your BankAccount model

    # Use PrimaryKeyRelatedField if store is represented by its ID
    store = serializers.PrimaryKeyRelatedField(queryset=StoreModel.objects.all())

    class Meta:
        model = BankAccount
        fields = ["id", "name", "account_name", "account_number", "image", "store"]


class BankAccountSerializer2(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = "__all__"


class BankAccountByStoreSerializer(serializers.Serializer):
    has_bank_account = serializers.SerializerMethodField()

    def get_has_bank_account(self, obj):
        return obj


# class BankAccountDetailByStoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankAccount
#         fields = ['id', 'name', 'account_name', 'account_number', 'image']


class WebInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebInfo
        fields = [
            "id",
            "name",
            "tel1",
            "tel2",
            "email",
            "address",
            "description",
            "logo",
            "background",
        ]


class NoticeListSerializers(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = NoticeModel
        fields = ["id", "subject", "user", "brochure", "created_at", "updated_at"]


class NoticeSerializers(serializers.ModelSerializer):
    class Meta:
        model = NoticeModel
        fields = ["id", "subject", "user", "brochure"]


class StockedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockedImage
        fields = ['id', 'position', 'image']

class StockedSerializer(serializers.ModelSerializer):
    images = StockedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Stocked
        fields = ['id', 'store', 'point_view', 'created_at', 'updated_at', 'images']

class StockedWithImagesSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )

    class Meta:
        model = Stocked
        fields = ['store', 'point_view', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        stocked = Stocked.objects.create(**validated_data)
        
        for image_data in images_data:
            StockedImage.objects.create(
                stocked=stocked,
                position=image_data['position'],
                image=image_data['image']
            )
        
        return stocked

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        instance.store_id = validated_data.get('store', instance.store_id)
        instance.point_view = validated_data.get('point_view', instance.point_view)
        instance.save()

        for image_data in images_data:
            StockedImage.objects.create(
                stocked=instance,
                position=image_data['position'],
                image=image_data['image']
            )
        
        return instance
    

class StoreSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    
    email = serializers.SerializerMethodField()
    
    def get_email(self, obj):
        return obj.seller.email if obj.seller else None
    
    def get_is_admin(self, obj):
        return obj.seller.is_admin if obj.seller else False
    
    
    class Meta:
        model = StoreModel
        fields = ['id', 'name', 'address', 'phone', 'company_number', 'sub_address', 'introduce', 'is_admin', 'email']


class StoreBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreBanner
        fields = ['id', 'image']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        fields = [
            'id',
            'seller',
            'name',
            'introduce',
            'address',
            'phone',
            'background_image',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        return StoreModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CreateStoreSerializer(serializers.ModelSerializer):
    seller_id = serializers.IntegerField()

    class Meta:
        model = StoreModel
        fields = ['seller_id', 'name', 'address', 'phone', 'company_number', 'sub_address', 'introduce']

    def validate_seller_id(self, value):
        try:
            seller = UserModel.objects.get(id=value, is_seller=True)
            if StoreModel.objects.filter(seller=seller).exists():
                raise serializers.ValidationError("Seller already has a store")
            return value
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Invalid seller ID or user is not a seller")


class Mode3DSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode3D
        fields = ['is_enabled']


# 3D Mode Image
class Mode3DImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode3DImage
        fields = ['id', 'store', 'image', 'name', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# 3D Mode Image Create
class Mode3DImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode3DImage
        fields = ['image', 'name', 'sort_order']


# 3D Mode Image Bulk Create
class Mode3DImageBulkCreateSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

    def create(self, validated_data):
        images_data = validated_data.get('images', [])
        created_images = []
        
        # Get the store_id from context
        store_id = self.context['store_id']
        
        # Get all existing sort_orders for this store
        existing_orders = set(Mode3DImage.objects.filter(store_id=store_id).values_list('sort_order', flat=True))
        
        # Find the maximum sort_order
        max_sort_order = max(existing_orders) if existing_orders else -1
        
        # Find available numbers between 0 and max_sort_order
        available_orders = [num for num in range(max_sort_order + 1) if num not in existing_orders]
        
        # Sort available orders
        available_orders.sort()
        
        # Counter for new images
        new_image_count = 0
        
        for image_data in images_data:
            # Store metadata before processing image
            name = image_data.get('name')
            
            # Determine sort_order
            if new_image_count < len(available_orders):
                # Use available order if there are any
                sort_order = available_orders[new_image_count]
            else:
                # Otherwise use the next number after max_sort_order
                sort_order = max_sort_order + (new_image_count - len(available_orders) + 1)
            
            # Convert base64 image to file
            image_base64 = image_data.get('image')
            if image_base64:
                try:
                    # Remove data URL prefix if present
                    if ',' in image_base64:
                        image_base64 = image_base64.split(',')[1]
                    
                    # Add padding if needed
                    padding = len(image_base64) % 4
                    if padding:
                        image_base64 += '=' * (4 - padding)
                    
                    # Decode base64 to binary
                    image_binary = base64.b64decode(image_base64)
                    
                    # Generate unique filename
                    filename = f"{uuid.uuid4()}.jpg"
                    
                    # Create ContentFile from binary data
                    image_file = ContentFile(image_binary, name=filename)
                    
                    # Create Mode3DImage instance
                    image_obj = Mode3DImage.objects.create(
                        store_id=store_id,
                        image=image_file,
                        name=name,
                        sort_order=sort_order
                    )
                    created_images.append(image_obj)
                    new_image_count += 1
                except Exception as e:
                    raise serializers.ValidationError(f"Error processing image: {str(e)}")
            
        return created_images


# 3D Mode Image Update
class Mode3DImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode3DImage
        fields = ['image', 'name', 'sort_order']
        extra_kwargs = {
            'image': {'required': False},
            'name': {'required': False},
            'sort_order': {'required': False}
        }

    def validate(self, attrs):
        # Get the instance being updated
        instance = self.instance
        store_id = instance.store_id
        
        # Get the new sort_order if it's being updated
        new_sort_order = attrs.get('sort_order')
        
        if new_sort_order is not None:
            # Check if another image in the same store has this sort_order
            existing_image = Mode3DImage.objects.filter(
                store_id=store_id,
                sort_order=new_sort_order
            ).exclude(id=instance.id).first()
            
            if existing_image:
                # Get all used sort_orders in the store
                used_orders = set(Mode3DImage.objects.filter(
                    store_id=store_id
                ).exclude(id=instance.id).values_list('sort_order', flat=True))
                
                # Get the highest sort_order
                max_sort_order = max(used_orders) if used_orders else 0
                
                # Find available numbers between 0 and max_sort_order
                available_orders = [num for num in range(max_sort_order + 1) if num not in used_orders]
                
                # Format available numbers for display
                available_text = ", ".join(map(str, available_orders)) if available_orders else "No available numbers"
                
                raise serializers.ValidationError({
                    'sort_order': f'order number {new_sort_order} already exists in this store',
                    'last_available_order': max_sort_order,
                    'available_orders': available_orders,
                    'message': f'Please select a new order number (available numbers from 0 is: {available_text}) or from {max_sort_order + 1} to 1000'
                })
        
        return attrs


class Mode3DImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode3DImage
        fields = ['id', 'image', 'name', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

