from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError

from .models import Bid, Listing, User, Wishlist


def index(request):
    listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def product(request, id):
    product = Listing.objects.get(id=id)
    if product.closed:
        bid = Bid.objects.filter(bid_on = product, current_highest=True)
        if len(bid) == 0:
            return render(request, "auctions/product.html", {
            "product": product,
            "highest_bid_by": "No one bidded on this item"
            })
        else:
            bid = bid[0]
            highest_bid = bid.bid_price
            highest_bid_by = bid.bid_by.username
            return render(request, "auctions/product.html", {
            "product": product,
            "highest_bid_by": f"{highest_bid_by} won this bidding by bidding at ${highest_bid}"
            })
    else:
        bids = Bid.objects.filter(bid_on = product).values()
        if str(product.created_by) == str(request.user.username):
            own_user = True
        else:
            own_user = False
        if len(bids)==0:
            current_highest = 0
            message = f"{len(bids)} bids so far."
            color = "darkcyan"
        else:
            bid = Bid.objects.filter(bid_on = product, current_highest=True)
            bid = bid[0]
            current_highest = bid.bid_price
            if bid.bid_by == request.user:
                message = f"{len(bids)} bids so far. Yours is current Highest"
                color = "darkcyan"
            else:
                message = f"{len(bids)} bids so far."
                color = "darkcyan"

        if request.user.is_anonymous:
            color = "darkcyan"
            return render(request, "auctions/product.html", {
            "product": product,
            "current_highest": current_highest,
            "message": message,
            "color": color,
            "own_user": False
            })
        else:
            if request.method == 'POST':
                if str(product.created_by) == str(request.user.username):
                    message = "You cannot put bid on your own item"
                    color = "red"
                else:
                    bidprice = request.POST['bid_input']
                    bidprice = int(bidprice)
                    if current_highest >= bidprice or product.price > bidprice :
                        message = "You cannot put lesser bid"
                        color = "red"
                    else:
                        bid = Bid.objects.create(bid_price = bidprice, bid_on = product, bid_by = request.user, current_highest=True)
                        bid.save()
                        Bid.objects.filter(bid_on = product).exclude(bid_price = bidprice).update(current_highest=False)
                        current_highest = bidprice
                        bids = Bid.objects.filter(bid_on = product).values()
                        message = f"{len(bids)} bids so far. Yours is current Highest"
                        color = "darkcyan"
            try:
                preexisting_order = Wishlist.objects.get(product = product, wishlist_of=request.user)
                if preexisting_order:
                    exist = True
                else:
                    exist = False
            except Wishlist.DoesNotExist:
                exist = False
        return render(request, "auctions/product.html", {
            "product": product,
            "exist": exist,
            "message": message,
            "current_highest": current_highest,
            "color": color,
            "own_user": own_user
        })

@login_required(login_url='login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(wishlist_of=request.user).all().values()
    product_list = []
    for item in wishlist_items:
        product = Listing.objects.filter(id =item['product_id']).all()
        product_list.append(product[0])
    return render(request, "auctions/wishlist.html", {
        "product_list": product_list
    })

@login_required(login_url='login')
def add_to_wishlist(request, id):
    item = Listing.objects.get(pk=id)
    try:
        preexisting_order = Wishlist.objects.get(product = item, wishlist_of=request.user)
        if preexisting_order:
            pass
        else:
            wishlist = Wishlist.objects.create(product = item, wishlist_of = request.user)
            wishlist.save()
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(product = item, wishlist_of = request.user)
        wishlist.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove_from_wishlist(request, id):
    item = Listing.objects.get(pk=id)
    try:
        preexisting_order = Wishlist.objects.get(product = item, wishlist_of=request.user)
        if preexisting_order:
            preexisting_order.delete()
        else:
            pass
    except Wishlist.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER'))

def delete_listing(request, id):
    product = Listing.objects.get(id=id)
    if str(product.created_by) == str(request.user.username):
        product.delete()
    return HttpResponseRedirect(reverse("index"))

def closeBid(request, id):
    product = Listing.objects.get(pk=id)
    if str(product.created_by) == str(request.user.username):
        Listing.objects.filter(pk=id).update(closed=True)
        Wishlist.objects.filter(product=id).delete()
    return redirect(request.META.get('HTTP_REFERER'))

    


def category(request):
    distinct_categories = Listing.objects.all().values('category').distinct()
    return render(request, "auctions/category.html", {
        "categories": distinct_categories
    })

def in_category(request, category):
    category_products = Listing.objects.filter(category = category).values()
    return render(request, "auctions/in-category.html", {
        "category_products": category_products
    })

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        title = request.POST['prod-title']
        price = request.POST["prod-price"]
        description = request.POST["prod-description"]
        category = request.POST["prod-category"]
        image_url = request.POST["prod-image"]
        created_by = request.user
        Listing.objects.create(title=title,price=price,description=description,category=category,image_url=image_url,created_by=created_by)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    

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
