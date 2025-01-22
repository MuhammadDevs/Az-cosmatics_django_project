from django.shortcuts import render, HttpResponse, redirect
from .models.product import *
from .models.catagory import *
from .models.customer import *
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.contrib.sessions.models import Session
import re
from django.views.decorators.csrf import csrf_exempt
from .models.order import *
from django.core.mail import EmailMessage
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})
        
        if product:
            quantity = cart.get(product, 0)
            if remove:
                if quantity > 1:
                    cart[product] = quantity - 1
                else:
                    cart.pop(product, None)
            else:
                cart[product] = quantity + 1
        
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('home_page')
    
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        Products = None
        Catagories = Catagory.objects.all()
        CatagoryId = request.GET.get('catagory')
        
        if CatagoryId:
            Products = Product.get_all_products_by_catagory_id(CatagoryId)
        else:
            Products = Product.objects.all()
        
        data = {
            'Products': Products,
            'Catagories': Catagories
        }
        
        print('you are', request.session.get('email'))
        return render(request, 'index.html', data)
    
def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        user_email = request.POST.get('email')  # User's email address
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Prepare email content
        email_subject = f"Contact Form Submission: {subject}"
        email_body = f"""
        You have received a new message from your contact form:

        Name: {name}
        Email: {user_email}
        Subject: {subject}
        Message: 
        {message}
        """

        try:
            # Send the email
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=user_email,  # Your app's Gmail account
                to=['mawais221114@gmail.com'],       # Recipient's email (your email)
                reply_to=[user_email],             # Set reply-to as user's email
            )
            email.send()

            # Success message
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            # Error message
            messages.error(request, f"An error occurred: {e}")

        return redirect('/contact?submitted=true')  # Redirect to the contact page with query string

    return render(request, 'contact.html')

def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
            error_message = "First Name is required"
    elif len(customer.first_name) < 4:
            error_message = "First Name must contain more than 5 letters"
    elif not customer.last_name:
            error_message = "Last Name is required"
    elif len(customer.last_name) < 4:
            error_message = "Last Name must contain more than 5 letters"
    elif not customer.phone:
            error_message = "Phone number is required"
    elif not re.match(r'^\d{4}-\d{7}$', customer.phone):
            error_message = "Phone number must be in the format XXXX-XXXXXXX"
    elif not customer.password:
            error_message = "Password is required"
    elif len(customer.password) < 6:
            error_message = "Password must be at least 6 characters long"
    elif not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', customer.password):
            error_message = "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character" 
     # Check if customer already exists
    if customer.isExist():
            error_message = "Email Address Already Exist"
            return error_message



def signup(request):
    error_message = None
    values = {  # Initialize 'values' with empty values
        'first_name': '',
        'last_name': '',
        'phone': '',
        'email': ''
    }
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Validation
        values = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        customer = Customer(first_name=first_name, 
                            last_name=last_name, 
                            phone=phone, 
                            email=email, 
                            password=password)
        error_message = validateCustomer(customer)
        
        # Saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home_page')
    
    data = {
        'error': error_message,
        'values': values
    }
    return render(request, 'signup.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                # Redirect to the stored URL or home page
                return_url = request.session.pop('return_url', None)
                if return_url:
                    return redirect(return_url)
                else:
                    return redirect('home_page')
            else:
                error_message = 'Invalid Email or password'
        else:
            error_message = 'Invalid Email or password'
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login_page')


def cart(request):
    # Ensure the cart key exists in the session
    if 'cart' not in request.session:
        request.session['cart'] = {}

    if request.method == 'GET':
        cart_keys = list(request.session.get('cart', {}).keys())
        products = Product.get_products_by_id(cart_keys)
        return render(request, 'cart.html', {'products': products})

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            order = Order(
                customer=Customer(id=customer), 
                product=product,
                price=product.price,
                address=address,
                quantity=cart.get(str(product.id))
            )
            order.placeOrder()
        
        request.session['cart'] = {}

    return redirect('cart_page')



def orderview(request):
    if request.method == 'GET':
        customer = request.session.get('customer')
        order = Order.get_orders_by_customer(customer)
        print(order)
        return render(request, 'orders.html', {'order': order})


    