from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer
import uuid 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer

def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        address = request.POST.get('address')

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('customer_signup')

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('customer_signup')

        # Email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('customer_signup')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create Customer Profile
        Customer.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            city=city,
            postal_code=postal_code,
            address=address
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('customer_login')

    return render(request, 'customer/customer_signup.html')


def customer_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('customer_login')

    return render(request, 'customer/customer_login.html')


def customer_dashboard(request):
    return render(request, 'customer/customer_dashboard.html')


def customer_logout(request):
    logout(request)
    return redirect('customer_login')
@login_required
def customer_profile(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.username,
            "phone": "",
            "city": "",
            "postal_code": "",
            "address": "",
        }
    )

    return render(request, "customer/customer_profile.html", {
        "customer": customer
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer

@login_required
def complete_profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
        # If already exists → open form filled
    except Customer.DoesNotExist:
        customer = None

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")

        if customer:
            # update existing
            customer.full_name = full_name
            customer.phone = phone
            customer.address = address
            customer.city = city
            customer.postal_code = postal_code
            customer.save()
        else:
            # create new
            Customer.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
            )

        messages.success(request, "Profile updated successfully!")
        return redirect("/products/checkout/")

    return render(request, "customer/complete_profile.html", {
        "customer": customer,
    })
