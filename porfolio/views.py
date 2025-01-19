from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout,login, authenticate
from broker.models import Account, Dashboard, Histotry, Withdraw,Deposit, Investment, myAsset,Profile
from django.contrib import messages


# Create your views here.

def index(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'index.html')

def termOfUse(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'terms-of-use.html')

def signup(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirmation')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        trading_platform = request.POST.get('trading_platform')
        next_url = request.POST.get('next', '/broker/dashboard/')  # Get `next` from the POST data

        # Debug: Log inputs and next_url
        print("Form Data:", username, first_name, last_name, email, phone, trading_platform)
        print("Next URL:", next_url)

        # Validate input
        errors = []
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")
        if Account.objects.filter(phone=phone).exists():
            errors.append("Phone number already exists.")

        if errors:
            # Return errors to the template
            return render(request, 'register.html', {'errors': errors, 'next': next_url})

        # Create user and related models
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        Account.objects.create(
            first_name=first_name,
            last_name=last_name,
            user=user,
            phone=phone,
            trading_platform=trading_platform,
        )
        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        myAsset.objects.create(
            user=user,
            bitcoin=10,
            ethereum=10
        )
        Dashboard.objects.create(
            user=user,
            deposit_wallet_balance=10.0,
            interest_wallet_balance=0.0,
            total_invest_balance=0.0,
            total_deposit=0.0,
            total_withdraw=0.0,
            referral_balance=0.0,
            trading_platform=trading_platform
        )

        # Automatically log in the user after signup
        login(request, user)
        messages.success(request, "Signup successful!")
        return redirect(next_url)  # Redirect to the `next` URL or default to '/'

    # Handle GET requests: Pass `next` to the template
    next_url = request.GET.get('next', '/broker/dashboard/')
    return render(request, 'register.html', {'next': next_url})

def signin(request):
    if request.method == 'POST':
        # Get the form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/broker/dashboard/')  # Get `next` parameter from the form, default to '/'

        print("GET next:", request.GET.get('next'))
        print("POST next:", request.POST.get('next'))

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "Login successful")
            return redirect(next_url)  # Redirect to the original page or default to '/'
        else:
            messages.error(request, "Login not successful. Check details and try again.")
    else:
        # Pass the `next` parameter to the template when rendering the form
        next_url = request.GET.get('next', '/broker/dashboard/')
    
    return render(request, 'login.html', {'next': next_url})

def about(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'about.html')


def privacyPolicy(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'privacy-policy.html')


def watch(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'watch.html')


def forgotpassword(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'forgot-password.html')


def features(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'features.html')


def contact(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'contact.html')


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        Subscribe.objects.create(email=email)
        return redirect("/")
    return redirect(request.path)
