from django.shortcuts import render,redirect
from .models import *
from .forms import CreateUserForm,CustomerForm
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .filters import BookFilter



def home(request):
    book=books.objects.all()
    context={'book':book}
    return render(request,'store/dashboard.html',context)

def view_book(request):
    book=books.objects.all()
    context={'book':book}
    
    return render(request,'store/view_books.html',context)

def show_book(request,pk):
    book=books.objects.get(id=pk)
    context={'book':book}
    return render(request,'store/show_book.html',context)

@login_required(login_url='login')
def _cart_(request,pk):

    user=request.user
    book=books.objects.get(id=pk)
    cart_data=cart.objects.filter(user=user,book=book)

    if request.method=="POST" and cart_data.count()==0:
        print(request.POST.get('book_quant'))
        quantity=int(request.POST.get('book_quant'))
        price=book.price
        cart1=cart(book=book,user=user,quantity=quantity,price=price)
        cart1.save()
        messages.info(request,"Your Item is successfully added")
    else:
         messages.info(request,"Your Item was already added")

    return redirect('show_book',pk=pk)

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

@login_required(login_url='login')
def show_cart(request):
    user=request.user
    cart_val=cart.objects.filter(user=user)
    total_price=0
    for c in cart_val:
        total_price+=c.price*c.quantity
    context={'cart':cart_val,'total_price':total_price}

    return render(request,'store/cart.html',context)

@login_required(login_url='login')
def update_cart(request,pk):
    cart_data=cart.objects.get(id=pk)
    if request.method=="POST":
        quant=int(request.POST.get('quantity'))
        if quant<1:
            cart_data.delete()
        else:
            cart_data.quantity=quant
            cart_data.save()

    return redirect('show_cart')


@login_required(login_url='login')
def view_order(request):
    user=request.user
    cart_data=cart.objects.filter(user=user)
    total_price=0
    for c in cart_data:
        order_data=order(book=c.book,user=c.user,quantity=c.quantity,price=c.price)
        order_data.save()
        c.delete()
    order_data=order.objects.filter(user=user)
    for orde in order_data:
        total_price+=orde.price*orde.quantity

    context={'order':order_data,'total_price':total_price}
    return render(request,'store/view_orders.html',context)

def view_book_lib(request):

    book=books.objects.all()
    myfilter=BookFilter(request.GET,queryset=book)
    book=myfilter.qs
    context={'book':book,'filter':myfilter}
    return render(request,'store/show_book_library.html',context)

def view_admin(request):
    context={}
    return render(request,'store/admin/dashboard.html',context)
    