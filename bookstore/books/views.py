import json
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse
from django.shortcuts import render
from .models import Book, Order, MyProfile,Cart, SiteReview
from django.views.generic import ListView, DetailView, TemplateView,CreateView,UpdateView,DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = 'list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'detail.html'

class BookCheckoutView(DetailView):
    model = Book
    template_name = 'checkout.html'


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:',body)
    product = Book.objects.get(id=body['productId'])
    Order.objects.create(product=product)
    return JsonResponse('payment completed',safe=False)

class HomePageView(TemplateView):
    template_name = 'home.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'



class SearchResultView(ListView):
    model = Book
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title=query)| Q(author=query))

class MyProfileView(ListView):
    model = MyProfile
    context_object_name = 'myprofile'
    template_name = 'myprofile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myprofile'] = context['myprofile'].filter(user=self.request.user)
        return context


class MyProfileCreate(LoginRequiredMixin, CreateView):
    model = MyProfile
    fields = ['name', 'email',  'bio', 'Favorites', 'address']
    success_url = reverse_lazy('myprofile')
    template_name = 'editprofile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MyProfileCreate, self).form_valid(form)


class MyProfileUpdate(LoginRequiredMixin, UpdateView):
    model = MyProfile
    fields = ['name', 'email', 'bio', 'Favorites', 'address']
    success_url = reverse_lazy('myprofile')
    template_name = 'editprofile.html'

    def get_object(self, queryset=None):
        return MyProfile.objects.get(user=self.request.user)


def add_to_cart(request, product_id):
    Product = get_object_or_404(Book, pk=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,product=Product, price=Product.price, image_url=Product.image_url,)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})





# Site Reviews
class SiteReviewView(ListView):
    model = SiteReview
    context_object_name = 'reviews'
    template_name = 'review.html'


class SiteReviewCreate(LoginRequiredMixin, CreateView):
    model = SiteReview
    context_object_name = 'reviewcreate'
    fields = ['review', 'rating']
    template_name = 'create-review.html'
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.user = self.request.user
        myprofile = MyProfile.objects.get(user=self.request.user)
        form.instance.name = myprofile
        return super().form_valid(form)


class SiteReviewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SiteReview
    fields = '__all__'
    template_name = 'review.html'
    success_url = reverse_lazy('reviews')

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user


class SiteReviewUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SiteReview
    fields = ['review', 'rating']
    template_name = 'create-review.html'
    success_url = reverse_lazy('reviews')

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user


