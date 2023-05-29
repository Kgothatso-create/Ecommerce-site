from django.shortcuts import render ,redirect
from django.views import View
from .models import Customer, Products, Cart, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
#import razorpay
#from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def home(request):
    """
    Renders the home page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered home.html template with the following context variables:
            - totalitem: The total number of items in the user's cart, if the user is authenticated.

    """
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/home.html", locals())

def about(request):
    """
    Renders the about page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered about.html template with the following context variables:
            - totalitem: The total number of items in the user's cart, if the user is authenticated.

    """
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html", locals())

@login_required
def contact(request):
    """
    Renders the contact page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered contact.html template with the following context variables:
            - totalitem: The total number of items in the user's cart, if the user is authenticated.

    """
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html", locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
     """
    Represents a view for displaying products of a specific category.

    Inherits:
        View: A base class for all views.

    Methods:
        get(request, val): Handles GET requests and renders the category.html template.

    Attributes:
        None.

    """
     def get(self,request,val):
         """
        Handles the GET request for the category view.

        Args:
            request: The HTTP request object.
            val: The category value used for filtering products.

        Returns:
            The rendered category.html template with the following context variables:
                - totalitem: The total number of items in the user's cart, if the user is authenticated.
                - products: The products filtered by the given category value.
                - title: The titles of the products filtered by the given category value.

        """
         totalitem=0
         if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
         products = Products.objects.filter(category=val)
         title = Products.objects.filter(category=val).values('title')
         return render(request,"app/category.html",locals())
     
@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
     """
    Represents a view for displaying products with a specific title.

    Inherits:
        View: A base class for all views.

    Methods:
        get(request, val): Handles GET requests and renders the category.html template.

    Attributes:
        None.

    """
     def get(self,request,val):
         """
        Handles the GET request for the category title view.

        Args:
            request: The HTTP request object.
            val: The title value used for filtering products.

        Returns:
            The rendered category.html template with the following context variables:
                - totalitem: The total number of items in the user's cart, if the user is authenticated.
                - products: The products filtered by the given title value.
                - title: The titles of the products with the same category as the first product in the filtered result.

        """
         totalitem=0
         if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
         products = Products.objects.filter(title=val)
         title = Products.objects.filter(category=products[0].category).values('title')
         return render(request,"app/category.html",locals())
     
@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    """
    Represents a view for displaying the details of a specific product.

    Inherits:
        View: A base class for all views.

    Methods:
        get(request, pk): Handles GET requests and renders the productdetail.html template.

    Attributes:
        None.

    """
    def get(self,request,pk):
        """
        Handles the GET request for the product detail view.

        Args:
            request: The HTTP request object.
            pk: The primary key of the product.

        Returns:
            The rendered productdetail.html template with the following context variables:
                - totalitem: The total number of items in the user's cart, if the user is authenticated.
                - products: The product with the given primary key.

        """
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        products = Products.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())


class CustomerRegistrationView(View):
    """
    Represents a view for customer registration.

    Inherits:
        View: A base class for all views.

    Methods:
        get(request): Handles GET requests and renders the customerregistration.html template.
        post(request): Handles POST requests for user registration.

    Attributes:
        None.

    """
    def get (self,request):
        """
        Handles the GET request for customer registration view.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered customerregistration.html template with the following context variables:
                - form: An instance of the CustomerRegistrationForm.
                - totalitem: The total number of items in the user's cart, if the user is authenticated.

        """
        form = CustomerRegistrationForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html', locals())
    def post(self,request):
        """
        Handles the POST request for user registration.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered customerregistration.html template with the following context variables:
                - form: An instance of the CustomerRegistrationForm.
                - messages: A success message if the form is valid and the user registration is successful,
                            or a warning message if the form is invalid.

        """
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Registration Successfull")
        else:
            messages.warning(request,"Invalid Input")
        return render(request,'app/customerregistration.html', locals())

