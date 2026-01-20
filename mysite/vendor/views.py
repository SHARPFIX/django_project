from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from vendor.models import Vendor, Sale
from products.models import Product, Category

import uuid


# =====================================================
#               VENDOR SIGNUP
# =====================================================
def vendor_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        shop_name = request.POST['shop_name']
        contact_number = request.POST['contact_number']
        address = request.POST['address']

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('vendor_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('vendor_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('vendor_signup')

        user = User.objects.create_user(username=username, email=email, password=password)

        Vendor.objects.create(
            user=user,
            shop_name=shop_name,
            contact_number=contact_number,
            address=address,
            vendor_id=str(uuid.uuid4())[:8]
        )

        messages.success(request, "Vendor created successfully! Login now.")
        return redirect('vendor_login')

    return render(request, 'vendor/vendor_signup.html')



# =====================================================
#               VENDOR LOGIN
# =====================================================
def vendor_login(request):
    if request.user.is_authenticated:
        if Vendor.objects.filter(user=request.user).exists():
            return redirect('vendor_dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if Vendor.objects.filter(user=user).exists():
                return redirect('vendor_dashboard')

            messages.error(request, "You are not registered as a vendor.")
            return redirect('vendor_login')

        messages.error(request, "Invalid username or password.")
        return redirect('vendor_login')

    return render(request, 'vendor/vendor_login.html')



# =====================================================
#               DASHBOARD
# =====================================================
@login_required
def vendor_dashboard(request):
    return render(request, "vendor/vendor_dashboard.html")



# =====================================================
#               ADD PRODUCT
# =====================================================
@login_required
def add_product(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "Vendor profile not found.")
        return redirect("vendor_login")

    categories = Category.objects.all()

    if request.method == 'POST':
        Product.objects.create(
            vendor=vendor,
            category=Category.objects.get(id=request.POST['category']),
            product_name=request.POST['product_name'],
            description=request.POST['description'],
            price=request.POST['price'],
            stock=request.POST['stock'],
            image1=request.FILES.get('image1'),
            image2=request.FILES.get('image2'),
            image3=request.FILES.get('image3'),
            image4=request.FILES.get('image4'),
        )
        messages.success(request, "Product added successfully!")
        return redirect('vendor_dashboard')

    return render(request, 'vendor/add_product.html', {'categories': categories})



# =====================================================
#               MY PRODUCTS
# =====================================================
@login_required
def my_products(request):
    vendor = Vendor.objects.get(user=request.user)
    products = Product.objects.filter(vendor=vendor).order_by('-created_at')
    return render(request, 'vendor/my_products.html', {'products': products})



# =====================================================
#               VENDOR SALES
# =====================================================
@login_required
def vendor_sales(request):
    vendor = Vendor.objects.get(user=request.user)
    sales = Sale.objects.filter(vendor=vendor).order_by('-sale_date')
    return render(request, 'vendor/vendor_sales.html', {'sales': sales})



# =====================================================
#               LOGOUT
# =====================================================
def vendor_logout(request):
    logout(request)
    return redirect('vendor_login')
