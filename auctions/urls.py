from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.new_listing, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("categories", views.categories, name="categories"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("archive", views.archive, name="archive")
]