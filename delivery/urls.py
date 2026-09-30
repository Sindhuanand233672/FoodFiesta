from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path(
        '',
        views.index,
        name='index'
    ),

    # ABOUT
    path(
        'about',
        views.about,
        name='about'
    ),

    # AUTH
    path(
        'open_signup',
        views.open_signup,
        name='open_signup'
    ),

    path(
        'open_signin',
        views.open_signin,
        name='open_signin'
    ),

    path(
        'signup',
        views.signup,
        name='signup'
    ),

    path('signin/', views.signin, name='signin'),

    path(
        'logout',
        views.logout_user,
        name='logout'
    ),

    # RESTAURANTS
    path(
        'open_show_restaurant',
        views.open_show_restaurant,
        name='open_show_restaurant'
    ),

    # ADMIN RESTAURANTS
    path(
        'open_add_restaurant',
        views.open_add_restaurant,
        name='open_add_restaurant'
    ),

    path(
        'add_restaurant',
        views.add_restaurant,
        name='add_restaurant'
    ),

    path(
        'open_update_restaurant/<int:restaurant_id>',
        views.open_update_restaurant,
        name='open_update_restaurant'
    ),

    path(
        'update_restaurant/<int:restaurant_id>',
        views.update_restaurant,
        name='update_restaurant'
    ),

    path(
        'delete_restaurant/<int:restaurant_id>',
        views.delete_restaurant,
        name='delete_restaurant'
    ),

    # CUSTOMER MENU
    path(
        'customer_menu',
        views.open_customer_menu,
        name='open_customer_menu'
    ),

    path(
        'customer_restaurant_menu/<int:restaurant_id>',
        views.open_customer_restaurant_menu,
        name='open_customer_restaurant_menu'
    ),

    # ADMIN MENU
    path(
        'open_update_menu/<int:restaurant_id>',
        views.open_update_menu,
        name='open_update_menu'
    ),

    path(
        'update_menu/<int:restaurant_id>',
        views.update_menu,
        name='update_menu'
    ),

    path(
        'edit_menu_item/<int:item_id>',
        views.edit_menu_item,
        name='edit_menu_item'
    ),

    path(
        'delete_menu_item/<int:item_id>',
        views.delete_menu_item,
        name='delete_menu_item'
    ),

    # CART
    path(
        'add_to_cart/<int:item_id>',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart',
        views.open_cart,
        name='open_cart'
    ),

    path(
        'remove_from_cart/<int:cart_item_id>',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # CHECKOUT
    path(
        'checkout',
        views.checkout,
        name='checkout'
    ),
    
    path(
    'verify_payment',
    views.verify_payment,
    name='verify_payment'
),

    # CUSTOMER ORDERS
    path(
        'orders',
        views.open_orders,
        name='open_orders'
    ),
    
    # SMART LEFTOVER COMPANION

    path(
    'smart-leftover/',
    views.smart_leftover_companion,
    name='smart_leftover_companion'
    ),
]