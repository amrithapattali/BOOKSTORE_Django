from django.contrib import admin
from .models import Book, MyProfile, SiteReview,Cart

# Register your models here.
admin.site.register(Book)
admin.site.register(MyProfile)
admin.site.register(SiteReview)
admin.site.register(Cart)
