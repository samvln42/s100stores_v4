import base64
import uuid
from collections import Counter
from pprint import pprint
from PIL import Image
import io
import django
from django.core.files.base import ContentFile
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import status, permissions, generics, viewsets, response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    BasePermission, 
    IsAdminUser,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
from rest_framework.decorators import api_view, permission_classes
from users.models import UserModel
from .models import StoreModel
from .serializers import CreateStoreSerializer

from .form import ReviewForm
from .models import (
    GoodsModel,
    StoreModel,
    ReviewModel,
    BookmarkModel,
    OrderModel,
    FilteringModel,
    ImageModel,
    CategoryModel,
    PolicyModel,
    SizeModel,
    ColorModel,
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
)
from .serializers import (
    StoreSerializer,
    GoodsSerializer,
    ReviewSerializer,
    GoodsDetailSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
    PendingOrderSerializer,
    ProcessingOrderSerializer,
    ShippedOrderSerializer,
    DeliveredOrderSerializer,
    OrderUpdateChinaUrlSerializer,
    OrderUpdateLaoUrlSerializer,
    OrderUpdateBillSerializer,
    PostSerializer,
    UpdateStoreSerializer,
    ImageSerializer,
    GoodsCreateSerializer,
    CategorySerializer,
    CreateProductSerializer,
    UpdateProductSerializer,
    BankAccountSerializer,
    BankAccountSerializer2,
    ReviewCreateSerializer,
    WebInfoSerializer,
    NoticeListSerializers,
    NoticeSerializers,
    StockedSerializer,
    StockedImageSerializer,
    StockedWithImagesSerializer,
    OnlyStoreGoodsSerializer,
    StoreBannerSerializer,
    CreateStoreSerializer,
    Mode3DSerializer,
)


from .permissions import IsOwnerOrReadOnly

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

"""
Permission to divide general users, merchants, and administrators
"""


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        try:
            seller = request.user.is_seller
            admin = request.user.is_admin
            if seller or admin:
                return True
            else:
                return False
        except:
            # Login
            return False


def goods_list(request):
    return render(request, "home.html")


def goods_detail(request, goods_id):
    return render(request, "store/goods_detail.html")


def order_list(request):
    return render(request, "store/order_list.html")


def store_setting(request):
    return render(request, "store/admin.html")


# Notice management
# class NoticeList(generics.ListAPIView):
#     queryset = NoticeModel.objects.all()
#     serializer_class = NoticeListSerializers

# class NoticeDetailDelete(generics.RetrieveDestroyAPIView):
#     queryset = NoticeModel.objects.all()
#     serializer_class = NoticeListSerializers

# class NoticeCreate(generics.CreateAPIView):
#     queryset = NoticeModel.objects.all()
#     serializer_class = NoticeSerializers

# class NoticeUpdate(generics.UpdateAPIView):
#     queryset = NoticeModel.objects.all()
#     serializer_class = NoticeSerializers


class NoticeList(generics.ListAPIView):
    queryset = NoticeModel.objects.all()
    serializer_class = NoticeListSerializers


class NoticeDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = NoticeModel.objects.all()
    serializer_class = NoticeListSerializers


class NoticeCreate(generics.CreateAPIView):
    queryset = NoticeModel.objects.all()
    serializer_class = NoticeSerializers

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            messages.success(request, "Notice created successfully.")
            return Response(
                {"message": "Notice created successfully.", "data": response.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "Error creating notice.", "errors": response.data},
                status=response.status_code,
            )


