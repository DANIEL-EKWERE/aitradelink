from django.db import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from broker.models import Account, Histotry, Withdraw,Deposit, Investment, Asset,Transfer,Profile,Swap
from broker.models import Dashboard
from django.shortcuts import render
from django.contrib.auth import logout,login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



# Create your views here.

@login_required(login_url='/signin/')
def index(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-index.html')

@login_required(login_url='/signin/')
def log(request):
    details = Dashboard.objects.get(user=request.user)
    # user = request.userjjjjjjjjjjjjjjjjjjjjjjjjj
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-log-my-trade.html', {'details':details})


@login_required(login_url='/signin/')
def p2p(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-p2p-trading.html')

@login_required(login_url='/signin/')
def transfer(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'dashboard-transfer-money.html')

@login_required(login_url='/signin/')
def withdraw(request):
    user = request.user
    details = Dashboard.objects.get(user=request.user)
    if request.method == "POST":
        amount = request.POST.get("amount")
        method = request.POST.get("method")
        address = request.POST.get("address")
        if float(amount) > 0 and method and address and float(amount) <= details.deposit_wallet_balance:
            # Create a withdrawal request
            Withdraw.objects.create(
                user=user,
                amount=amount,
                wallet_Address=address,
                method=method,
            )

            # Send withdrawal request email
            mail_subject = "WITHDRAW REQUEST PLACED"
            mail_context = {
                'email': request.user.email,
                'name': request.user.username,
            }

            html_message = render_to_string('withdraw-mail.html', mail_context)
            plain_text = strip_tags(html_message)  # Fallback for plain text email clients
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            try:
                email_message = EmailMultiAlternatives(
                    subject=mail_subject,
                    body=plain_text,  # Use the plain text as fallback
                    from_email=from_email,
                    to=recipient_list,
                )
                email_message.content_subtype = "plain"  # Ensure the fallback is plain text
                email_message.attach_alternative(html_message, "text/html")  # Attach HTML version
                email_message.send()
            except Exception as e:
                print(f"An error occurred: {e}")

            return redirect('/broker/dashboard/')

    return render(request, 'dashboard-withdraw.html', {'balance': details.deposit_wallet_balance})


# http://127.0.0.1:5000/accounts/signin/?next=/broker/withdraw/

@login_required(login_url='/signin/')
def deposit(request):
    details = None
    details = Dashboard.objects.get(user=request.user)
    print("details",details)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('method')
             # Fetch the Dashboard object for the user
        
        assets = Asset.objects.get(user=request.user)
        print("details",details)
        if not amount or not payment_method:
            # messages.error(request, "Amount and payment method are required.")
            return redirect('broker:deposit')

        # Redirect to the invoice page with the data in the URL
        return redirect(f'/broker/invoice/{amount}/{payment_method}/', {"details":details})

    return render(request, 'deposit.html',{"details":details})


@login_required(login_url='/signin/')
def invoice(request, amount, payment_method):
    try:
        # Validate the data (e.g., ensure amount is numeric)
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        
        # Add additional validation for payment_method if needed
        valid_methods = {'1': 'USDT'}  # Replace with your actual payment method options
        if payment_method not in valid_methods:
            raise ValueError("Invalid payment method.")

    except ValueError as e:
        # messages.error(request, str(e))
        return redirect('/broker/deposit/')

    # If valid, pass the data to the template for display
    context = {'amount': amount, 'payment_method': valid_methods[payment_method], 'is_ethereum':payment_method == '1'}
    return render(request, 'invoice.html', context)


@login_required(login_url='/signin/')
def confirm_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        if not amount or not payment_method:
            # messages.error(request, "Missing payment data.")
            return redirect('/broker/deposit/')

        # Save the deposit to the database
        Deposit.objects.create(
            user=request.user,
            amount=amount,
            payment_method=payment_method,
            status="PENDING"
        )

        # Send withdrawal request email
        mail_subject = "DEPOSIT REQUEST PLACED"
        mail_context = {
            'email': request.user.email,
            'name': request.user.username,
        }

        html_message = render_to_string('deposit-mail.html', mail_context)
        plain_text = strip_tags(html_message)  # Fallback for plain text email clients
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]

        try:
            email_message = EmailMultiAlternatives(
                subject=mail_subject,
                body=plain_text,  # Use the plain text as fallback
                from_email=from_email,
                to=recipient_list,
            )
            email_message.content_subtype = "plain"  # Ensure the fallback is plain text
            email_message.attach_alternative(html_message, "text/html")  # Attach HTML version
            email_message.send()
        except Exception as e:
            print(f"An error occurred: {e}")
        # messages.success(request, "Your payment has been confirmed!")
        return redirect('/broker/dashboard/')

    return redirect('/broker/deposit/')


@login_required(login_url='/signin/')
def market(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'market.html')

@login_required(login_url='/signin/')
def paymentMethod(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'payment-method.html')

@login_required(login_url='/signin/')
def setting(request):
    details = Profile.objects.get(user=request.user)
    # user = request.user
    # if user.is_authenticated:
    #     return redirect('/dashboard/')
    return render(request, 'settings.html', {"details":details})

@login_required(login_url='/signin/')
def signout(request):
    logout(request)
    return redirect('/')



@login_required(login_url='/signin/')
def swap(request):
    user = request.user
    balance = Dashboard.objects.get(user=user).deposit_wallet_balance  

    return render(request, 'swap.html',{'balance':balance})


@login_required(login_url='/signin/')
def process_swap(request):
    user = request.user
    balance = Dashboard.objects.get(user=request.user).deposit_wallet_balance    
    if request.method == 'POST':

            network = request.POST.get('network')
            from_token = request.POST.get('from_token')
            to_token = request.POST.get('to_token')
            amount = request.POST.get('amount')



            # try:
            #     swap, created = Swap.objects.get_or_create(user=user)
            #     if created:
            #         # Handle the case where the record was newly created
            #         pass
            #     else:
            #         # Handle the case where the record already exists
            #         pass
            # except IntegrityError as e:
            #     # Log the error and provide feedback to the user
            #     print(f"IntegrityError: {e}")

            #store the swap transaction
            swap = Swap.objects.create(
                user=user,
                from_token=from_token,
                network=network,
                to_token=to_token,
                amount=amount
            )


            # Send swap request email
            mail_subject = "SWAP REQUEST PLACED"
            mail_context = {
                'email': request.user.email,
                'name': request.user.username,
            }

            html_message = render_to_string('swap-mail.html', mail_context)
            plain_text = strip_tags(html_message)  # Fallback for plain text email clients
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            try:
                email_message = EmailMultiAlternatives(
                    subject=mail_subject,
                    body=plain_text,  # Use the plain text as fallback
                    from_email=from_email,
                    to=recipient_list,
                )
                email_message.content_subtype = "plain"  # Ensure the fallback is plain text
                email_message.attach_alternative(html_message, "text/html")  # Attach HTML version
                email_message.send()
            except Exception as e:
                print(f"An error occurred: {e}")
            return redirect('/broker/dashboard/')  # Replace 'dashboard' with the name of your dashboard route
    return render(request, 'swap.html',{'balance':balance})


@login_required(login_url='/signin/')
def update_profile(request):
    details = Account.objects.get(user=request.user)
    if request.method == "POST":
        # Get the current user
        user = request.user

        # Retrieve form data
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        state = request.POST.get('state')
        bank = request.POST.get('bank')
        account = request.POST.get('account')
        accname = request.POST.get('accname')
        wallet_address = request.POST.get('wallet_address')
        image = request.FILES.get('image')

        # Update user's profile
        try:
            profile = Profile.objects.get(user=user)
            profile.fname = fname
            profile.phone = phone
            profile.country = country
            profile.city = city
            profile.zip_code = zip_code
            profile.state = state
            profile.bank = bank
            profile.account = account
            profile.accname = accname
            profile.wallet_address = wallet_address

            if image:
                profile.image = image  # Update profile picture if provided

            profile.save()
            # messages.success(request, "Your profile has been updated successfully.")
            return redirect('/broker/dashboard/')  # Replace 'dashboard' with the name of your dashboard route
        except Profile.DoesNotExist:
            # messages.error(request, "Profile does not exist. Please contact support.")
            return redirect('profile-setting')  # Replace 'profile-setting' with your profile settings page route

    return render(request, 'settings.html', {'details':details})  # Render the form template for GET requests


@login_required(login_url='/signin/')
def dashboard(request):
    user = request.user

    # Initialize variables with default values
    details = None
    # pending = None
    # approved = None
    # cancelled = None
    # deposits = None
    # withdraws = None
    profile = None
    assets = None

    try:
        # Fetch the Dashboard object for the user
        details = Dashboard.objects.get(user=user)
        assets = Asset.objects.get(user=user)



        deposits = Deposit.objects.filter(user=user).order_by("-date")
        withdraws = Withdraw.objects.filter(user=user)
        # profile = Account.objects.get(user=user)
        for x in deposits:
            if x.status == "APPROVED":
                details.deposit_wallet_balance += int(x.amount)

        for x in withdraws:
            if x.status == "APPROVED":
                details.deposit_wallet_balance -= int(x.amount)
        # Fetch History objects based on transaction type
        # pending = Histotry.objects.filter(user=user, tType="PENDING")
        # approved = Histotry.objects.filter(user=user, tType="APPROVED")
        # cancelled = Histotry.objects.filter(user=user, tType="CANCELLED")

        # deposits = Deposit.objects.filter(user=user).order_by("-date")
        # withdraws = Withdraw.objects.filter(user=user)
        profile = Account.objects.get(user=user)
        # for x in deposits:
        #     if x.status == "APPROVED":
        #         details.deposit_wallet_balance += int(x.amount)

        # for x in withdraws:
        #     if x.status == "APPROVED":
        #         details.deposit_wallet_balance -= int(x.amount)
        
        # if withdraws.amount == 0.0:
        #     print(0)
        # else:
        #     print("its not")
    except ObjectDoesNotExist:
        # Handle case where Dashboard or related objects do not exist
        print("No Dashboard object or related data found for the user.",user)

    # Pass all required data to the template
    return render(
        request, 
        'dashboard-index.html', 
        {
            'details': details,
            # 'pending': pending,
            # 'approved': approved,
            # 'cancelled': cancelled,
            # 'deposits': deposits,
            # 'withdraws':withdraws,
            'profile':profile,
            'MyAsset':assets,
        }
    )


@login_required
def profile(request):
    user = request.user
    profile = Account.objects.get(user=user)

    return render(request, 'profile.html',{'profile':profile})

# @login_required
# def withdraw(request):
#     return render(request, 'dashboard-withdraw.html')

@login_required
def withdrawcrypto(request):
    user = request.user
    dashboard = None
    errors = []
    if request.method == "POST":
            amount = request.POST.get('amount')
            address = request.POST.get('copy')
            try:
                dashboard = Dashboard.objects.get(user=user)
                if int(dashboard.deposit_wallet_balance) < int(amount):
                    errors.append("your account balance is not sufficient to place this withdrawal")
                    return render(request, 'withdraw-crypto.html',{'errors':errors})
            except ObjectDoesNotExist:
                dashboard = None
            withdraw = Withdraw.objects.create(
                user=user,
                amount=amount,
                wallet_Address=address
            )

            history = Histotry.objects.create(
                user=user,
                amount=amount,
                wallet_Address=address,
                tType="Withdraw"
            )
            return redirect('/dashboard/')

    return render(request, 'withdraw-crypto.html')



@login_required
def depositcrypto(request):
    user = request.user
    if request.method == "POST":
        amount = request.POST.get('amount')
        address = request.POST.get('copy')

        deposit = Deposit.objects.create(
            user=user,
            amount=amount,
            wallet_Address=address
        )

        history = Histotry.objects.create(
            user=user,
            amount=amount,
            wallet_Address=address,
            tType="Deposit"
        )


        return redirect('/dashboard/')


    return render(request, 'deposit-crypto.html')


# from django.views.decorators.csrf import csrf_exempt

# def invoice(request, payment_method,amount):
#     Deposit.objects.create(
#         user=request.user,
#         payment_method=payment_method,
#         amount=amount
#     )
    
    return render(request, 'dashboard-index')


# @csrf_exempt  # Use only if CSRF is not needed (not recommended for authenticated forms)
def process_transfer(request):
    if request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        balance = Dashboard.objects.get(user=request.user).deposit_wallet_balance
        
        # Perform validation and business logic here
        if email and amount:
            # Example logic: Ensure the amount is within bounds
            if 1000 <= float(amount) <= 10000 and float(balance) <= float(amount):
                # Simulate processing
                print(balance)
                Transfer.objects.create(
                    user= request.user,
                    amount=amount,
                    receiver_email=email,

                )

            # Send transfer request email
            mail_subject = "TRANSFER REQUEST PLACED"
            mail_context = {
                'email': request.user.email,
                'name': request.user.username,
            }

            html_message = render_to_string('transfer-mail.html', mail_context)
            plain_text = strip_tags(html_message)  # Fallback for plain text email clients
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            try:
                email_message = EmailMultiAlternatives(
                    subject=mail_subject,
                    body=plain_text,  # Use the plain text as fallback
                    from_email=from_email,
                    to=recipient_list,
                )
                email_message.content_subtype = "plain"  # Ensure the fallback is plain text
                email_message.attach_alternative(html_message, "text/html")  # Attach HTML version
                email_message.send()
            except Exception as e:
                print(f"An error occurred: {e}")


                return JsonResponse({'success': True, 'message': 'Transfer processed successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'Amount must be between 1000 and 10000 USD, and withdraw amount must not be greater than the balance.'})
        return JsonResponse({'success': False, 'message': 'Invalid data submitted.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def signup(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        confirm_password = request.POST.get('ConfirmPassword')
        email = request.POST.get('email')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        referrer = request.POST.get('referrer')

        address = request.POST.get('aadress')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipCode')
       
        # Debug: Log all inputs
        #print("Form Data:", username, first_name, last_name, email, phone, country, address, state, city,zipcode)

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

         # Debug: Log errors
        print("Errors:", errors)

        if errors:
            # Return errors to the template
            return render(request, 'signup.html', {'errors': errors})

        # Create user and account if no errors
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        Account.objects.create(
            first_name = first_name,
            last_name=last_name,
            user=user,
            # country=country,
            phone=phone,
            # referral=referrer,
            # address=address,
            # city=city,
            # state=state,
            # zipcode=zipcode
        )

        Dashboard.objects.create(
            user=user,
            deposit_wallet_balance=10.0,
            interest_wallet_balance=0.0,
            total_invest_balance=0.0,
            total_deposit=0.0,
            total_withdraw=0.0,
            referral_balance=0.0,
            referral_code=referrer

        )
        # Deposit.objects.create(user=user,amount=0.0,wallet_Address="N/A",status="PENDING")
        # Withdraw.objects.create(user=user,amount=0.0,wallet_Address="N/A",status="PENDING")


        login(request, user)
        return redirect('/dashboard/')

    # Render the signup form
    return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user=user)
            # messages.success(request,"login successful")
            return render(request, 'dashboard.html')
    # messages.error(request,"login not successful, check details and try again.")
    return render(request, 'signin.html')

def resetpassword(request):
    return render(request, 'reset-password.html')


def plans(request):
    return render(request, 'plans.html')

def privacyPolicy(request):
    return render(request, 'privacy-policy.html')

def licensing(request):
    return render(request, 'licensing.html')

# def subscribe(request):
#     if request.method == "POST":
#         email = request.POST.get('newsletter')
#         Subscribe.objects.create(email=email)
#         return redirect("/")
#     return redirect(request.path)

# def contactus(request):
#     if request.method == "POST":
#         fullName = request.POST.get("fullName")
#         email = request.POST.get("email")
#         message = request.POST.get("Message")

#         ContactUs.objects.create(
#             full_name=fullName,
#             email=email,
#             message=message
#         )
#         return redirect("/")

#     return render(request, 'contact.html')

def about(request):
    return render(request, 'aboutus.html')

# def signup(request):

#     return render(request, 'signup.html')

@login_required
def transaction(request):
    user = request.user
    deposits = None
    withdraws = None
    try:
        history = Histotry.objects.filter(user=user)
        deposits = Deposit.objects.filter(user=user).order_by("-date")
        withdraws = Withdraw.objects.filter(user=user)
    except ObjectDoesNotExist:
        history = None

    return render(request, 'transaction.html',{'history':history,'deposits':deposits,'withdraws':withdraws})

@login_required
def investment(request):
    user = request.user
    investment = None
    try:
        investment = Investment.objects.get(user=user)
    except ObjectDoesNotExist:
        investment = None
    return render(request, 'investment.html',{'investment':investment})



'''
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
from datetime import datetime
import asyncio

# Bot token and admin chat ID
BOT_TOKEN = "7654458030:AAEdaH81aN6Q-jWIkdUjBf9oMLWc9jBT4qs"  # Replace with your actual bot token
ADMIN_CHAT_ID = 7142580406  # Replace this with your admin chat  ID
WALLET_ADDRESS = "8CEkNWWi6ipY79Wjmubip65Gvy7EWvFMQKv3gLK3wzaV"

# Conversation states for withdrawal
WALLET_ADDRESS, AMOUNT = range(2)

# In-memory user balances and jobs
user_balances = {}
user_jobs = {}

INACTIVITY_TIMEOUT = 120  # 2 minutes timeout

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Solana's fastest bot to copy trade any coin (SPL token). Deposit SOL to start trading.\n"
        "How can I assist you? Use the buttons below to interact."
    )
    #await reset_inactivity_timer(context, update.effective_user.id)

# Reset inactivity timer
async def reset_inactivity_timer(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    if context.job_queue is None:
        print("Error: JobQueue not initialized.")
        return

    # Cancel any existing job
    if user_id in user_jobs:
        user_jobs[user_id].schedule_removal()

    # Schedule new inactivity job
    job = context.job_queue.run_once(send_inactivity_message, INACTIVITY_TIMEOUT, chat_id=user_id)
    user_jobs[user_id] = job

# Send inactivity message
async def send_inactivity_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="You've been inactive for 2 minutes. Type /start to continue."
    )

# Wallet command
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet_address = "8CEkNWWi6ipY79Wjmubip65Gvy7EWvFMQKv3gLK3wzaV"
    await update.message.reply_text(
        f"Your wallet address:  {wallet_address}\n\n"
        "Copy the address and send SOL to deposit."
    )
    #await reset_inactivity_timer(context, update.effective_user.id)

# Balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Unknown"

    # Notify the user that data is being fetched
    await update.message.reply_text("Fetching Balance, Please Wait...")

    # Send balance request notification to the admin
    balance = user_balances.get(user_id, 100)  # Default balance = 100 USDT for new users
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"User @{username} (ID: {user_id}) has requested their balance. Current balance: {balance} USDT."
    )
    #await reset_inactivity_timer(context, update.effective_user.id)

# Admin reply handler
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_CHAT_ID:
        return  # Ignore messages not from the admin

    command_parts = update.message.text.split(maxsplit=2)
    if len(command_parts) < 3:
        await update.message.reply_text("Usage: /reply <user_id> <your message>")
        return

    user_id_raw = command_parts[1]
    reply_message = command_parts[2]

    if not user_id_raw.isdigit():
        await update.message.reply_text("Error: The user ID must be a valid number.")
        return

    user_id = int(user_id_raw)
    try:
        await context.bot.send_message(chat_id=user_id, text=f"{reply_message}")
        await update.message.reply_text(f"Message successfully sent to user {user_id}.")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")

# Withdraw command - Step 1: Ask for wallet address
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "To withdraw, please provide your wallet address.",
        reply_markup=ReplyKeyboardRemove()
    )
    #await reset_inactivity_timer(context, update.effective_user.id)
    return WALLET_ADDRESS

# Withdraw Step 2: Get wallet address and ask for amount
async def wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet_address"] = update.message.text.strip()
    await update.message.reply_text("Got it! Now, please enter the amount you'd like to withdraw (in SOL):")
    await reset_inactivity_timer(context, update.effective_user.id)
    return AMOUNT

# Withdraw Step 3: Validate amount and process withdrawal
async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    wallet = context.user_data.get("wallet_address")
    amount_text = update.message.text.strip()

    # Validate the amount
    try:
        amount = float(amount_text)
        if amount <= 0:
            await update.message.reply_text("Invalid amount. Please enter a positive number (e.g., 0.5 SOL).")
            return AMOUNT
    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a valid number (e.g., 0.5 SOL).")
        return AMOUNT

    # Notify user of the received withdrawal request
    await update.message.reply_text(
        f"Withdrawal request received:\nWallet: {wallet}\nAmount: {amount_text} SOL.\nProcessing..."
    )

    # Simulate delay for processing
    await asyncio.sleep(3)

    # Notify user about server overload
    await update.message.reply_text(
        "Too many requests at the same time. Please wait a while and try again."
    )

    #await reset_inactivity_timer(context, update.effective_user.id)
    return ConversationHandler.END

# Cancel withdrawal
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Withdrawal process canceled.", reply_markup=ReplyKeyboardRemove())
    await reset_inactivity_timer(context, update.effective_user.id)
    return ConversationHandler.END

# Copy trade command
async def copytrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    copy_wallet = "8CEkNWWi6ipY79Wjmubip65Gvy7EWvFMQKv3gLK3wzaV"
    await update.message.reply_text(
        f"To get started, deposit SOL to your wallet address below:\n\n{copy_wallet}"
    )
    await reset_inactivity_timer(context, update.effective_user.id)

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handler for withdrawal
    withdraw_handler = ConversationHandler(
        entry_points=[CommandHandler("withdraw", withdraw)],
        states={
            WALLET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_address)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(withdraw_handler)
    app.add_handler(CommandHandler("copytrade", copytrade))
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_CHAT_ID), admin_reply))

    print("Bot is running in bot folder...")
    app.run_polling()

if __name__ == "__main__":
    main()

'''