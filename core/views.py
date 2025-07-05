from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import OfferForm, ProfileForm, RequestForm, SignUpForm, CategoryForm  # already added RequestForm, OfferForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Request, Offer
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings



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
        offer = Offer.objects.create(
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

        # Send email to the requester
        requester = req.user
        donor = request.user

        subject = "Someone Offered Help for Your Request"
        message = f"""
Hi {requester.first_name or requester.username},

{donor.get_full_name() or donor.username} has offered help for your request titled '{req.title}'.

Request Description:
{req.description}

Donor's Contact Details:
Name: {donor.get_full_name() or donor.username}
Email: {donor.email}
Phone Number: {donor.phone_number or 'Not provided'}
Location: {donor.location or 'Not specified'}

Please log in to view more details.

- Community Portal
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [requester.email],
            fail_silently=False,
        )

        messages.success(request, "You have successfully offered help.")
        return redirect('request_list')

    # This part is needed for the GET request (rendering confirmation page)
    return render(request, 'core/offer_help.html', {'request_item': req})


@login_required
def claim_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    if offer.status != 'available':
        messages.warning(request, "This offer is no longer available.")
        return redirect('offer_list')

    # Create a dummy request (if not required, adjust logic)
    dummy_request = Request.objects.create(
        user=request.user,
        title=f"Claimed Offer: {offer.title}",
        description="Auto-generated request for claimed offer.",
        category=offer.category,
        location=offer.location,
        status='fulfilled'
    )

    offer.linked_request = dummy_request
    offer.status = 'claimed'
    offer.save()

    donor = offer.user
    requester = request.user

    # Email to Donor
    subject_donor = "Your Offer Has Been Claimed"
    message_donor = f"""
Hi {donor.first_name or donor.username},

Your offer titled '{offer.title}' has been claimed.

Requester Contact Info:
Name: {requester.get_full_name() or requester.username}
Email: {requester.email}
Phone: {getattr(requester, 'phone_number', 'Not provided')}
Location: {requester.location or 'Not specified'}

Thank you for your generosity!

- Community Portal
"""
    send_mail(subject_donor, message_donor, settings.DEFAULT_FROM_EMAIL, [donor.email])

    # Email to Requester
    subject_requester = "You Have Claimed an Offer"
    message_requester = f"""
Hi {requester.first_name or requester.username},

You have successfully claimed the offer titled '{offer.title}'.

Donor Contact Info:
Name: {donor.get_full_name() or donor.username}
Email: {donor.email}
Phone: {getattr(donor, 'phone_number', 'Not provided')}
Location: {donor.location or 'Not specified'}

Please connect with the donor to proceed.

- Community Portal
"""
    send_mail(subject_requester, message_requester, settings.DEFAULT_FROM_EMAIL, [requester.email])

    messages.success(request, "Offer claimed successfully! Donor and requester have been notified.")
    return redirect('offer_list')




@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('home')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'core/edit_profile.html', {'form': form})





@login_required
def delete_request(request, request_id):
    req = get_object_or_404(Request, id=request_id, user=request.user)
    req.delete()
    return redirect('request_list')

@login_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)
    offer.delete()
    messages.success(request, "Offer deleted successfully.")
    return redirect('offer_list')
