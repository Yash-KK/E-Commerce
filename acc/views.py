from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

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
            print(f"{first_name}, {last_name}, {email}, {phone_number}, {password}, {username}")    
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,password=password)
            user.phone_number = phone_number
            print(user)
            user.save()          
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
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('login-page')
        
    return render(request, 'acc/login.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('login-page')
