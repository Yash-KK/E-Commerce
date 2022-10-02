from typing import Type
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# VERIFICATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Models
from .models import (
    Account
)
# Forms
from .forms import (
    RegisterationForm
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
            login(request, user)
            # messages.info(request, f"You are now logged in!")
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
    # return HttpResponse("ok")


def dashboard(request):
    return render(request, 'acc/dashboard.html')
