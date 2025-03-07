from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, CartItem
from django.contrib import messages

def index(request):
    """Display the homepage."""
    return render(request, 'store/index.html')

def shop(request):
    """Display all products grouped by category on the shop page."""
    categories = Category.objects.all()
    products_by_category = {category: Product.objects.filter(category=category) for category in categories}
    return render(request, 'store/shop.html', {
        'products_by_category': products_by_category,
    })

@login_required
def add_to_cart(request, product_id):
    """Add a product to the shopping cart."""
    product = get_object_or_404(Product, id=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f'Added another {product.name} in your cart')
    else:
        messages.success(request, f'{product.name} has been added to your cart')

    return redirect('store:shop')

@login_required
def cart(request):
    if request.method == "POST":
        user_cart = get_object_or_404(Cart, user=request.user)
        CartItem.objects.filter(cart=user_cart).delete()
        messages.success(request, "Order placed successfully! Your cart has been cleared.")
        return redirect("store:cart")
    
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)  # Updated this line
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        
        if new_quantity < 1:
            cart_item.delete()
            messages.warning(request, f"{cart_item.product.name} removed from cart")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.info(request, f"{cart_item.product.name} quantity updated")
    
    return redirect('store:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.warning(request, f"{product_name} removed from cart")
    return redirect('store:cart')

@login_required
def clear_cart(request):
    user_cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=user_cart).delete()
    messages.info(request, "Cart cleared successfully")
    return redirect('store:cart')