from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Customer)
admin.site.register(author)
admin.site.register(books)

admin.site.register(cart)
# Register your models here.
