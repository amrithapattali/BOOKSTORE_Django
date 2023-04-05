from django import urls
from django.urls import path
from . import views

from .views import BookListView, BookDetailView, BookCheckoutView, HomePageView, SearchResultView, ContactPageView, \
    AboutPageView, MyProfileView,SiteReviewView, SiteReviewCreate, SiteReviewDelete, \
    SiteReviewUpdate,MyProfileCreate,MyProfileUpdate


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('book_list',BookListView.as_view(), name='list'),
    path('details/<int:pk>/',BookDetailView.as_view(), name='details'),
    path('checkout/<int:pk>/',BookCheckoutView.as_view(), name='checkout'),
    path('complete/',views.paymentComplete, name='complete'),

    path('search/', SearchResultView.as_view(), name='search'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('about/', AboutPageView.as_view(), name='about'),


    path('myprofile/', MyProfileView.as_view(), name='myprofile'),
    path('createprofile/', MyProfileCreate.as_view(), name='createprofile'),
    path('editprofile/', MyProfileUpdate.as_view(), name='editprofile'),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),

    path('reviews/', SiteReviewView.as_view(), name='reviews'),
    path('reviewcreate/', SiteReviewCreate.as_view(), name='reviewcreate'),
    path('reviewdelete/<int:pk>/', SiteReviewDelete.as_view(), name='reviewdelete'),
    path('reviewupdate/<int:pk>/', SiteReviewUpdate.as_view(), name='reviewupdate')

]


