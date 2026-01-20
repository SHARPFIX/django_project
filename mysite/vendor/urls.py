
from django.urls import path, include
from .import views
urlpatterns = [
   path('',views.vendor_login, name="vendor_login"),
   path('signup/', views.vendor_signup, name='vendor_signup'),
   path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
   path('add-product/', views.add_product, name='add_product'),
   path('logout/', views.vendor_logout, name='vendor_logout'),
   path('my-products/', views.my_products, name='my_products'),
   path('sales/', views.vendor_sales, name='vendor_sales'),


]