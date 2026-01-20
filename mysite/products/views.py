from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Cart, Order, OrderItem
from vendor.models import Sale
from customer.models import Customer


# =============================
# PRODUCT LIST
# =============================
def products_list(request):
    category_id = request.GET.get("category")
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
        selected = int(category_id)
    else:
        products = Product.objects.all()
        selected = None

    return render(request, "products/products_list.html", {
        "products": products,
        "categories": categories,
        "selected": selected,
    })


# =============================
# VIEW PRODUCT PAGE
# =============================
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/view_product.html", {"product": product})


# =============================
# ADD TO CART
# =============================
@login_required(login_url="customer_login")
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart!")
    return redirect("view_cart")


# =============================
# VIEW CART
# =============================
@login_required(login_url="customer_login")
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(i.product.price * i.quantity for i in cart_items)

    return render(request, "products/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


# =============================
# REMOVE FROM CART
# =============================
@login_required(login_url="customer_login")
def remove_from_cart(request, cart_id):
    Cart.objects.filter(id=cart_id, user=request.user).delete()
    messages.success(request, "Item removed.")
    return redirect("view_cart")


# =============================
# BUY NOW
# =============================
def buy_now(request, pk):
    if not request.user.is_authenticated:
        return redirect(f"/customer/login/?next=/products/buy-now/{pk}/")

    # Set session variable for single purchase
    request.session["buy_now_product"] = pk
    return redirect("checkout")


# =============================
# CHECKOUT PAGE
# =============================
@login_required(login_url="customer_login")
def checkout(request):
    # Detect BUY NOW vs CART checkout
    buy_now_id = request.session.get("buy_now_product")

    if buy_now_id:
        product = get_object_or_404(Product, id=buy_now_id)
        items = [
            {
                "product": product,
                "quantity": 1,
                "price": product.price
            }
        ]
        total = product.price
    else:
        cart_items = Cart.objects.filter(user=request.user)
        items = cart_items
        total = sum(i.product.price * i.quantity for i in cart_items)

    # Ensure customer profile exists
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.warning(request, "Please complete your profile before checkout.")
        return redirect("/customer/complete-profile/")

    return render(request, "products/checkout.html", {
        "items": items,
        "total": total,
        "customer": customer,
    })


# =============================
# PLACE ORDER
# =============================
@login_required(login_url="customer_login")
def place_order(request):
    if request.method != "POST":
        return redirect("checkout")

    # Check customer profile
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Please complete your profile first.")
        return redirect("/customer/complete-profile/")

    # BUY NOW checkout
    buy_now_id = request.session.get("buy_now_product")
    if buy_now_id:
        product = get_object_or_404(Product, id=buy_now_id)
        items = [{"product": product, "quantity": 1}]
        total = product.price
        # Clear session
        del request.session["buy_now_product"]
    else:
        # CART checkout
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect("view_cart")

        items = cart_items
        total = sum(i.product.price * i.quantity for i in cart_items)

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
    )

    for item in items:
        qty = item["quantity"] if isinstance(item, dict) else item.quantity
        prod = item["product"] if isinstance(item, dict) else item.product
        price = prod.price

        OrderItem.objects.create(
            order=order,
            product=prod,
            quantity=qty,
            price=price
        )

        Sale.objects.create(
            product=prod,
            vendor=prod.vendor,
            buyer=request.user,
            quantity=qty,
            total_price=price * qty
        )

    # Clear cart after checkout
    Cart.objects.filter(user=request.user).delete()

    return redirect("order_success")


# =============================
# ORDER SUCCESS PAGE
# =============================
def order_success(request):
    return render(request, "products/order_success.html")
