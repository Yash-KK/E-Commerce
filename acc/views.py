#DJANGO
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

#PYTHON
from urllib import parse

# VERIFICATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#VIEWS
from Cart.views import _cart_id

# MODELS
from .models import (
    Account,
    UserProfile
)
from Cart.models import (
    Cart,
    CartItems
)
from Orders.models import (
    Order,
    OrderProduct,
    Payment
)
# Forms
from .forms import (
    RegisterationForm,
    AccountForm,
    ProfileForm
)
# Create your views here.
def register_page(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            
            username = email.split('@')[0]
            # print(f"{first_name}, {last_name}, {email}, {phone_number}, {password}, {username}")    
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,password=password)
            user.phone_number = phone_number
            # print(user)
            user.save()      
            
            profile = UserProfile()
            profile.user = user
            profile.profile_pic = 'Images/default/defaultPic.jpg'
            profile.save()
            
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your Account'
            message = render_to_string('acc/acc_verification_mail.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()           
                
            messages.success(request ,'An email has been sent to you')
    else:    
        form = RegisterationForm()
    context = {
        'form': form
    }
    return render(request, 'acc/register.html',context)


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)
        if user is not None:
           
            
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items_exist = CartItems.objects.filter(cart=cart).exists()
                if cart_items_exist:
                    
                    # Fetching the product variations
                    product_ke_var = []
                    cart_items = CartItems.objects.filter(cart=cart)
                    for item in cart_items:
                        var = item.variations.all()
                        product_ke_var.append(list(var))
                    
                    
                    # User Cart
                    user_cart = CartItems.objects.filter(user=user)
                    existing_var = []
                    item_id = []
                    for item in user_cart:
                        var = item.variations.all()
                        existing_var.append(list(var))
                        item_id.append(item.id)
                    
                    for pr in product_ke_var:
                        if pr in existing_var:   
                            index = existing_var.index(pr)
                            id = item_id[index]
                            item = CartItems.objects.get(id=id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItems.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()         
                # for item in cart_items:
                #     item.user = user
                #     item.save()
            except:
                pass 
            login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                print("Try wala")
                x = dict(parse.parse_qs(parse.urlsplit(url).query))
                if 'next' in x:
                    next_page = x['next'][0]
                    return redirect(next_page)
            except:
                print("Except wala")
                pass
            # messages.info(request, f"You are now logged in!")
            print("here")
            return redirect('dashboard')
        else: 
            messages.error(request,"Invalid username or password.")
            return redirect('login-page')
        
    return render(request, 'acc/login.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('login-page')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated')
        return redirect('login-page')
    else:
        return messages.error(request, 'Invalid activation link')
        return redirect('register')    
   

@login_required(login_url='login-page')
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_count = orders.count()
    
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'orders': orders,
        'order_count': order_count,
        'user_profile': user_profile
    }
    return render(request, 'acc/dashboard.html', context)

@login_required(login_url='login-page')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    
    return render(request, 'acc/my_orders.html',context)

@login_required(login_url='login-page')
def edit_profile(request):
    profile_instance = UserProfile.objects.get(user=request.user)   
  
    if request.method == 'POST':
        acc_form = AccountForm(request.POST,instance= request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if acc_form.is_valid() and profile_form.is_valid():
            acc_form.save()
            profile_form.save()
            print("Updated the Profile")
            return redirect('edit-profile')
    else:
        acc_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_instance)
        print("View the Profile")
    context = {
        'acc_form':acc_form,
        'profile_form': profile_form,
        
        'profile_pic': profile_instance.profile_pic.url
    }
     
    return render(request, 'acc/edit_profile.html',context)

@login_required(login_url='login-page')
def change_password(request):    
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(username = request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset')
                return redirect('dashboard')
            else:
                messages.error(request, 'Current password does not match!')
                return redirect('change-password')
        else:
            messages.error(request, 'Passwords do not Match!')
            return redirect('change-password')
        
    return render(request, 'acc/change_password.html')

 
def order_detail(request, order_id):
    order = Order.objects.get(id = order_id)
    order_products = OrderProduct.objects.filter(order=order)
    
    sub_total = 0
    for item in order_products:
        sub_total += item.quantity * item.product_price
    context = {
        'order':order,
        'order_products': order_products,
        'sub_total': sub_total
    } 
    return render(request, 'acc/order_detail.html',context)
