from django.contrib import admin
from django.urls import path, include
from delivery import views


urlpatterns = [

    # Custom Admin Order Management
    # MUST be before Django Admin
    path(
        'admin/orders/',
        views.admin_orders,
        name='admin_orders'
    ),

    path(
        'admin/orders/<int:order_id>/status/',
        views.update_order_status,
        name='update_order_status'
    ),

    # Django Admin
    path('admin/', admin.site.urls),

    # All Delivery App URLs
    path('', include('delivery.urls')),
]