from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from store import views
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet

router = DefaultRouter()
router.register(r'bank-accounts/detail', BankAccountViewSet)


urlpatterns = [
    path("all-stores", views.StoreViewSet.as_view({'get': 'list'}), name='store-list'),
    path("", views.GoodsView.as_view(), name="goods_list"),
    path("detail/<int:goods_id>", views.GoodsView.as_view(), name="goods_detail"),
    path("<int:store_id>", views.StoreView.as_view(), name="store"),
    path('product/create', views.CreateProductAPIView.as_view(), name='create-product'),
    path('product/create2', views.CreateProductView.as_view(), name='create-product'),
    # update product
    path('product/<int:pk>/update', views.UpdateProductAPIView.as_view(), name='update-product'),
    # delete product
    path('product/<int:pk>/delete', views.DeleteProductAPIView.as_view(), name='delete-product'),
    path(
        "goods", views.GoodsPatchView.as_view(), name="goods_change"
    ),
    # ດຶງຂໍ້ມູດສິນຄ້າເພີ່ມເຕີມ ແລະ ສາມາດອັບເດດຂໍ້ມູດສິນຄ້າໄດ້
    path(
        "goods/<int:goods_id>", views.GoodsView.as_view(), name="goods_detail"
    ),
    path("review/<int:pk>", views.ReviewView.as_view(), name="review"),
    path("order", views.OrderView.as_view(), name="order"),
    path('orders', views.OrderListView.as_view(), name='order-list'),
    path('order/create', views.OrderCreateAPIView.as_view(), name='order-create'),
    path('order/update/<int:pk>', views.OrderUpdateAPIView.as_view(), name='order-update'),
    path('order/update/china-url/<int:pk>', views.OrderUpdateChinaUrlAPIView.as_view(), name='order-update-china-url'),
    path('order/update/lao-url/<int:pk>', views.OrderUpdateLaoUrlAPIView.as_view(), name='order-update-lao-url'),
    path('order/update/order-bill/<int:pk>', views.OrderUpdateBillAPIView.as_view(), name='order-update-bill'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('user/<int:user_id>/order', views.UserOrderListView.as_view(), name='user-order-list'),
    path('order/delete/<int:pk>', views.OrderDeleteView.as_view(), name='delete-order'),
    path('order/pending/', views.PendingOrderListAPIView.as_view(), name='pending-orders'),
    path('order/processing/', views.ProcessingOrderListAPIView.as_view(), name='processing-orders'),
    path('order/shipped/', views.ShippedOrderListAPIView.as_view(), name='shipped-orders'),
    path('order/delivered/', views.DeliveredOrderListAPIView.as_view(), name='delivered-orders'),
    path("search", views.SearchView.as_view(), name="search"),
    path("check-review/<int:pk>", views.CheckReview.as_view(), name="CheckReview"),
    path("terms/<int:pk>", views.TermsAPI.as_view(), name="terms"),
    path("review/form/<int:pk>", views.review_form, name="review_form"),
    path("review/list/<int:pk>", views.review_list, name="review_list"),
    path('reviews', views.ReviewList.as_view(), name='review-list'),
    path('review/create', views.ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>', views.ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),
    path('reviews/by-product/<int:product_id>/user/<int:user_id>', views.ReviewByProductAndUserAPIView.as_view(), name='review-by-product-and-user'),
    path('product/<int:product_id>/review', views.ProductReviewListView.as_view(), name='product-reviews-list'),
    path("goods/list", views.goods_list, name="goods_list"),
    path("goods/detail/<int:goods_id>", views.goods_detail, name="goods_detail"),
    path("order/list", views.order_list, name="order_list"),
    path("setting", views.store_setting, name="store_setting"),
    path('bank-accounts', views.BankAccountListCreateAPIView.as_view(), name='bank-account-list-create'),
    path('bank-accounts/<int:pk>', views.BankAccountRetrieveUpdateDestroyAPIView.as_view(), name='bank-account-detail'),
    path('bank-accounts/<int:store_id>/has_bank_account', views.check_store_bank_account, name='check_store_bank_account'),
    path('', include(router.urls)),
    path('bank-accounts/update/<int:store_id>', views.BankAccountUpdateAPIView.as_view(), name='bank-account-update'),
    path("web-info", views.WebInfoListCreateAPIView.as_view(), name="web-info-list-create"),
    path("web-info/<int:pk>", views.WebInfoRetrieveUpdateAPIView.as_view(), name="edit-web-information"),
    path("notice", views.NoticeList.as_view(), name="list-notice"),
    path("notice/create", views.NoticeCreate.as_view(), name="list-notice"),
    path("notice/detail/<int:pk>", views.NoticeDetailDelete.as_view(), name="detail-notice"),
    path("notice/delete/<int:pk>", views.NoticeDetailDelete.as_view(), name="delete-notice"),
    path("notice/update/<int:pk>", views.NoticeUpdate.as_view(), name="update-notice"),
    # stocked
    path('stocked/<int:pk>', views.StockedDetailView.as_view(), name='stocked-detail'),
    # stocked image goods create
    path('<int:store_id>/stocked-image/<int:stocked_image_id>/goods', views.StoreStockedImageGoodsView.as_view(), name='store-stocked-image-goods'),
    # stocked image list create
    path('stocked/<int:stocked_id>/images', views.StockedImageListCreateView.as_view(), name='stocked-image-list-create'),
    # stocked image detail, can update and delete
    path('stocked/stocked-image/<int:pk>', views.StockedImageDetailView.as_view(), name='stocked-image-detail'),
    # ເພີ່ມ stocked
    path('<int:store_id>/stocked/create', views.StockedCreateView.as_view(), name='stocked-create'),
    # stocked list
    path('<int:store_id>/stocked', views.StoreStockedListView.as_view(), name='store-stocked-list'),
    # stocked update
    path('stocked/<int:pk>/update', views.StockedUpdateView.as_view(), name='stocked-update'),
    # stocked image goods list
    path('<int:store_id>/stocked-image/<int:stocked_image_id>/goods/list',
        views.StoreStockedImageGoodsListView.as_view(), 
        name='store-stocked-image-goods-list'),
    # stocked image goods update
    path('goods/<int:pk>/update',
        views.StoreStockedImageGoodsUpdateView.as_view(), 
        name='goods-update'),
    # delete stocked image
    path('stocked-image/<int:pk>/delete', views.DeleteStockedImageAPIView.as_view(), name='delete-stocked-image'),
    # update stocked image
    path('stocked-image/<int:pk>/update', views.UpdateStockedImageAPIView.as_view(), name='update-stocked-image'),
    # delete stocked
    path('stocked/<int:pk>/delete', views.DeleteStockedView.as_view(), name='delete-stocked'),
    # get products by coordinates and stocked image
    path('stocked-image/<int:stocked_image_id>/products/area/', 
         views.ProductsByAreaView.as_view(),
         name='products-by-area'),
    # get store list
    path('stores/', views.StoreListView.as_view(), name='store-list'),
    
    # add goods
    path('<int:store_id>/goods', views.StoreGoodsView.as_view(), name='store-goods'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
