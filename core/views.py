from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import OfferForm, RequestForm, SignUpForm, CategoryForm  # already added RequestForm, OfferForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Request, Offer
from django.contrib.auth.decorators import login_required



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()
            return redirect('request_list')
    else:
        form = RequestForm()
    return render(request, 'core/create_request.html', {'form': form})


@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            return redirect('offer_list')
    else:
        form = OfferForm()
    return render(request, 'core/create_offer.html', {'form': form})

@login_required
def request_list(request):
    requests = Request.objects.all()
    return render(request, 'core/request_list.html', {'requests': requests})

@login_required
def offer_list(request):
    offers = Offer.objects.all()
    return render(request, 'core/offer_list.html', {'offers': offers})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Or wherever you want to go next
    else:
        form = CategoryForm()
    return render(request, 'core/add_category.html', {'form': form})

@login_required
def offer_help(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    if req.user == request.user:
        messages.warning(request, "You can't offer help on your own request.")
        return redirect('request_list')

    if req.status == 'fulfilled':
        messages.warning(request, "This request has already been fulfilled.")
        return redirect('request_list')

    if request.method == 'POST':
        Offer.objects.create(
            user=request.user,
            title=f"Help for: {req.title}",
            description=f"Offering Help for: {req.description}",
            category=req.category,
            location=req.location,
            status='claimed',
            linked_request=req,
        )
        req.status = 'fulfilled'
        req.save()

        messages.success(request, "You have successfully offered help.")
        return redirect('request_list')

    return render(request, 'core/offer_help.html', {'request_item': req})





@login_required
def delete_request(request, request_id):
    req = get_object_or_404(Request, id=request_id, user=request.user)
    req.delete()
    return redirect('request_list')
