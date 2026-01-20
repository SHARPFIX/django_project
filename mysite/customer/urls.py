from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.customer_signup, name='customer_signup'),
    path('login/', views.customer_login, name='customer_login'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path("profile/",views.customer_profile, name="customer_profile"),
    path('complete-profile/', views.complete_profile, name='complete_profile'),

]
