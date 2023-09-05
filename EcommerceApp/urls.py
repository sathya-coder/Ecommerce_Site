from django.urls import path, include
from EcommerceApp.views.Products import *
from EcommerceApp.views.User import *

urlpatterns = [
    path('api/products/',ProductList.as_view(), name='product-list'),
    path('api/register-for-user/', RegisterUser.as_view(), name='register-for-user'),
    path('api/register-list/', RegisterList.as_view(), name='register-list'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('api/products_all_list/', ProductAllList.as_view(), name='product-all-list'),
    path('api/products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('api/products/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('api/cart/add/', CartAddProduct.as_view(), name='cart-add'),
    path('api/cart/view/<int:user>/', CartView.as_view(), name='cart-view'),
    path('api/checkout/<int:user_id>/', CheckoutView.as_view(), name='checkout'),
    path('api/products/search/', ProductSearchView.as_view(), name='product-search'),
    path('api/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('api/products/<int:product_id>/reviews/', ProductReviewsListAPIView.as_view(), name='product-reviews-list'),
    path('api/variants/', ProductVariantListCreateAPIView.as_view(), name='variant-list-create'),
    path('api/products/<int:product_id>/variants/', ProductVariantsListAPIView.as_view(), name='product-variants-list'),
    path('api/password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('api/coupun-generation/', coupungeneration.as_view(), name='coupun-generation'),
    path('api/user-apply-coupun/', userapplycoupun.as_view(), name='user-apply-coupun'),
    path('api/coupun-list/', coupunlist.as_view(), name='coupun-list'),
]
