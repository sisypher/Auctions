from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime
from django.db.models.base import ObjectDoesNotExist 
from django.contrib import messages

from .models import *


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'description', 'starting_bid', 'category', 'image']
        widgets = {
            'description': forms.Textarea()
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea()
        }

def index(request):
    listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html",{
        'title': 'Active Listings',
        'listings': listings
    })

def archive(request):
    listings = Listing.objects.filter(active=False)

    return render(request, "auctions/index.html",{
        'title': 'Archived Listings',
        'listings': listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    bid_form = BidForm()
    comment_form = CommentForm()

    # check if the user is logged in
    if request.user.is_authenticated:
        user_watchlist = User.objects.get(id=request.user.id).watchlist.all()

    # get place bids for listing
    try:
        placed_bids = listing.bids.all()
    except ObjectDoesNotExist:
        placed_bids = None
    
    # get comments for listing
    try:
        comments = listing.comments.all()
    except ObjectDoesNotExist:
        comments = None

    # if there is no logged in user
    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "placed_bids": placed_bids
        })

    if request.method == 'POST':
        # to add or remove listing form user's watchlist
        if 'add' in request.POST:
            if listing not in user_watchlist:
                User.objects.get(id=request.user.id).watchlist.add(listing)

        elif 'remove' in request.POST:
            if listing in user_watchlist:
                User.objects.get(id=request.user.id).watchlist.remove(listing)
        
        # Close Auction
        if 'close_auction' in request.POST:
            if request.user == listing.user:
                listing.active = False
                listing.winner = listing.bids.latest('id').user
                listing.save()

        bid_form = BidForm(request.POST)
        comment_form = CommentForm(request.POST)

        # to handle placed bids
        if bid_form.is_valid():
            
            # validating the value of the entered bid
            new_bid = float(request.POST['bid'])
            starting_bid = listing.starting_bid
            try:
                last_placed_bid = listing.bids.latest('id').bid
            except ObjectDoesNotExist:
                last_placed_bid = None

            if new_bid >= starting_bid:
                if last_placed_bid is None:
                    bid = bid_form.save(commit=False)
                    bid.listing = listing
                    bid.user = request.user
                    bid.save()
                    bid_error_message = "Bid was placed successfully!"
                    messages.success(request, bid_error_message)

                elif last_placed_bid and new_bid > last_placed_bid:
                    bid = bid_form.save(commit=False)
                    bid.listing = listing
                    bid.user = request.user
                    bid.save()
                    bid_error_message = "Bid was placed successfully!"
                    messages.success(request, bid_error_message)

                else:
                    bid_error_message = "Please enter a bid greater than the last one placed."
                    messages.error(request, bid_error_message)

            else:
                bid_error_message = "Please enter a bid greater than the starting bid."
                messages.error(request, bid_error_message)
            
        # to handle new comments
        if comment_form.is_valid():

            comment = comment_form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            timestamp = datetime.now()
            comment.created_timestamp = timestamp
            comment.save()
                
        return HttpResponseRedirect(f"{listing_id}")

    
    return render(request, "auctions/listing.html", {
    "listing": listing,
    "user_watchlist": User.objects.get(id=request.user.id).watchlist.all(),
    "bid_form": bid_form,
    "comment_form": comment_form,
    "comments": comments,
    "placed_bids": reversed(placed_bids)
    })


def FilterByCategory(request):
    queryset = Listing.objects.all()
    categories = Category.objects.all()

    category = request.GET.get('category')

    if category != "" or category != None:
        queryset = queryset.filter(category__name=category)
    else:
        return queryset

    return queryset

def categories(request):
    queryset = FilterByCategory(request)

    return render(request, "auctions/category.html", {
        "queryset": queryset,
        "categories": Category.objects.all()
    })

@login_required
def watchlist(request):

    user_watchlist = User.objects.get(id=request.user.id).watchlist.all()
    
    return render(request, "auctions/index.html", {
        'title': 'Watchlist',
        'listings': user_watchlist
    })

@login_required
def user_listings(request):

    user_listings = Listing.objects.filter(user=request.user)

    return render(request, "auctions/index.html", {
        'title': 'My Listings',
        'listings': reversed(user_listings)
    })

@login_required
def new_listing(request):
    if request.method == 'POST':
        
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            
            listing = form.save(commit=False)
            timestamp = datetime.now()
            listing.created_timestamp = timestamp
            listing.user = request.user
            listing.save()

            return render(request, "auctions/newlisting.html", {
                "form": ListingForm(initial={"categories": Category.objects.all()}),
                "message": "Listing was created."
            })
            

        return render(request, "auctions/newlisting.html", {
            "form": ListingForm(request.POST, request.FILES)
        })

    return render(request, "auctions/newlisting.html", {
    "form": ListingForm(initial={"categories": Category.objects.all()})
    })