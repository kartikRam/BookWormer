from django.shortcuts import render,redirect
from .models import *
from .forms import CreateUserForm,CustomerForm
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate



def home(request):
    book=books.objects.all()
    context={'book':book}
    return render(request,'store/dashboard.html',context)

def view_book(request):
    book=books.objects.all()
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={'book':book}
    
    return render(request,'store/view_books.html',context)

def show_book(request,pk):
    book=books.objects.get(id=pk)
    context={'book':book}
    return render(request,'store/show_book.html',context)

def _cart_(request,pk):

    user=request.user
    book=books.objects.get(id=pk)
    if request.method=="POST":
        quantity=int(request.POST.get('quant'))
        price=book.price*quantity
        cart1=cart(book=book,user=user,quantity=quantity,price=price)
        cart1.save()

    cart_val=cart.objects.filter(user=user)
    context={'cart':cart_val}
    return render(request,'store/cart.html',context)

def userlogin(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username or Password is incorrect")


    return render(request,'store/login.html')


def userregister(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            phone=request.POST.get('phone')
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user,name=user.username,email=user.email,phone=phone)
            messages.success(request,'Account was created for '+username)
            return redirect('login')

    context={'form':form}
    
    return render(request,'store/register.html',context)

def logoutUser(request):
    logout(request)    
    return redirect('login')
