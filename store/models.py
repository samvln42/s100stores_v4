from django.db import models
from users.models import UserModel


class CategoryModel(models.Model):
    class Meta:
        db_table = "category"
        verbose_name_plural = "1. Category types"

    name = models.CharField(max_length=100, default="etc", verbose_name="Category name")
    image = models.ImageField(upload_to="media/", null=True, blank=True)

    def __str__(self):
        return str(self.name)


class StoreModel(models.Model):
    class Meta:
        db_table = "store"
        verbose_name_plural = "2. Store list"

    seller = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, verbose_name="seller"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Store name",
    )
    address = models.CharField(
        max_length=200,
        verbose_name="store location",
    )
    phone = models.CharField(max_length=200, null=True, blank=True)
    company_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Company Registration Number",
    )
    sub_address = models.CharField(
        max_length=200, verbose_name="Store detailed address", null=True, blank=True
    )
    introduce = models.TextField(null=True, blank=True, verbose_name="introduction")

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Save the store first
        super().save(*args, **kwargs)
        # Create Mode3D instance if it doesn't exist
        Mode3D.objects.get_or_create(store=self, defaults={'is_enabled': False})
    
    def delete(self, *args, **kwargs):
        # Get the seller before deleting the store
        seller = self.seller
        
        # Delete the store
        super().delete(*args, **kwargs)
        
        # Check if the seller has no other stores
        if not StoreModel.objects.filter(seller=seller).exists():
            # Convert seller to regular user by setting is_seller to False
            seller.is_seller = False
            seller.save()


# store banner image
class StoreBanner(models.Model):
    class Meta:
        db_table = "store_banner"
        verbose_name_plural = "Store Banner"
        
    store = models.ForeignKey(
        StoreModel,
        on_delete=models.CASCADE,
        related_name='banner'
    )
    image = models.ImageField(upload_to='media/store_banner/')
    
    
class Stocked(models.Model):
    class Meta:
        db_table = "stocked"
        verbose_name_plural = "Stocked"

    store = models.ForeignKey(
        StoreModel, 
        on_delete=models.CASCADE,
        related_name='stocked'
    )
    point_view = models.CharField(max_length=100, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stocked {self.pk} - Store: {self.store.name}"

class StockedImage(models.Model):
    class Meta:
        db_table = "stocked_images"
        verbose_name_plural = "Stocked Images"

    stocked = models.ForeignKey(
        Stocked,
        on_delete=models.CASCADE,
        related_name='images'
    )
    position = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='media/stocked/')

    def __str__(self):
        return f"StockedImage {self.pk} - Position: {self.position}"

    def delete(self, *args, **kwargs):
        # Delete the physical image file
        if self.image:
            self.image.delete()
        
        # Delete all related goods before deleting self
        GoodsModel.objects.filter(stocked_image=self).delete()
        
        super().delete(*args, **kwargs)


class GoodsModel(models.Model):
    class Meta:
        db_table = "goods"
        verbose_name_plural = "3. Product list"

    store = models.ForeignKey(
        StoreModel, on_delete=models.CASCADE, verbose_name="store"
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="category",
    )
    stocked_image = models.ForeignKey(
        'StockedImage',
        on_delete=models.CASCADE,
        null=True,
        related_name='goods'
    )
    name = models.CharField(max_length=100, verbose_name="product name")
    price = models.PositiveIntegerField(default=0, verbose_name="price")
    description = models.TextField(blank=True)
    x_axis = models.JSONField(null=True)
    y_axis = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class SizeModel(models.Model):
    product = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, related_name="size"
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ColorModel(models.Model):
    product = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, related_name="color"
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ImageModel(models.Model):
    class Meta:
        db_table = "image"
        verbose_name_plural = "4. Product image list"

    goods = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, verbose_name="Goods"
    )
    image = models.FileField(
        null=True, blank=True, verbose_name="image", upload_to="media/"
    )

    def __str__(self):
        return str(self.goods.name)


class ProductImage(models.Model):
    product = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="media/")

    def __str__(self):
        return f"Image for {self.product.name}"


