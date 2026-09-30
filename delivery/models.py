
from django.db import models


class Customer(models.Model):

    username = models.CharField(max_length=20)

    password = models.CharField(max_length=20)

    email = models.CharField(max_length=50)

    mobile = models.CharField(max_length=10)

    address = models.CharField(max_length=100)


class Restaurant(models.Model):

    name = models.CharField(max_length=20)

    picture = models.URLField(
        max_length=200,
        default="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
    )

    cuisine = models.CharField(max_length=200)

    rating = models.FloatField()


class Item(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.FloatField()

    vegetarian = models.BooleanField(default=False)
    
    is_grocery = models.BooleanField(default=False)

    picture = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Cart(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.customer.username


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"


class Order(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    total_amount = models.FloatField()

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    # Razorpay fields added
    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.FloatField()

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return self.item.name
    
class Recipe(models.Model):

    name = models.CharField(max_length=150)

    description = models.TextField()

    ingredients = models.TextField(
        help_text="Enter ingredients separated by commas"
    )

    cooking_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes"
    )

    instructions = models.TextField()

    picture = models.URLField(
        max_length=500,
        blank=True
    )

    vegetarian = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name