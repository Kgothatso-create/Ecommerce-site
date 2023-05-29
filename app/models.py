from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATE_CHOICES = {
    ('PLK','Polokwane'),
    ('GP','Gauteng'),
    ('MP','Mpumalanga'),
    ('NW','North-West'),
    ('EC','Easten-Cape'),
    ('WC','Western-Cape'),
    ('PE','Portelizabeth'),
}

CATEGORY_CHOICES={
    ('CR','Cream'),
    ('MS','Moisture'),
    ('CM','Combos'),
    ('WS','Wash'),
    ('SR','Serun'),
    ('BL','Balm'),
}

STATUS_CHOICES={
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
}

class Products(models.Model):
    """
    Represents a product in the system.

    Attributes:
        title (CharField): The title of the product.
        selling_price (FloatField): The selling price of the product.
        discounted_price (FloatField): The discounted price of the product.
        description (TextField): The description of the product.
        composition (TextField): The composition of the product.
        prodapp (TextField): The application of the product.
        category (CharField): The category of the product.
        product_image (ImageField): The image of the product.

    """
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    def __str__(self):
        """
        Returns a string representation of the product.

        Returns:
            The title of the product.

        """
        return self.title
    
class Customer(models.Model):
    """
    Represents a customer in the system.

    Attributes:
        User (ForeignKey): The user associated with the customer.
        name (CharField): The name of the customer.
        locality (CharField): The locality of the customer.
        city (CharField): The city of the customer.
        mobile (IntegerField): The mobile number of the customer.
        zipcode (IntegerField): The zipcode of the customer.
        state (CharField): The state of the customer.

    """
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        """
        Returns a string representation of the customer.

        Returns:
            The name of the customer.

        """
        return self.name

class Cart(models.Model):
    """
    Represents a cart item in the system.

    Attributes:
        user (ForeignKey): The user associated with the cart item.
        product (ForeignKey): The product associated with the cart item.
        quantity (PositiveIntegerField): The quantity of the product in the cart item.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        """
        Calculates the total cost of the cart item.

        Returns:
            The total cost of the cart item (quantity * product's discounted price).

        """
        return self.quantity * self.product.discounted_price
    
class Payment(models.Model):
    """
    Represents a payment in the system.

    Attributes:
        user (ForeignKey): The user associated with the payment.
        amount (FloatField): The amount of the payment.
        razorpay_order_id (CharField): The order ID provided by Razorpay (if applicable).
        razorpay_payment_status (CharField): The payment status provided by Razorpay (if applicable).
        razorpay_payment_id (CharField): The payment ID provided by Razorpay (if applicable).
        paid (BooleanField): Indicates whether the payment has been paid or not.

    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlaced(models.Model):
    """
    Represents an order placed in the system.

    Attributes:
        user (ForeignKey): The user associated with the order.
        customer (ForeignKey): The customer associated with the order.
        product (ForeignKey): The product associated with the order.
        quantity (PositiveIntegerField): The quantity of the product in the order.
        ordered_date (DateTimeField): The date and time when the order was placed.
        status (CharField): The status of the order.
        payment (ForeignKey): The payment associated with the order.

    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price