@method_decorator(login_required, name='dispatch')    
class ProfileView(View):
    """
    Represents a view for managing user profiles.

    Inherits:
        View: A base class for all views.

    Methods:
        get(request): Handles GET requests and renders the profile.html template.
        post(request): Handles POST requests for updating user profiles.

    Attributes:
        None.

    """
    def get(self,request):
        """
        Handles the GET request for the profile view.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered profile.html template with the following context variables:
                - form: An instance of the CustomerProfileForm.
                - totalitem: The total number of items in the user's cart, if the user is authenticated.

        """
        form = CustomerProfileForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render (request, 'app/profile.html', locals())
    def post(self,request):
        """
        Handles the POST request for updating user profiles.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered profile.html template with the following context variables:
                - form: An instance of the CustomerProfileForm.
                - messages: A success message if the form is valid and the profile is saved successfully,
                            or a warning message if the form is invalid.

        """
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile =  form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(User=user, name=name, locality=locality, city=city, mobile=mobile, state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile saved successfully')
        else:
            messages.warning(request,"Invalid input data")
        return render (request, 'app/profile.html', locals())

@login_required 
def address(request):
    add = Customer.objects.filter(User=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    """
    Represents a view for updating user addresses.

    Inherits:
        View: A base class for all views.

    Methods:
        get(request, pk): Handles GET requests and renders the updateAddress.html template.
        post(request, pk): Handles POST requests for updating user addresses.

    Attributes:
        None.

    """
    def get(self,request,pk):
        """
        Handles the GET request for the update address view.

        Args:
            request: The HTTP request object.
            pk: The primary key of the customer object.

        Returns:
            The rendered updateAddress.html template with the following context variables:
                - add: The customer object with the given primary key.
                - form: An instance of the CustomerProfileForm with the customer's current address values.
                - totalitem: The total number of items in the user's cart, if the user is authenticated.

        """
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())
    def post(self, request, pk):
        """
        Handles the POST request for updating user addresses.

        Args:
            request: The HTTP request object.
            pk: The primary key of the customer object.

        Returns:
            A redirect to the 'address' URL with a success message if the form is valid and the profile is updated successfully,
            or a redirect to the 'address' URL with a warning message if the form is invalid.

        """
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile =  form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.warning(request,"Invalid input data")
        return redirect ('address')

@login_required    
def add_to_cart(request):
    """
    Handles adding a product to the user's cart.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the '/cart' URL.

    """
    user=request.user
    Products_id=request.GET.get('prod_id')
    product=Products.objects.get(id=Products_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    """
    Handles displaying the user's cart.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered addtocart.html template with the following context variables:
            - user: The current user.
            - cart: The Cart objects associated with the user.
            - amount: The total amount of the products in the cart (before adding shipping cost).
            - totalamount: The total amount of the products in the cart (including shipping cost).
            - totalitem: The total number of items in the user's cart, if the user is authenticated.

    """
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

@login_required
def plus_cart(request):
    """
    Handles increasing the quantity of a product in the user's cart.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response containing the updated quantity, amount, and total amount of the products in the cart.

    """
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse (data)

@login_required    
def minus_cart(request):
    """
    Handles decreasing the quantity of a product in the user's cart.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response containing the updated quantity, amount, and total amount of the products in the cart.

    """
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse (data)

@login_required    
def remove_cart(request):
    """
    Handles removing a product from the user's cart.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response containing the updated amount and total amount of the products in the cart.

    """
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse (data)

@method_decorator(login_required, name='dispatch')    
class checkout(View):
    """
    Handles the checkout process.

    """
    def get(self,request):
        """
        Handles the GET request for the checkout page.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered checkout.html template with the following context variables:
                - totalitem: The total number of items in the user's cart, if the user is authenticated.
                - user: The current user.
                - add: The Customer objects associated with the user.
                - cart_items: The Cart objects associated with the user.
                - famount: The total amount of the products in the cart (before adding shipping cost).
                - totalamount: The total amount of the products in the cart (including shipping cost).

        """
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(User=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        #razoramount = int(totalamount * 100)
        #client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET ))
        #data = {"amount": razoramount, "currency": "R", "recipient": "order_rcptid_11"}
        #payment_response = client.order.created(data=data)
        #print(payment_response)

        #order_id = payment_response['id']
        #order_status = payment_response['status']
        #if order_status == 'created':
        #    payment = payment(
        #        user=user,
        #        amount=totalamount,
        #        razorpay_order_id=order_id
        #        razorpay_payment_status = order_status
        #    )
        #    payment.save()
        return render(request, 'app/checkout.html',locals())
"""   
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')

    user=request.user

    Customer=Customer.objects.get(id=cust_id)

    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # Tosave order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")
    """

@login_required
def orders(request):
    """
    Renders the orders page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered orders.html template with the following context variables:
            - totalitem: The total number of items in the user's cart, if the user is authenticated.
            - orders_placed: The total number of orders in the users cart.

    """
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    orders_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())
    
 #def add_to_cart(request):
  #  user=request.user
   # Products_id=request.GET.get('prod_id')
    #product=Products.objects.get(id=Products_id)
    #Cart(user=user,product=product).save()
    #return redirect("/cart")

@login_required 
def search(request):
    """
    Renders the searched item product page.

    Args:
        request: The HTTP request object.

    Returns:
        The search result

    """
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user))
    product = Products.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())