class NoticeUpdate(generics.UpdateAPIView):
    queryset = NoticeModel.objects.all()
    serializer_class = NoticeSerializers

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            messages.success(request, "Notice updated successfully.")
            return Response(
                {"message": "Notice updated successfully.", "data": response.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Error updating notice.", "errors": response.data},
                status=response.status_code,
            )


# Category management
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer

    def get_object_or_404(self, queryset=None):
        try:
            return super().get_object()
        except Http404:
            raise Http404({"message": "Category not found"})

    def put(self, request, *args, **kwargs):
        instance = self.get_object_or_404()
        serializer = CategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object_or_404()
        serializer = CategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object_or_404()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GoodsView2(APIView):
    @swagger_auto_schema(
        tags=["View product list and details"], responses={200: "Success"}
    )
    def get(self, request, goods_id=None):
        """
        <View product>
        goods_id O -> View details
        goods_id
        * Separately removed due to merchant permission issues *
        """
        category_id = request.GET.get("category", "1")  # Default category ID
        category_name = request.GET.get("category_name")  # Category name if provided
        if category_name:
            category_id = get_object_or_404(CategoryModel, name=category_name).id

        if goods_id is None:
            category = request.GET.get(
                "category", "1"
            )  # You can provide default values.
            goods = GoodsModel.objects.all()
            if not goods.exists():
                return Response([], status=200)
            """
             <Filtering branch>
             - Latest
             - Old shoots
             - Price ascending & descending order
             - Ascending & descending number of reviews (5,6)
             """
            if category == "2":
                goods = goods.order_by("-price")
            elif category == "3":
                goods = goods.annotate(review_count=Count("reviewmodel")).order_by(
                    "-review_count"
                )
            elif category == "4":
                goods = goods.order_by("price")
            elif category == "5":
                goods = goods.annotate(order_count=Count("ordermodel")).order_by(
                    "-order_count"
                )
            elif category == "6":
                goods = goods.annotate(order_count=Count("ordermodel")).order_by(
                    "-created_at"
                )
            elif category == "7":
                goods = goods.filter(is_popular=True).order_by("-created_at")
            else:
                try:
                    goods = goods.order_by("-price")
                except Exception as e:
                    print(e)
                    return Response(
                        {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
            serializer = GoodsSerializer(goods, many=True)
            return Response(serializer.data, status=200)
            # return render(request, 'home.html', context={'data': serializer.data, "token": token})
        else:
            goods = get_object_or_404(GoodsModel, id=goods_id)
            serializer = GoodsDetailSerializer(goods)
            order_total = OrderModel.objects.filter(
                user_id=request.user.id, goods=goods
            ).count()
            review_total = ReviewModel.objects.filter(
                user_id=request.user.id, goods=goods
            ).count()
            result = serializer.data.copy()
            if order_total >= review_total:
                result["is_ordered"] = True
            else:
                result["is_ordered"] = False
            return Response(result, status=200)
            # return render(request, 'store/goods_detail.html', context={'goods': serializer.data})


# class GoodsView(APIView):
#     @swagger_auto_schema(
#         tags=["View product list and details"], responses={200: "Success"}
#     )
#     def get(self, request, goods_id=None):
#         category_name = request.GET.get("category_name")
#         category_type = request.GET.get("category_type", "1")  # Default category type
#         if goods_id is None:
#             if category_name:
#                 category = get_object_or_404(CategoryModel, name=category_name)
#                 goods = GoodsModel.objects.filter(category=category)
#             else:
#                 goods = GoodsModel.objects.all()

#             if not goods.exists():
#                 return Response([], status=200)
#             if category_type == "2":
#                 goods = goods.order_by("-price")
#             elif category_type == "3":
#                 goods = goods.annotate(review_count=Count("review")).order_by(
#                     "-review_count"
#                 )
#             elif category_type == "4":
#                 goods = goods.order_by("price")
#             elif category_type == "5":
#                 goods = goods.annotate(order_count=Count("ordermodel")).order_by(
#                     "-order_count"
#                 )
#             elif category_type == "6":
#                 goods = goods.annotate(order_count=Count("ordermodel")).order_by(
#                     "-created_at"
#                 )
#             elif category_type == "7":
#                 goods = goods.filter(is_popular=True).order_by("-created_at")
#             else:
#                 try:
#                     goods = goods.order_by("-price")
#                 except Exception as e:
#                     print(e)
#                     return Response(
#                         {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
#                     )

#             serializer = GoodsSerializer(goods, many=True)
#             return Response(serializer.data)
#         else:
#             goods = get_object_or_404(GoodsModel, id=goods_id)
#             serializer = GoodsDetailSerializer(goods)
#             order_total = OrderModel.objects.filter(
#                 user_id=request.user.id, goods=goods
#             ).count()
#             review_total = ReviewModel.objects.filter(
#                 user_id=request.user.id, goods=goods
#             ).count()
#             result = serializer.data.copy()
#             if order_total >= review_total:
#                 result["is_ordered"] = True
#             else:
#                 result["is_ordered"] = False
#             return Response(result, status=200)


class GoodsView(APIView):
    @swagger_auto_schema(
        tags=["View product list and details"], responses={200: "Success"}
    )
    def get(self, request, goods_id=None):
        category_name = request.GET.get("category_name")
        category_type = request.GET.get("category_type", "1")  # Default category type
        store_id = request.GET.get("store_id")

        if goods_id is None:
            goods = self.get_filtered_goods(category_name, category_type, store_id)

            if not goods.exists():
                return Response([], status=200)

            serializer = GoodsSerializer(goods, many=True)
            return Response(serializer.data)
        else:
            goods = get_object_or_404(GoodsModel, id=goods_id)
            serializer = GoodsDetailSerializer(goods)
            result = serializer.data.copy()
            result["is_ordered"] = self.is_ordered_by_user(request.user.id, goods)
            return Response(result, status=200)

    def get_filtered_goods(self, category_name, category_type, store_id):
        goods = GoodsModel.objects.all()

        if store_id:
            goods = goods.filter(store_id=store_id)

        if category_name:
            category = get_object_or_404(CategoryModel, name=category_name)
            goods = goods.filter(category=category)

        sorting_mapping = {
            "2": "-price",
            "3": "-review_count",
            "4": "price",
            "5": "-order_count",
            "1": "-created_at",
        }


        sorting_key = sorting_mapping.get(category_type, sorting_mapping["1"])

        if category_type == "3":
            goods = goods.annotate(review_count=Count("review"))

        if category_type in ["5", "6"]:
            goods = goods.annotate(order_count=Count("order"))

        if category_type == "7":
            goods = goods.filter(is_popular=True)

        try:
            goods = goods.order_by(sorting_key)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return goods

    def is_ordered_by_user(self, user_id, goods):
        order_total = OrderModel.objects.filter(user_id=user_id, goods=goods).count()
        review_total = ReviewModel.objects.filter(user_id=user_id, goods=goods).count()
        return order_total >= review_total


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoreModel.objects.all()
    serializer_class = StoreSerializer


class StoreView(APIView):
    # permission_classes = [IsSeller]

    @swagger_auto_schema(
        tags=["Store information & product registration & store modification"],
        responses={200: "Success"},
    )
    def get(self, request, store_id):
        """
        ดึงข้อมูลร้านค้า พร้อมสินค้าและรูปภาพทั้งหมด
        """
        try:
            # ใช้ prefetch_related เพื่อลด queries
            store = StoreModel.objects.prefetch_related(
                'goodsmodel_set',  # ดึงสินค้าทั้งหมด
                'goodsmodel_set__images',  # ดึงรูปภาพของสินค้า
                'goodsmodel_set__size',  # ดึงข้อมูล size
                'goodsmodel_set__color'  # ดึงข้อมูล color
            ).get(id=store_id)
            
            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except StoreModel.DoesNotExist:
            return Response(
                {"error": "Store not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        tags=["Store information & product registration & store modification"],
        request_body=PostSerializer,
        responses={200: "Success"},
    )
    def post(self, request, store_id):
        """
        เพิ่มหรืออัพเดทสินค้าพร้อมรูปภาพ
        """
        try:
            store = get_object_or_404(StoreModel, id=store_id)
            
            # ตรวจสอบสิทธิ์ (ถ้าจำเป็น)
            if request.user != store.seller and not request.user.is_admin:
                return Response(
                    {"error": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            goods_data = request.data.get("goods_set", [])
            response_data = []

            for data in goods_data:
                # แยกข้อมูลรูปภาพออกจากข้อมูลสินค้า
                images_data = data.pop('images', [])
                sizes_data = data.pop('sizes', [])
                colors_data = data.pop('colors', [])

                # สร้างหรืออัพเดทสินค้า
                goods_serializer = GoodsCreateSerializer(data=data)
                if goods_serializer.is_valid():
                    goods = goods_serializer.save(store=store)

                    # จัดการรูปภาพ
                    for image_data in images_data:
                        ProductImage.objects.create(
                            product=goods,
                            image=image_data
                        )

                    # จัดการ sizes
                    for size in sizes_data:
                        SizeModel.objects.create(
                            product=goods,
                            name=size
                        )

                    # จัดการ colors
                    for color in colors_data:
                        ColorModel.objects.create(
                            product=goods,
                            name=color
                        )

                    # ดึงข้อมูลที่อัพเดทแล้ว
                    updated_goods = GoodsSerializer(goods).data
                    response_data.append(updated_goods)
                else:
                    return Response(
                        goods_serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        tags=["Store information & product registration & store modification"],
        request_body=PostSerializer,
        responses={200: "Success"},
    )
    def patch(self, request, store_id):
        """
        อัพเดทข้อมูลร้านค้า
        """
        try:
            store = get_object_or_404(StoreModel, id=store_id)
            
            # ตรวจสอบสิทธิ์
            if request.user != store.seller and not request.user.is_admin:
                return Response(
                    {"error": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = UpdateStoreSerializer(
                store, 
                data=request.data, 
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateProductAPIView(APIView):
    @swagger_auto_schema(
        tags=["Store information & product registration & store modification"],
        responses={200: "Success"},
    )
    def get(self, request, store_id):
        """
        <View store information>
        - Store basic information
        - List of products in the store
        """
        store = get_object_or_404(StoreModel, id=store_id)
        serializer = StoreSerializer(store)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateProductView(CreateAPIView):
    queryset = GoodsModel.objects.all()
    serializer_class = CreateProductSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateProductAPIView(APIView):
#     def put(self, request, pk, format=None):
#         try:
#             product = GoodsModel.objects.get(pk=pk)
#         except GoodsModel.DoesNotExist:
#             return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UpdateProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "success"}, status=status.HTTP_200_OK)
#         return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductAPIView(APIView):
    def get_object(self, pk):
        try:
            return GoodsModel.objects.get(pk=pk)
        except GoodsModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = UpdateProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response(
            {"message": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = UpdateProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response(
            {"message": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteProductAPIView(APIView):
    def delete(self, request, pk, format=None):
        try:
            product = GoodsModel.objects.get(pk=pk)
        except GoodsModel.DoesNotExist:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Delete related Size instances
        SizeModel.objects.filter(product=product).delete()

        # Delete related Color instances
        ColorModel.objects.filter(product=product).delete()

        # Delete related ProductImage instances
        ProductImage.objects.filter(product=product).delete()

        # Delete the Product instance
        product.delete()

        return Response({"message": "success"}, status=status.HTTP_200_OK)


class GoodsPatchView(APIView):
    # permission_classes = [IsSeller]

    @swagger_auto_schema(
        tags=["Multiple product modifications"],
        request_body=PostSerializer,
        responses={200: "Success"},
    )
    def patch(self, request):
        if request.data.get("goods_set"):
            for data in request.data.get("goods_set"):
                if data:
                    data = data.copy()
                    if "Kip" in data["price"]:
                        data["price"] = data["price"][:-1]
                    goods = get_object_or_404(GoodsModel, id=data.get("id"))
                    serializer = GoodsSerializer(goods, data=data, partial=True)
                    category, is_created = CategoryModel.objects.get_or_create(
                        name=data.get("category")
                    )
                    if serializer.is_valid():
                        instance = serializer.save(category=category)
                        images_data = data.get("images", [])
                        if images_data:
                            instance.imagemodel_set.all().delete()
                            for idx, image_data in enumerate(images_data):
                                # Convert Base64 encoded string to image file
                                # Delete all existing images and save as new -> It would be better to select the image and edit it later.
                                format, imgstr = image_data.split(";base64,")
                                ext = format.split("/")[-1]
                                file_data = ContentFile(
                                    base64.b64decode(imgstr),
                                    name=f"{uuid.uuid4()}.{ext}",
                                )
                                # Create a new image object and save it with the image file
                                ImageModel.objects.create(
                                    goods=instance, image=file_data
                                )
                    else:
                        print(serializer.errors)
            return Response(
                {"message": "The product has been modified."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "A problem has occurred."}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        if request.data.get("goods_id"):
            goods = get_object_or_404(GoodsModel, id=request.data.get("goods_id"))
            goods.delete()
        return Response({"message": "success"}, status=status.HTTP_200_OK)


# Old review
class ReviewView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    """
    <Logic related to reviews>
    Edit and delete review -> pk = id of review
    """

    @swagger_auto_schema(
        tags=["View and write product reviews"], responses={200: "Success"}
    )
    def get(self, request, pk):
        # pk = product id
        review = ReviewModel.objects.filter(goods_id=pk).order_by("-created_at")
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["View and write product reviews"],
        request_body=PostSerializer,
        responses={201: "Created"},
    )
    def post(self, request, pk):
        # pk = product id
        review = ReviewModel.objects.filter(user=request.user, goods_id=pk).exists()
        order = OrderModel.objects.filter(user=request.user, goods_id=pk).exists()
        if not order:
            return Response(
                {"message": "Only users who have placed an order can leave a review."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if review:
            return Response(
                {"message": "I've already written a review."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(goods_id=pk, user=request.user)
            return Response(
                {"message": "Review completed"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Please use after logging in."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk):
        review = get_object_or_404(ReviewModel, id=pk, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        review = get_object_or_404(ReviewModel, id=pk, user=request.user)
        review.delete()
        return Response({"message": "success"}, status=status.HTTP_200_OK)


# new review
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Review.objects.filter(user_id=user_id)


class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return Review.objects.filter(product_id=product_id)


# class ReviewDeleteView(generics.DestroyAPIView):
#     def delete(self, request, pk, format=None):
#         try:
#             review = Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             return Response({"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

#         review.delete()

#         return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)


class ReviewByProductAndUserAPIView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer

    def get_object(self):
        product_id = self.kwargs["product_id"]
        user_id = self.kwargs["user_id"]

        try:
            review = Review.objects.get(product_id=product_id, user_id=user_id)
            return review
        except Review.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is None:
            content = {"detail": "Review not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CheckReview(APIView):
    def post(self, request, pk):
        review = ReviewModel.objects.filter(user=request.user, goods_id=pk).exists()
        order = OrderModel.objects.filter(user=request.user, goods_id=pk).exists()
        if not order:
            return Response(
                {"message": "Only users who have placed an order can leave a review."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if review:
            return Response(
                {"message": "I've already written a review."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "success"}, status=status.HTTP_200_OK)


class TermsAPI(APIView):
    def get(self, request, pk):
        # 1: Terms of Use, 2: Privacy Policy
        turm = PolicyModel.objects.filter(category=pk).last()
        content = turm.content if turm else ""
        return Response({"content": content}, status=status.HTTP_200_OK)


def review_form(request, pk):
    form = ReviewForm()
    return render(request, "store/review.html", {"form": form, "goods_id": pk})


def review_list(request, pk):
    return render(request, "store/review_list.html", {"goods_id": pk})


# Old one
class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    <Product order logic>
    """

    @swagger_auto_schema(
        tags=["Product ordering and inquiry"], responses={200: "Success"}
    )
    def get(self, request):
        order_set = (
            OrderModel.objects.filter(user=request.user).distinct().values("goods")
        )
        data = []
        if order_set:
            for order in order_set:
                goods = GoodsModel.objects.get(id=order["goods"])
                data.append(GoodsSerializer(goods).data)
            return Response(data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Product ordering and inquiry"],
        request_body=PostSerializer,
        responses={200: "Success"},
    )
    def post(self, request):
        goods_id = request.data.get("goods_id")

        goods = get_object_or_404(GoodsModel, id=goods_id)
        goods = GoodsSerializer(goods).data.copy()

        serializer = OrderSerializer(data=goods)

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(user=request.user, goods_id=goods_id)
                return Response(
                    {"message": "I ordered a product."}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# New one
# Order
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Retrieve orders with status "Pending"
        return Order.objects.filter(status="Pending")


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Order.objects.filter(user_id=user_id)


# class CreateOrderView(generics.CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderUpdateSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateChinaUrlAPIView(APIView):
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderUpdateChinaUrlSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateLaoUrlAPIView(APIView):
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderUpdateLaoUrlSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateBillAPIView(APIView):
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderUpdateBillSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteView(generics.DestroyAPIView):
    def delete(self, request, pk, format=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Delete related OrderItem instances
        OrderItem.objects.filter(order_id=order).delete()

        # Delete the Order instance
        order.delete()

        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)


# class PendingOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.filter(status='Pending')
#     serializer_class = PendingOrderSerializer

# class ProcessingOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.filter(status='Processing')
#     serializer_class = ProcessingOrderSerializer

# class ShippedOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.filter(status='Shipped')
#     serializer_class = ShippedOrderSerializer

# class DeliveredOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.filter(status='Delivered')
#     serializer_class = DeliveredOrderSerializer

# class DeliveredOrderListAPIView(generics.ListAPIView):
#     serializer_class = DeliveredOrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(status='Delivered')


class PendingOrderListAPIView(generics.ListAPIView):
    serializer_class = PendingOrderSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get("store_id", None)
        queryset = Order.objects.filter(status="Pending")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(
            {"count": len(serializer.data), "orders": serializer.data}
        )


class ProcessingOrderListAPIView(generics.ListAPIView):
    serializer_class = ProcessingOrderSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get("store_id", None)
        queryset = Order.objects.filter(status="Processing")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(
            {"count": len(serializer.data), "orders": serializer.data}
        )


class ShippedOrderListAPIView(generics.ListAPIView):
    serializer_class = ShippedOrderSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get("store_id", None)
        queryset = Order.objects.filter(status="Shipped")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(
            {"count": len(serializer.data), "orders": serializer.data}
        )


class DeliveredOrderListAPIView(generics.ListAPIView):
    serializer_class = DeliveredOrderSerializer

    def get_queryset(self):
        store_id = self.request.query_params.get("store_id", None)
        queryset = Order.objects.filter(status="Delivered")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(
            {"count": len(serializer.data), "orders": serializer.data}
        )


# class PendingOrderListAPIView(generics.ListAPIView):
#     serializer_class = PendingOrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(status='Pending')

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         count = queryset.count()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({
#             'count': count,
#             'orders': serializer.data
#         })


# class ProcessingOrderListAPIView(generics.ListAPIView):
#     serializer_class = ProcessingOrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(status="Processing")

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         count = queryset.count()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({"count": count, "orders": serializer.data})


# class ShippedOrderListAPIView(generics.ListAPIView):
#     serializer_class = ShippedOrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(status="Shipped")

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         count = queryset.count()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({"count": count, "orders": serializer.data})


# class DeliveredOrderListAPIView(generics.ListAPIView):
#     serializer_class = DeliveredOrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(status="Delivered")

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         count = queryset.count()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({"count": count, "orders": serializer.data})


class SearchView(APIView):
    @swagger_auto_schema(
        tags=["search"], request_body=PostSerializer, responses={200: "Success"}
    )
    def post(self, request):
        search_word = request.data.get("search")
        goods_set = GoodsModel.objects.filter(
            Q(name__icontains=search_word) | Q(store__name__icontains=search_word)
        )
        goods = GoodsSerializer(goods_set, many=True).data

        return Response(goods, status=status.HTTP_200_OK)


def resize_image(image_data, output_size=(800, 600), quality=85):
    """
    Adjust the resolution of the image file and save it in JPEG format.
    :param image_data: Original image data (base64 encoded string).
    :param output_size: Size (width, height) of the image to be changed.
    :param quality: JPEG storage quality (1-100).
    :return: Changed image data (base64 encoded string).
    """
    # Convert image data to PIL image object
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    # Change image size
    image = image.resize(output_size, Image.ANTIALIAS)

    # Save in JPEG format
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="JPEG", quality=quality)
    output_data = base64.b64encode(output_buffer.getvalue()).decode()

    return output_data


# Bank account
class BankAccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class BankAccountRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


def check_store_bank_account(request, store_id):
    try:
        store = StoreModel.objects.get(pk=store_id)
    except StoreModel.DoesNotExist:
        return JsonResponse({"error": "Store not found"}, status=404)

    # Check if the store has a bank account
    has_bank_account = BankAccount.objects.filter(store=store).exists()

    return JsonResponse({"has_bank_account": has_bank_account})


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer2

    def list(self, request, *args, **kwargs):
        store_id = self.request.query_params.get("store_id")
        if store_id:
            queryset = self.queryset.filter(store_id=store_id)
        else:
            queryset = self.queryset.none()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BankAccountUpdateAPIView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def update(self, request, *args, **kwargs):
        store_id = kwargs.get("store_id")
        try:
            # Retrieve the bank account associated with the given store ID
            bank_account = BankAccount.objects.get(store_id=store_id)
        except BankAccount.DoesNotExist:
            # If bank account does not exist, return a not found response
            return Response(
                {"message": "Bank account not found for the given store ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the bank account with the updated data
        serializer = self.get_serializer(bank_account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# Website infomation
class WebInfoListCreateAPIView(generics.ListCreateAPIView):
    queryset = WebInfo.objects.all()
    serializer_class = WebInfoSerializer


class WebInfoRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = WebInfo.objects.all()
    serializer_class = WebInfoSerializer
    lookup_field = "pk"  # Use 'pk' as the lookup field for retrieving and updating the WebInfo object



class StockedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stocked.objects.all()
    serializer_class = StockedSerializer

class StockedImageListCreateView(generics.ListCreateAPIView):
    serializer_class = StockedImageSerializer

    def get_queryset(self):
        stocked_id = self.kwargs['stocked_id']
        return StockedImage.objects.filter(stocked_id=stocked_id)

    def perform_create(self, serializer):
        stocked_id = self.kwargs['stocked_id']
        serializer.save(stocked_id=stocked_id)

class StockedImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockedImage.objects.all()
    serializer_class = StockedImageSerializer

class StoreStockedListView(generics.ListAPIView):
    serializer_class = StockedSerializer

    def get_queryset(self):
        store_id = self.kwargs['store_id']
        return Stocked.objects.filter(store_id=store_id).prefetch_related('images')

    @swagger_auto_schema(
        tags=["Stocked"],
        operation_description="Get all stocked items for a specific store",
        responses={200: StockedSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "No stocked items found for this store"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StockedCreateView(generics.CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = StockedWithImagesSerializer
    
    @swagger_auto_schema(
        tags=["Stocked"],
        operation_description="Create a stocked item with images for a specific store",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'point_view': openapi.Schema(type=openapi.TYPE_STRING),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'position': openapi.Schema(type=openapi.TYPE_STRING),
                            'image': openapi.Schema(type=openapi.TYPE_STRING, description='Base64 encoded image'),
                        }
                    )
                ),
            },
            required=['images']
        )
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        images_data = []
        
        # Process images from JSON data
        for image in data.get('images', []):
            try:
                position = image.get('position')
                image_data = image.get('image')
                
                if ';base64,' in image_data:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                else:
                    imgstr = image_data
                    ext = 'jpg'
                
                # Add padding if needed
                padding = len(imgstr) % 4
                if padding:
                    imgstr += '=' * (4 - padding)

                # Convert base64 to file
                file_data = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"{uuid.uuid4()}.{ext}"
                )
                
                images_data.append({
                    'position': position,
                    'image': file_data
                })
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                continue

        # Format data for serializer
        formatted_data = {
            'store': kwargs['store_id'],
            'point_view': str(data.get('point_view', 0)),
            'images': images_data
        }

        serializer = self.get_serializer(data=formatted_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockedUpdateView(generics.UpdateAPIView):
    queryset = Stocked.objects.all()
    serializer_class = StockedWithImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=["Stocked"],
        operation_description="Partially update a stocked item",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'store': openapi.Schema(type=openapi.TYPE_INTEGER),
                'point_view': openapi.Schema(type=openapi.TYPE_STRING),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'position': openapi.Schema(type=openapi.TYPE_STRING),
                            'image': openapi.Schema(type=openapi.TYPE_FILE),
                        }
                    )
                ),
            }
        )
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        
        # สร้าง data ใหม่สำหรับ Stocked model
        formatted_data = {}
        if 'store' in data:
            formatted_data['store'] = data['store']
        if 'point_view' in data:
            formatted_data['point_view'] = str(data['point_view'])

        # อัพเดท Stocked
        serializer = self.get_serializer(instance, data=formatted_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # อัพเดท StockedImage
            i = 0
            while f'images[{i}][position]' in data or f'images[{i}][image]' in data:
                image_id = data.get(f'images[{i}][id]')
                position = data.get(f'images[{i}][position]')
                image = data.get(f'images[{i}][image]')
                
                if image_id:
                    # อัพเดทรูปภาพที่มีอยู่
                    try:
                        image_instance = StockedImage.objects.get(id=image_id, stocked=instance)
                        if position:
                            image_instance.position = position
                        if image:
                            image_instance.image = image
                        image_instance.save()
                    except StockedImage.DoesNotExist:
                        pass
                elif position or image:
                    # สร้างรูปภาพใหม่
                    StockedImage.objects.create(
                        stocked=instance,
                        position=position,
                        image=image
                    )
                i += 1
            
            # ดึงข้อมูลล่าสุด
            updated_instance = self.get_object()
            updated_serializer = self.get_serializer(updated_instance)
            return Response(updated_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreStockedImageGoodsView(APIView):
    @swagger_auto_schema(
        tags=["Store information & product registration"],
        request_body=PostSerializer,
        responses={200: "Success"},
    )
    def post(self, request, store_id, stocked_image_id):
        """
        <Product Registration with Stocked Image>
        """
        if request.data.get("goods_set"):
            store = get_object_or_404(StoreModel, id=store_id)
            stocked_image = get_object_or_404(
                StockedImage, 
                id=stocked_image_id,
                stocked__store_id=store_id
            )
            
            for data in request.data.get("goods_set"):
                if data:
                    serializer = GoodsCreateSerializer(data=data)
                    category, is_created = CategoryModel.objects.get_or_create(
                        name=data.get("category")
                    )

                    if serializer.is_valid():
                        instance = serializer.save(
                            store=store,
                            category=category,
                            stocked_image=stocked_image,
                            x_axis=data.get('x_axis'),
                            y_axis=data.get('y_axis')
                        )
                        
                        # Create sizes if provided
                        sizes_data = data.get("sizes", [])
                        for size_data in sizes_data:
                            SizeModel.objects.create(product=instance, name=size_data)

                        # Create colors if provided
                        colors_data = data.get("colors", [])
                        for color_data in colors_data:
                            ColorModel.objects.create(product=instance, name=color_data)

                        # Handle product images
                        images_data = data.get("images", [])
                        if images_data:
                            for image_data in images_data:
                                try:
                                    if ';base64,' in image_data:
                                        format, imgstr = image_data.split(';base64,')
                                        ext = format.split('/')[-1]
                                    else:
                                        imgstr = image_data
                                        ext = 'jpg'
                                    
                                    padding = len(imgstr) % 4
                                    if padding:
                                        imgstr += '=' * (4 - padding)

                                    file_data = ContentFile(
                                        base64.b64decode(imgstr),
                                        name=f"{uuid.uuid4()}.{ext}"
                                    )
                                    ProductImage.objects.create(
                                        product=instance, 
                                        image=file_data
                                    )
                                except Exception as e:
                                    print(f"Error processing image: {str(e)}")
                                    continue

            return Response(
                {"message": "The product has been registered."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "A problem has occurred."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class StoreStockedImageGoodsListView(APIView):
    @swagger_auto_schema(
        tags=["Store information & product list"],
        responses={200: GoodsSerializer(many=True)}
    )
    def get(self, request, store_id, stocked_image_id):
        """
        Get all products for specific store and stocked image
        """
        store = get_object_or_404(StoreModel, id=store_id)
        stocked_image = get_object_or_404(
            StockedImage, 
            id=stocked_image_id,
            stocked__store_id=store_id
        )
        
        goods = GoodsModel.objects.filter(
            store=store,
            stocked_image=stocked_image
        )
        
        if not goods.exists():
            return Response([], status=status.HTTP_200_OK)
            
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

# stocked image goods update
class StoreStockedImageGoodsUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = GoodsCreateSerializer
    
    def patch(self, request, pk):
        try:
            try:
                goods = GoodsModel.objects.get(id=pk)
            except GoodsModel.DoesNotExist:
                return Response(
                    {
                        "error": f"Product with ID {pk} not found",
                        "code": "product_not_found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # ตรวจสอบว่ามีการส่งรูปภาพมาหรือไม่
            if request.FILES:
                # กรณีอัพเดทรูปภาพ
                images = request.FILES.getlist('images')
                
                if not images:
                    return Response(
                        {"error": "No images found in request"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    # ลบรูปภาพเก่า
                    for old_image in goods.images.all():
                        if old_image.image:
                            old_image.image.delete()
                        old_image.delete()
                    
                    # เพิ่มรูปภาพใหม่
                    for image in images:
                        ProductImage.objects.create(
                            product=goods,
                            image=image
                        )

                    return Response(
                        {
                            "message": "Product images updated successfully",
                            "image_count": len(images),
                            "product_id": pk
                        },
                        status=status.HTTP_200_OK
                    )
                except Exception as img_error:
                    return Response(
                        {
                            "error": f"Error updating images: {str(img_error)}",
                            "code": "image_update_error"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # กรณีอัพเดทข้อมูลอื่นๆ
            data = request.data.copy()
            
            # แปลงข้อมูล JSON strings เป็น Python objects
            for field in ['sizes', 'colors', 'x_axis', 'y_axis']:
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = json.loads(data[field])
                    except json.JSONDecodeError:
                        return Response(
                            {"error": f"Invalid JSON format for {field}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            serializer = self.serializer_class(goods, data=data, partial=True)
            if serializer.is_valid():
                instance = serializer.save()

                # อัพเดท sizes ถ้ามี
                if 'sizes' in data:
                    SizeModel.objects.filter(product=instance).delete()
                    for size in data['sizes']:
                        SizeModel.objects.create(product=instance, name=size)

                # อัพเดท colors ถ้ามี
                if 'colors' in data:
                    ColorModel.objects.filter(product=instance).delete()
                    for color in data['colors']:
                        ColorModel.objects.create(product=instance, name=color)

                return Response(
                    {"message": "Product updated successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "code": "unexpected_error"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# delete stocked image
class DeleteStockedImageAPIView(APIView):
    def delete(self, request, pk, format=None):
        try:
            stocked_image = StockedImage.objects.get(pk=pk)
        except StockedImage.DoesNotExist:
            return Response(
                {"message": "Stocked image not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the image file
        if stocked_image.image:
            stocked_image.image.delete()

        # Delete the StockedImage instance
        stocked_image.delete()

        return Response(
            {"message": "Stocked image deleted successfully"}, 
            status=status.HTTP_200_OK
        )

class UpdateStockedImageAPIView(APIView):
    @swagger_auto_schema(
        tags=["Stocked Image"],
        operation_description="Update a stocked image",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'position': openapi.Schema(type=openapi.TYPE_STRING),
                'image': openapi.Schema(type=openapi.TYPE_FILE),
            }
        ),
        responses={200: "Success"}
    )
    def patch(self, request, pk):
        try:
            stocked_image = StockedImage.objects.get(pk=pk)
        except StockedImage.DoesNotExist:
            return Response(
                {"message": "Stocked image not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # อัพเดทตำแหน่ง
        if 'position' in request.data:
            stocked_image.position = request.data['position']

        # อัพเดทรูปภาพ
        if 'image' in request.data:
            # ลบรูปเก่า
            if stocked_image.image:
                stocked_image.image.delete()
            stocked_image.image = request.data['image']

        stocked_image.save()

        return Response(
            {"message": "Stocked image updated successfully"},
            status=status.HTTP_200_OK
        )

# delete stocked
class DeleteStockedView(APIView):
    @swagger_auto_schema(
        tags=["Stocked"],
        operation_description="Delete a stocked item and all related products",
        responses={
            200: "Success",
            404: "Not found"
        }
    )
    def delete(self, request, pk):
        try:
            stocked = Stocked.objects.get(pk=pk)
        except Stocked.DoesNotExist:
            return Response(
                {"message": "Stocked not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Get all StockedImages
        stocked_images = stocked.images.all()
        
        # For each StockedImage, delete related products first
        for stocked_image in stocked_images:
            # Get and delete all products related to this stocked image
            products = GoodsModel.objects.filter(stocked_image=stocked_image)
            for product in products:
                # Delete related Size instances
                SizeModel.objects.filter(product=product).delete()
                
                # Delete related Color instances
                ColorModel.objects.filter(product=product).delete()
                
                # Delete related ProductImage instances
                ProductImage.objects.filter(product=product).delete()
                
                # Delete the Product instance
                product.delete()

            # Delete the physical image file
            if stocked_image.image:
                stocked_image.image.delete()
            
            # Delete the StockedImage record
            stocked_image.delete()

        # Finally delete the Stocked instance
        stocked.delete()

        return Response(
            {"message": "Stocked and all related data deleted successfully"}, 
            status=status.HTTP_200_OK
        )

class ProductsByAreaView(APIView):
    @swagger_auto_schema(
        tags=["Store Products"],
        manual_parameters=[
            openapi.Parameter('start_x', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('end_x', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('start_y', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('end_y', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True),
        ],
        responses={200: OnlyStoreGoodsSerializer(many=True)}
    )
    def get(self, request, stocked_image_id):
        try:
            # Get coordinates from query params
            start_x = float(request.query_params.get('start_x'))
            end_x = float(request.query_params.get('end_x'))
            start_y = float(request.query_params.get('start_y'))
            end_y = float(request.query_params.get('end_y'))

            # Get all products for the stocked image
            products = GoodsModel.objects.filter(stocked_image_id=stocked_image_id)
            
            # Filter products manually
            filtered_products = []
            for product in products:
                try:
                    if product.x_axis and product.y_axis:
                        # Get coordinates from JSONField
                        x_coords = product.x_axis
                        y_coords = product.y_axis
                        
                        # Check if coordinates are within range
                        if (isinstance(x_coords, list) and isinstance(y_coords, list) and
                            len(x_coords) == 2 and len(y_coords) == 2):
                            if (start_x <= max(x_coords) and end_x >= min(x_coords) and
                                start_y <= max(y_coords) and end_y >= min(y_coords)):
                                filtered_products.append(product)
                except (TypeError, ValueError, IndexError):
                    continue

            serializer = OnlyStoreGoodsSerializer(filtered_products, many=True)
            return Response(serializer.data)

        except ValueError:
            return Response(
                {"error": "Invalid coordinate values"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class StoreListView(generics.ListAPIView):
    queryset = StoreModel.objects.all()
    serializer_class = StoreSerializer

    @swagger_auto_schema(
        tags=["Store information"],
        responses={200: StoreSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class StoreGoodsView(APIView):
    @swagger_auto_schema(
        tags=["Store information & product registration"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'goods_set': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'category': openapi.Schema(type=openapi.TYPE_STRING),
                            'sizes': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            ),
                            'colors': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            ),
                            'images': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            ),
                        }
                    )
                ),
            }
        ),
        responses={201: "Created"}
    )
    def post(self, request, store_id):
        """
        เพิ่มสินค้าใหม่เข้าร้านค้า
        """
        try:
            store = get_object_or_404(StoreModel, id=store_id)
            
            # ตรวจสอบสิทธิ์
            if request.user != store.seller and not request.user.is_admin:
                return Response(
                    {"error": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            if not request.data.get("goods_set"):
                return Response(
                    {"error": "No goods data provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            response_data = []
            
            for data in request.data.get("goods_set"):
                serializer = GoodsCreateSerializer(data=data)
                category, _ = CategoryModel.objects.get_or_create(
                    name=data.get("category")
                )

                if serializer.is_valid():
                    instance = serializer.save(
                        store=store,
                        category=category
                    )
                    
                    # สร้าง sizes
                    for size in data.get("sizes", []):
                        SizeModel.objects.create(
                            product=instance,
                            name=size
                        )

                    # สร้าง colors
                    for color in data.get("colors", []):
                        ColorModel.objects.create(
                            product=instance,
                            name=color
                        )

                    # จัดการรูปภาพ
                    for image_data in data.get("images", []):
                        try:
                            if ';base64,' in image_data:
                                format, imgstr = image_data.split(';base64,')
                                ext = format.split('/')[-1]
                            else:
                                imgstr = image_data
                                ext = 'jpg'
                            
                            padding = len(imgstr) % 4
                            if padding:
                                imgstr += '=' * (4 - padding)

                            file_data = ContentFile(
                                base64.b64decode(imgstr),
                                name=f"{uuid.uuid4()}.{ext}"
                            )
                            ProductImage.objects.create(
                                product=instance,
                                image=file_data
                            )
                        except Exception as e:
                            print(f"Error processing image: {str(e)}")
                            continue

                    response_data.append(GoodsSerializer(instance).data)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                response_data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class StoreBannerListCreateView(generics.ListCreateAPIView):
    serializer_class = StoreBannerSerializer
    
    def get_queryset(self):
        return StoreBanner.objects.filter(store_id=self.kwargs['store_id'])
    
    def perform_create(self, serializer):
        store = get_object_or_404(StoreModel, id=self.kwargs['store_id'])
        
        # ตรวจสอบว่ามี banner อยู่แล้วหรือไม่
        existing_banner = StoreBanner.objects.filter(store=store).first()
        if existing_banner:
            # ถ้ามี banner อยู่แล้ว ให้ลบรูปเก่า
            if existing_banner.image:
                existing_banner.image.delete()
            existing_banner.delete()
            
        # สร้าง banner ใหม่
        serializer.save(store=store)

class StoreBannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StoreBanner.objects.all()
    serializer_class = StoreBannerSerializer
    
    def perform_update(self, serializer):
        # ลบรูปเก่าก่อนอัพเดทรูปใหม่
        instance = self.get_object()
        if instance.image and hasattr(serializer.validated_data, 'image'):
            instance.image.delete()
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.image:
            instance.image.delete()
        instance.delete()

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_store_for_seller(request):
    serializer = CreateStoreSerializer(data=request.data)
    if serializer.is_valid():
        seller = UserModel.objects.get(id=serializer.validated_data['seller_id'])
        store = serializer.save(seller=seller)
        return Response({
            'message': 'Store created successfully',
            'store': {
                'id': store.id,
                'name': store.name,
                'address': store.address,
                'phone': store.phone,
                'seller_id': store.seller.id
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            store = StoreModel.objects.get(pk=pk)
            return Response({
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "phone": store.phone,
                "company_number": store.company_number,
                "sub_address": store.sub_address,
                "introduce": store.introduce,
                "seller": store.seller.id
            })
        except StoreModel.DoesNotExist:
            return Response({
                "message": "Store not found"
            }, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            store = StoreModel.objects.get(pk=pk)
            
            # Check if user has permission to update
            if not request.user.is_admin and request.user != store.seller:
                return Response({
                    "message": "You don't have permission to update this store"
                }, status=status.HTTP_403_FORBIDDEN)
                
            serializer = UpdateStoreSerializer(
                store,
                data=request.data,
                partial=True  # Allow partial updates
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except StoreModel.DoesNotExist:
            return Response({
                "message": "Store not found"
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            store = StoreModel.objects.get(pk=pk)
            
            # Check if user has permission to delete
            if not request.user.is_admin and request.user != store.seller:
                return Response({
                    "message": "You don't have permission to delete this store"
                }, status=status.HTTP_403_FORBIDDEN)
                
            store.delete()
            return Response({
                "message": "Store deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
            
        except StoreModel.DoesNotExist:
            return Response({
                "message": "Store not found"
            }, status=status.HTTP_404_NOT_FOUND)

class Mode3DUpdateView(APIView):
    permission_classes = []  # Remove authentication requirement for GET
    
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated()]  # Require authentication for PATCH
        return []  # No authentication required for GET

    @swagger_auto_schema(
        tags=["Store 3D Mode"],
        request_body=Mode3DSerializer,
        responses={
            200: openapi.Response("Success", Mode3DSerializer),
            404: "Store not found",
            403: "Permission denied"
        }
    )
    def patch(self, request, store_id):
        try:
            store = StoreModel.objects.get(id=store_id)
            
            # Check permissions
            if request.user != store.seller and not request.user.is_admin:
                return Response(
                    {"error": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get or create Mode3D instance
            mode_3d, created = Mode3D.objects.get_or_create(store=store)
            
            # Update the is_enabled field
            serializer = Mode3DSerializer(mode_3d, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except StoreModel.DoesNotExist:
            return Response(
                {"error": "Store not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        tags=["Store 3D Mode"],
        responses={
            200: Mode3DSerializer,
            404: "Store not found"
        }
    )
    def get(self, request, store_id):
        try:
            store = StoreModel.objects.get(id=store_id)
            mode_3d, created = Mode3D.objects.get_or_create(store=store)
            serializer = Mode3DSerializer(mode_3d)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except StoreModel.DoesNotExist:
            return Response(
                {"error": "Store not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


