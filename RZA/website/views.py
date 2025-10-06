from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm
from .models import Record
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.urls import reverse
from .forms import BookingForm
from .models import Booking, TicketType




# Home page
def home(request):
    return render(request, 'pages/index.html')


# Register a user
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()   # ✅ hashes password properly
            return redirect('my-login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'pages/register.html', context)


# Login
def my_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()   # ✅ AuthenticationForm handles authenticate
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    context = {'login_form': form}
    return render(request, 'pages/my-login.html', context)


# Logout
def user_logout(request):
    logout(request)
    return redirect('my-login')


# Dashboard (protected page)
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records':my_records}

    return render(request, 'pages/dashboard.html',context)

# Creating a record
@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ This saves to the database
            return redirect('dashboard')
        else:
            form = CreateRecordForm()
    context = {'form': form}
    return render(request, 'pages/create_record.html', context)


# Reading/viewing a record
@login_required(login_url='my-login')
def view_record(request,pk):

    one_record = Record.objects.get(id=pk)
    context = {'record':one_record}
    return render(request, 'pages/view-record.html', context=context)


#  update records
@login_required(login_url='my-login')
def update_record(request, pk):
    one_record = Record.objects.get(id=pk)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=one_record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UpdateRecordForm(instance=one_record)

    context = {'form': form, 'record': one_record}
    return render(request, 'pages/update-record.html', context)



#deleting a record
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()

    return redirect("dashboard")


@login_required(login_url='my-login')
def book_tickets(request):
    """Handles the ticket booking form submission and initial price display."""
    
    # Fetch ticket prices for display on the page
    prices = {t.name: t.base_price for t in TicketType.objects.all()}

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # The .save() method automatically calculates and sets the total_price
            booking = form.save() 
            
            # Redirect to the confirmation page
            return redirect(reverse('booking_confirmation', args=[booking.id]))
    else:
        # Initial GET request: display an empty form
        form = BookingForm()

    context = {
        'form': form,
        'ticket_prices': prices,
        'title': 'Book Zoo Tickets',
    }
    return render(request, 'pages/book_tickets.html', context)


@login_required(login_url='my-login')
def booking_confirmation(request, booking_id):
    """Displays the confirmed booking details and total price."""
    
    # Use get_object_or_404 to handle invalid IDs gracefully
    booking = get_object_or_404(Booking, id=booking_id)

    context = {
        'booking': booking,
        'title': 'Booking Confirmed',
    }
    return render(request, 'pages/confirmation.html', context)