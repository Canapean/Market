from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('products/create/', ProductCreateView.as_view(), name='products_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='products_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='products_delete'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products_detail'),
    path('category/<int:id>/', ProductByCategoryListView.as_view(), name="products_by_category"),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]