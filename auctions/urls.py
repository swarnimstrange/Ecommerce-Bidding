from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:id>", views.product, name="product"),
    path("watchlist", views.wishlist, name="watchlist"),
    path("watchlist/add/<int:id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("watchlist/remove/<int:id>", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("categories", views.category, name="categories"),
    path("categories/<str:category>", views.in_category, name="in_category"),
    path("product/delete/<int:id>", views.delete_listing, name="delete_listing"),
    path("product/close/<int:id>", views.closeBid, name="closeBid"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
