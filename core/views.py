
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RequestForm, OfferForm
from .models import Request, Offer



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


def request_list(request):
    requests = Request.objects.all()
    return render(request, 'core/request_list.html', {'requests': requests})


def offer_list(request):
    offers = Offer.objects.all()
    return render(request, 'core/offer_list.html', {'offers': offers})
