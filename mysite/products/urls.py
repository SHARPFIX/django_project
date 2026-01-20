from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),

    # View Single Product
    path('<int:product_id>/', views.view_product, name='view_product'),

    # Cart
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Buy Now
    path('buy-now/<int:pk>/', views.buy_now, name='buy_now'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('place-order/', views.place_order, name='place_order'),

]
