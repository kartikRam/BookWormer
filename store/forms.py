from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,books,author
from django.contrib.auth.models import User


class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']

class BookForm(ModelForm):
    class Meta:
        model=books
        fields='__all__'
        
class AuthorForm(ModelForm):
    class Meta:
        model=author
        fields='__all__'

class CreateUserForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']