# Old one
class OrderModel(models.Model):
    class Meta:
        db_table = "order"
        verbose_name_plural = "5. Order History"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="buyer")
    goods = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, verbose_name="purchase goods"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="price")
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="order time")

    def __str__(self):
        return str(self.goods.name)


# New one
class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    store = models.ForeignKey(
        StoreModel,
        on_delete=models.CASCADE,
        verbose_name="store",
        null=True,
        blank=True,
    )
    tel = models.CharField(max_length=20)
    total_prices = models.DecimalField(max_digits=10, decimal_places=2)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    shipping_company = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    china_url = models.CharField(max_length=255, null=True, blank=True)
    lao_url = models.CharField(max_length=255, null=True, blank=True)
    order_bill = models.ImageField(upload_to="media/", null=True, blank=True)

    def __str__(self):
        return f"Order {self.pk} - User: {self.user.email}, Status: {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        GoodsModel, on_delete=models.SET_NULL, null=True, related_name="orderitem"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)

    def __str__(self):
        return f"OrderItem {self.pk} - Product: {self.product.name}, Quantity: {self.quantity}"


# old review
class ReviewModel(models.Model):
    class Meta:
        db_table = "review"
        verbose_name_plural = "6. Review history"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="Writer")
    goods = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, verbose_name="review product"
    )
    review = models.TextField()
    star = models.FloatField(default=0, verbose_name="scope")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.goods.name)


# # new review
class Review(models.Model):
    product = models.ForeignKey(
        GoodsModel, on_delete=models.CASCADE, related_name="review"
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.email}"


class BookmarkModel(models.Model):
    class Meta:
        db_table = "bookmark"
        verbose_name_plural = "Bookmark history"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE)
    bookmark = models.BooleanField(default=True)


class FilteringModel(models.Model):
    class Meta:
        verbose_name_plural = "7. Filter product list"

    filter = models.CharField(max_length=100, verbose_name="filter")
    option = models.TextField(
        null=True, blank=True, default="", verbose_name="Additional explanation"
    )


class PolicyModel(models.Model):
    class Meta:
        verbose_name_plural = "8. Terms and privacy policy"

    category = models.IntegerField(
        null=True, blank=True, default=1, verbose_name="type"
    )
    content = models.TextField(null=True, blank=True, default="", verbose_name="detail")


# Bank account
class BankAccount(models.Model):
    store = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    image = models.FileField(
        null=True, blank=True, verbose_name="image", upload_to="media/"
    )

    def __str__(self):
        return f"BankAccount {self.pk} - Store: {self.store.name}"


class WebInfo(models.Model):
    class Meta:
        db_table = "WebInfo"
        verbose_name_plural = "Website Informations"
        
    name = models.CharField(max_length=100)
    tel1 = models.CharField(max_length=20)
    tel2 = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.FileField(
        null=True, blank=True, verbose_name="logo image", upload_to="media/"
    )
    background = models.FileField(
        null=True, blank=True, verbose_name="background image", upload_to="media/"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NoticeModel(models.Model):
    subject = models.CharField(max_length=100)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="admin")
    brochure = models.FileField(
        null=True, blank=True, verbose_name="Brochure", upload_to="media/notice/"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("-id",)
    
    def __str__(self):
        return self.subject


class Mode3D(models.Model):
    class Meta:
        db_table = "mode_3d"
        verbose_name_plural = "3D Mode Settings"

    store = models.OneToOneField(
        StoreModel,
        on_delete=models.CASCADE,
        related_name='mode_3d'
    )
    is_enabled = models.BooleanField(default=False, verbose_name="3D Mode Enabled")
    
    def __str__(self):
        return f"3D Mode for {self.store.name}"
    
# 3D Mode Image panorama
class Mode3DImage(models.Model):
    class Meta:
        db_table = "mode_3d_image"
        verbose_name_plural = "3D Mode Image"
        unique_together = ['store', 'sort_order']
        
    store = models.ForeignKey(StoreModel, on_delete=models.CASCADE, related_name='mode_3d_image')
    image = models.ImageField(upload_to='media/mode_3d/')
    name = models.CharField(max_length=100, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"3D Mode Image for {self.store.name}"
