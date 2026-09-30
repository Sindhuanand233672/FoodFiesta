import razorpay
import uuid
from django.conf import settings
from django.db import transaction
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q



from .models import (
    Customer,
    Restaurant,
    Item,
    Cart,
    CartItem,
    Order,
    OrderItem
)


def admin_required(request):
    return request.session.get('role') == 'admin'


def customer_required(request):
    return request.session.get('role') == 'customer'


# =========================
# PUBLIC
# =========================

def index(request):
    return render(request, 'delivery/index.html')

def about(request):
    return render(request, 'delivery/about.html')


def open_signup(request):
    return render(request, 'delivery/signup.html')


def open_signin(request):
    return render(request, 'delivery/signin.html')


# =========================
# SIGNUP
# =========================

def signup(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Customer.objects.get(username=username)
            return HttpResponse("Duplicate username!")

        except Customer.DoesNotExist:

            Customer.objects.create(
                username=username,
                password=password,
                email=email,
                mobile=mobile,
                address=address
            )

        return render(request, 'delivery/signin.html')


# =========================
# SIGNIN
# =========================

def signin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:

            Customer.objects.get(
                username=username,
                password=password
            )

            request.session['username'] = username

            # ADMIN
            if username == 'admin':

                request.session['role'] = 'admin'

                restaurants = Restaurant.objects.all()

                restaurant_count = restaurants.count()
                item_count = Item.objects.count()

                if restaurants.exists():

                    total_rating = sum(
                        restaurant.rating
                        for restaurant in restaurants
                    )

                    average_rating = round(
                        total_rating / restaurant_count,
                        1
                    )

                else:
                    average_rating = 0

                return render(
                    request,
                    'delivery/admin_home.html',
                    {
                        'restaurant_count': restaurant_count,
                        'item_count': item_count,
                        'average_rating': average_rating
                    }
                )

            # CUSTOMER
            request.session['role'] = 'customer'

            restaurantList = Restaurant.objects.all()

            return render(
                request,
                'delivery/customer_home.html',
                {
                    'restaurantList': restaurantList,
                    'username': username
                }
            )

        except Customer.DoesNotExist:

            return HttpResponse("Registration failed")


# =========================
# LOGOUT
# =========================

def logout_user(request):

    request.session.flush()

    return redirect('index')


# =========================
# RESTAURANTS
# =========================

def open_show_restaurant(request):

    restaurantList = Restaurant.objects.all()

    search_query = request.GET.get('q', '').strip()

    if search_query:

        restaurantList = restaurantList.filter(
            Q(name__icontains=search_query) |
            Q(cuisine__icontains=search_query)
        )

    return render(
        request,
        'delivery/show_restaurants.html',
        {
            'restaurantList': restaurantList,
            'role': request.session.get('role', 'customer'),
            'search_query': search_query
        }
    )


# =========================
# ADMIN - ADD RESTAURANT
# =========================

def open_add_restaurant(request):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    return render(
        request,
        'delivery/add_restaurant.html'
    )


def add_restaurant(request):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    if request.method == 'POST':

        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        try:

            Restaurant.objects.get(name=name)

            return HttpResponse(
                "Duplicate restaurant!"
            )

        except Restaurant.DoesNotExist:

            Restaurant.objects.create(
                name=name,
                picture=picture,
                cuisine=cuisine,
                rating=rating
            )

    restaurants = Restaurant.objects.all()

    restaurant_count = restaurants.count()
    item_count = Item.objects.count()

    if restaurants.exists():

        total_rating = sum(
            restaurant.rating
            for restaurant in restaurants
        )

        average_rating = round(
            total_rating / restaurant_count,
            1
        )

    else:

        average_rating = 0

    return render(
        request,
        'delivery/admin_home.html',
        {
            'restaurant_count': restaurant_count,
            'item_count': item_count,
            'average_rating': average_rating
        }
    )


# =========================
# ADMIN - UPDATE RESTAURANT
# =========================

def open_update_restaurant(request, restaurant_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    return render(
        request,
        'delivery/update_restaurant.html',
        {
            'restaurant': restaurant
        }
    )


def update_restaurant(request, restaurant_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    if request.method == 'POST':

        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')

        restaurant.save()

    return redirect('open_show_restaurant')


# =========================
# ADMIN - DELETE RESTAURANT
# =========================

def delete_restaurant(request, restaurant_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    restaurant.delete()

    return redirect('open_show_restaurant')


# =========================
# CUSTOMER - ALL FOOD
# =========================

def open_customer_menu(request):

    if not customer_required(request):
        return HttpResponse("Customer access required.")

    itemList = Item.objects.select_related(
        'restaurant'
    ).all()

    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    category = request.GET.get(
        'category',
        ''
    ).strip()

    if search_query:

        itemList = itemList.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(restaurant__name__icontains=search_query) |
            Q(restaurant__cuisine__icontains=search_query)
        )

    if category:

        keywords = {
            'Pizza': ['pizza'],
            'Burgers': ['burger'],
            'Indian': [
                'indian',
                'dosa',
                'idli',
                'biryani'
            ],
            'Chinese': [
                'chinese',
                'noodles',
                'wok'
            ],
            'Beverages': [
                'beverage',
                'coffee',
                'drink',
                'juice'
            ],
            'Desserts': [
                'dessert',
                'cake',
                'ice cream',
                'sweet'
            ]
        }

        selected_words = keywords.get(
            category,
            []
        )

        if selected_words:

            category_query = Q()

            for word in selected_words:

                category_query |= (
                    Q(name__icontains=word) |
                    Q(description__icontains=word) |
                    Q(restaurant__cuisine__icontains=word)
                )

            itemList = itemList.filter(
                category_query
            )

    return render(
        request,
        'delivery/customer_menu.html',
        {
            'itemList': itemList,
            'search_query': search_query,
            'category': category
        }
    )


# =========================
# CUSTOMER - RESTAURANT MENU
# =========================

def open_customer_restaurant_menu(
    request,
    restaurant_id
):

    if not customer_required(request):
        return HttpResponse("Customer access required.")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    itemList = Item.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        'delivery/customer_restaurant_menu.html',
        {
            'restaurant': restaurant,
            'itemList': itemList
        }
    )


# =========================
# ADMIN - MENU MANAGEMENT
# =========================

def open_update_menu(request, restaurant_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    itemList = Item.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        'delivery/update_menu.html',
        {
            'restaurant': restaurant,
            'itemList': itemList
        }
    )


def update_menu(request, restaurant_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegetarian = (
            request.POST.get('vegetarian') == 'on'
        )
        picture = request.POST.get('picture')

        try:

            Item.objects.get(
                restaurant=restaurant,
                name=name
            )

            return HttpResponse(
                "Duplicate Item!"
            )

        except Item.DoesNotExist:

            Item.objects.create(
                restaurant=restaurant,
                name=name,
                description=description,
                price=price,
                vegetarian=vegetarian,
                picture=picture
            )

    return redirect(
        'open_update_menu',
        restaurant_id=restaurant_id
    )


def edit_menu_item(request, item_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    item = Item.objects.get(
        id=item_id
    )

    if request.method == 'POST':

        item.name = request.POST.get('name')
        item.description = request.POST.get(
            'description'
        )
        item.price = request.POST.get('price')
        item.vegetarian = (
            request.POST.get('vegetarian') == 'on'
        )
        item.picture = request.POST.get(
            'picture'
        )

        item.save()

        return redirect(
            'open_update_menu',
            restaurant_id=item.restaurant.id
        )

    return render(
        request,
        'delivery/edit_menu_item.html',
        {
            'item': item
        }
    )


def delete_menu_item(request, item_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    item = Item.objects.get(
        id=item_id
    )

    restaurant_id = item.restaurant.id

    item.delete()

    return redirect(
        'open_update_menu',
        restaurant_id=restaurant_id
    )


# =========================
# CART
# =========================

def add_to_cart(request, item_id):

    if request.method != 'POST':
        return HttpResponse("Invalid request.")

    if not customer_required(request):
        return HttpResponse("Customer access required.")

    username = request.session.get(
        'username'
    )

    customer = Customer.objects.get(
        username=username
    )

    item = Item.objects.get(
        id=item_id
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item
    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect(
        'open_customer_restaurant_menu',
        restaurant_id=item.restaurant.id
    )


def open_cart(request):

    if not customer_required(request):
        return HttpResponse("Customer access required.")

    username = request.session.get(
        'username'
    )

    customer = Customer.objects.get(
        username=username
    )

    try:

        cart = Cart.objects.get(
            customer=customer
        )

        cart_items = CartItem.objects.filter(
            cart=cart
        )

        cart_total = sum(
            cart_item.total_price()
            for cart_item in cart_items
        )

    except Cart.DoesNotExist:

        cart = None
        cart_items = []
        cart_total = 0

    return render(
        request,
        'delivery/cart.html',
        {
            'cart': cart,
            'cart_items': cart_items,
            'cart_total': cart_total
        }
    )


def remove_from_cart(
    request,
    cart_item_id
):

    if request.method != 'POST':
        return HttpResponse("Invalid request.")

    if not customer_required(request):
        return HttpResponse("Customer access required.")

    username = request.session.get(
        'username'
    )

    customer = Customer.objects.get(
        username=username
    )

    cart_item = CartItem.objects.get(
        id=cart_item_id,
        cart__customer=customer
    )

    cart_item.delete()

    return redirect('open_cart')


# =========================
# CHECKOUT
# =========================

@require_POST
def checkout(request):
    if not customer_required(request):
        return HttpResponse("Customer access required.")

    username = request.session.get('username')
    customer = Customer.objects.get(username=username)

    try:
        cart = Cart.objects.get(customer=customer)
    except Cart.DoesNotExist:
        return HttpResponse("Your cart is empty.")

    cart_items = list(
        CartItem.objects.filter(cart=cart).select_related('item')
    )

    if not cart_items:
        return HttpResponse("Your cart is empty.")

    total_amount = sum(
        cart_item.total_price() for cart_item in cart_items
    )

    amount_paise = round(total_amount * 100)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    razorpay_order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": f"ff_{uuid.uuid4().hex}",
    })

    with transaction.atomic():
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            status='Pending',
            razorpay_order_id=razorpay_order['id']
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=cart_item.item.price
            )

    return render(
        request,
        'delivery/payment.html',
        {
            'order': order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'amount_paise': amount_paise,
            'customer': customer
        }
    )

@require_POST
def verify_payment(request):
    if not customer_required(request):
        return HttpResponse("Customer access required.")

    payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
    order_id = request.POST.get('order_id')

    if not all([payment_id, razorpay_order_id, signature, order_id]):
        return HttpResponse("Payment details are incomplete.")

    username = request.session.get('username')
    customer = Customer.objects.get(username=username)

    try:
        order = Order.objects.get(
            id=order_id,
            customer=customer,
            razorpay_order_id=razorpay_order_id,
            status='Pending'
        )
    except Order.DoesNotExist:
        return HttpResponse("Order not found or already processed.")

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )
    

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
    except Exception:
        return HttpResponse("Payment verification failed.")
    
    payment = client.payment.fetch(payment_id)

    if (
        payment.get('order_id') != razorpay_order_id
        or payment.get('status') != 'captured'
    ):
        return HttpResponse("Payment is not captured.")

    with transaction.atomic():
        order.razorpay_payment_id = payment_id
        order.status = 'Confirmed'
        order.save(update_fields=[
            'razorpay_payment_id',
            'status'
        ])

        CartItem.objects.filter(
            cart__customer=customer
        ).delete()

    return render(
        request,
        'delivery/order_success.html',
        {'order': order}
    )



# =========================
# MY ORDERS
# =========================

def open_orders(request):

    if not customer_required(request):
        return HttpResponse("Customer access required.")

    username = request.session.get(
        'username'
    )

    customer = Customer.objects.get(
        username=username
    )

    orders = Order.objects.filter(
        customer=customer
    ).order_by('-created_at')

    return render(
        request,
        'delivery/orders.html',
        {
            'orders': orders
        }
    )
    

# =========================
# ADMIN - ORDER MANAGEMENT
# =========================

def admin_orders(request):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    orders = Order.objects.select_related(
        'customer'
    ).order_by('-created_at')

    status_choices = [
        'Pending',
        'Confirmed',
        'Preparing',
        'Out for delivery',
        'Delivered',
        'Cancelled'
    ]

    return render(
        request,
        'delivery/admin_orders.html',
        {
            'orders': orders,
            'status_choices': status_choices
        }
    )


def update_order_status(request, order_id):

    if not admin_required(request):
        return HttpResponse("Access denied. Admins only.")

    if request.method != 'POST':
        return HttpResponse("Invalid request.")

    status = request.POST.get('status')

    allowed_statuses = [
        'Pending',
        'Confirmed',
        'Preparing',
        'Out for delivery',
        'Delivered',
        'Cancelled'
    ]

    if status not in allowed_statuses:
        return HttpResponse("Invalid order status.")

    try:
        order = Order.objects.get(id=order_id)

    except Order.DoesNotExist:
        return HttpResponse("Order not found.")

    order.status = status
    order.save(update_fields=['status'])

    return redirect('admin_orders')

# =========================
# SMART LEFTOVER COMPANION
# =========================

def smart_leftover_companion(request):

    if not customer_required(request):
        return redirect('open_signin')

    recipes = [
        {
            'name': 'Tomato Rice',
            'description': 'A simple, flavourful rice dish.',
            'ingredients': [
                'rice', 'tomato', 'onion', 'oil', 'salt'
            ],
            'time': '20 minutes',
            'vegetarian': True,
        },
        {
            'name': 'Vegetable Fried Rice',
            'description': 'Quick fried rice with vegetables.',
            'ingredients': [
                'rice', 'carrot', 'beans', 'onion',
                'soy sauce', 'oil'
            ],
            'time': '25 minutes',
            'vegetarian': True,
        },
        {
            'name': 'Masala Omelette',
            'description': 'An omelette with onion and spices.',
            'ingredients': [
                'egg', 'onion', 'tomato', 'salt', 'oil'
            ],
            'time': '10 minutes',
            'vegetarian': False,
        },
        {
            'name': 'Onion Dosa',
            'description': 'Crispy dosa topped with onion.',
            'ingredients': [
                'dosa batter', 'onion', 'oil', 'salt'
            ],
            'time': '15 minutes',
            'vegetarian': True,
        },
        {
            'name': 'Aloo Fry',
            'description': 'Spiced potato fry.',
            'ingredients': [
                'potato', 'onion', 'chilli', 'oil', 'salt'
            ],
            'time': '25 minutes',
            'vegetarian': True,
        },
        {
            'name': 'Paneer Bhurji',
            'description': 'Scrambled paneer with spices.',
            'ingredients': [
                'paneer', 'tomato', 'onion', 'oil', 'salt'
            ],
            'time': '20 minutes',
            'vegetarian': True,
        },
        {
            'name': 'Banana Pancakes',
            'description': 'Easy pancakes made with banana.',
            'ingredients': [
                'banana', 'flour', 'milk', 'egg', 'sugar'
            ],
            'time': '15 minutes',
            'vegetarian': False,
        },
        {
            'name': 'Lemon Rice',
            'description': 'Tangy rice with lemon.',
            'ingredients': [
                'rice', 'lemon', 'oil', 'salt', 'peanuts'
            ],
            'time': '15 minutes',
            'vegetarian': True,
        },
                # ==================== PASTA ====================

        {
            'name': 'White Sauce Pasta',
            'description': 'Creamy pasta with a rich white sauce.',
            'ingredients': [
                'pasta', 'milk', 'butter', 'flour',
                'cheese', 'garlic', 'salt', 'pepper'
            ],
            'time': '25 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Red Sauce Pasta',
            'description': 'Italian-style pasta in a tangy tomato sauce.',
            'ingredients': [
                'pasta', 'tomato', 'onion', 'garlic',
                'olive oil', 'chilli flakes', 'salt'
            ],
            'time': '25 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Mushroom Alfredo Pasta',
            'description': 'Creamy Alfredo pasta with sautéed mushrooms.',
            'ingredients': [
                'pasta', 'mushroom', 'cream', 'milk',
                'butter', 'garlic', 'cheese', 'salt'
            ],
            'time': '30 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Chicken Pasta',
            'description': 'Pasta tossed with seasoned chicken.',
            'ingredients': [
                'pasta', 'chicken', 'tomato', 'onion',
                'garlic', 'oil', 'pepper', 'salt'
            ],
            'time': '35 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Mac and Cheese',
            'description': 'Comforting macaroni coated in cheesy sauce.',
            'ingredients': [
                'macaroni', 'milk', 'butter',
                'cheese', 'flour', 'salt', 'pepper'
            ],
            'time': '20 minutes',
            'vegetarian': True,
        },

        # ==================== PIZZA ====================

        {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza topped with tomato and cheese.',
            'ingredients': [
                'pizza dough', 'tomato', 'cheese',
                'oregano', 'olive oil', 'salt'
            ],
            'time': '30 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Mushroom Pizza',
            'description': 'Cheesy pizza topped with fresh mushrooms.',
            'ingredients': [
                'pizza dough', 'mushroom', 'cheese',
                'tomato', 'garlic', 'oregano'
            ],
            'time': '35 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Chicken Pizza',
            'description': 'Pizza topped with chicken and melted cheese.',
            'ingredients': [
                'pizza dough', 'chicken', 'cheese',
                'tomato', 'onion', 'capsicum', 'oregano'
            ],
            'time': '40 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Veggie Pizza',
            'description': 'Colorful vegetable pizza with a cheesy topping.',
            'ingredients': [
                'pizza dough', 'tomato', 'onion',
                'capsicum', 'corn', 'cheese', 'oregano'
            ],
            'time': '35 minutes',
            'vegetarian': True,
        },

        # ==================== CAKES & DESSERTS ====================

        {
            'name': 'Chocolate Cake',
            'description': 'Soft chocolate cake for chocolate lovers.',
            'ingredients': [
                'flour', 'cocoa powder', 'sugar',
                'milk', 'butter', 'baking powder'
            ],
            'time': '45 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Vanilla Cake',
            'description': 'A soft and fluffy vanilla-flavoured cake.',
            'ingredients': [
                'flour', 'sugar', 'milk', 'butter',
                'vanilla essence', 'baking powder'
            ],
            'time': '40 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Banana Cake',
            'description': 'Moist cake made with ripe bananas.',
            'ingredients': [
                'banana', 'flour', 'sugar',
                'butter', 'milk', 'baking powder'
            ],
            'time': '45 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Chocolate Mug Cake',
            'description': 'A quick chocolate cake made in a mug.',
            'ingredients': [
                'flour', 'cocoa powder', 'sugar',
                'milk', 'oil', 'baking powder'
            ],
            'time': '5 minutes',
            'vegetarian': True,
        },

        # ==================== CHICKEN ====================

        {
            'name': 'Chicken Curry',
            'description': 'Chicken simmered in a spiced onion-tomato gravy.',
            'ingredients': [
                'chicken', 'onion', 'tomato', 'ginger',
                'garlic', 'chilli powder', 'oil', 'salt'
            ],
            'time': '45 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Chicken Fried Rice',
            'description': 'Stir-fried rice with chicken and vegetables.',
            'ingredients': [
                'rice', 'chicken', 'carrot', 'beans',
                'onion', 'soy sauce', 'oil', 'pepper'
            ],
            'time': '30 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Chicken Pepper Fry',
            'description': 'Spicy chicken tossed with freshly ground pepper.',
            'ingredients': [
                'chicken', 'onion', 'pepper',
                'ginger', 'garlic', 'oil', 'salt'
            ],
            'time': '35 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Chicken Sandwich',
            'description': 'A quick sandwich filled with seasoned chicken.',
            'ingredients': [
                'bread', 'chicken', 'mayonnaise',
                'onion', 'tomato', 'pepper', 'salt'
            ],
            'time': '20 minutes',
            'vegetarian': False,
        },

        # ==================== FISH & SEAFOOD ====================

        {
            'name': 'Fish Fry',
            'description': 'Crispy fish coated with Indian spices.',
            'ingredients': [
                'fish', 'chilli powder', 'turmeric',
                'lemon', 'oil', 'salt'
            ],
            'time': '25 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Fish Curry',
            'description': 'Fish cooked in a tangy and spicy gravy.',
            'ingredients': [
                'fish', 'onion', 'tomato', 'chilli',
                'turmeric', 'tamarind', 'oil', 'salt'
            ],
            'time': '35 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Garlic Butter Fish',
            'description': 'Pan-seared fish with garlic butter.',
            'ingredients': [
                'fish', 'butter', 'garlic',
                'lemon', 'pepper', 'salt'
            ],
            'time': '20 minutes',
            'vegetarian': False,
        },

        # ==================== MUSHROOM ====================

        {
            'name': 'Mushroom Masala',
            'description': 'Mushrooms cooked in a flavourful masala gravy.',
            'ingredients': [
                'mushroom', 'onion', 'tomato',
                'ginger', 'garlic', 'chilli powder', 'oil', 'salt'
            ],
            'time': '30 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Garlic Mushroom',
            'description': 'Mushrooms sautéed with garlic and butter.',
            'ingredients': [
                'mushroom', 'garlic', 'butter',
                'pepper', 'salt', 'parsley'
            ],
            'time': '15 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Mushroom Fried Rice',
            'description': 'Fried rice with mushrooms and vegetables.',
            'ingredients': [
                'rice', 'mushroom', 'carrot',
                'onion', 'soy sauce', 'garlic', 'oil'
            ],
            'time': '25 minutes',
            'vegetarian': True,
        },

        # ==================== OTHER DISHES ====================

        {
            'name': 'Vegetable Sandwich',
            'description': 'Toasted sandwich with fresh vegetables.',
            'ingredients': [
                'bread', 'tomato', 'onion',
                'cucumber', 'butter', 'cheese'
            ],
            'time': '15 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Veggie Burger',
            'description': 'A vegetable patty served in a burger bun.',
            'ingredients': [
                'burger bun', 'potato', 'carrot',
                'peas', 'onion', 'cheese', 'mayonnaise'
            ],
            'time': '35 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Egg Fried Rice',
            'description': 'Quick fried rice with scrambled eggs.',
            'ingredients': [
                'rice', 'egg', 'onion', 'carrot',
                'soy sauce', 'oil', 'pepper', 'salt'
            ],
            'time': '20 minutes',
            'vegetarian': False,
        },

        {
            'name': 'Potato Cheese Balls',
            'description': 'Crispy potato bites filled with melted cheese.',
            'ingredients': [
                'potato', 'cheese', 'flour',
                'bread crumbs', 'oil', 'salt', 'pepper'
            ],
            'time': '30 minutes',
            'vegetarian': True,
        },

        {
            'name': 'Corn Cheese Sandwich',
            'description': 'Toasted sandwich with sweet corn and cheese.',
            'ingredients': [
                'bread', 'corn', 'cheese',
                'butter', 'pepper', 'salt'
            ],
            'time': '15 minutes',
            'vegetarian': True,
        },
    ]

    ingredient_input = request.GET.get(
        'ingredients', ''
    ).strip()

    available_ingredients = {
        ingredient.strip().lower()
        for ingredient in ingredient_input.split(',')
        if ingredient.strip()
    }

    matching_recipes = []

    if available_ingredients:

        for recipe in recipes:

            recipe_ingredients = set(
                recipe['ingredients']
            )

            matched = sorted(
                available_ingredients & recipe_ingredients
            )

            missing = sorted(
                recipe_ingredients - available_ingredients
            )

            if matched:
                matching_recipes.append({
                    **recipe,
                    'matched': matched,
                    'missing': missing,
                    'match_count': len(matched),
                })

        matching_recipes.sort(
            key=lambda recipe: recipe['match_count'],
            reverse=True
        )

    return render(
        request,
        'delivery/smart_leftover.html',
        {
            'ingredient_input': ingredient_input,
            'matching_recipes': matching_recipes,
            'searched': bool(ingredient_input),
        }
    )