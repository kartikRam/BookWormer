from django.shortcuts import render,redirect
from .models import *
from .forms import CreateUserForm,CustomerForm,BookForm,AuthorForm
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .filters import BookFilter,OrderFilter
from django.db.models import Sum
from django.contrib.auth.models import Group
from .decorators import allowed_users,admin_only


@allowed_users(allowed_roles=['customer'])
def home(request):
    book=books.objects.all()
    context={'book':book}
    return render(request,'store/dashboard.html',context)

@allowed_users(allowed_roles=['customer'])
def view_book(request):
    book=books.objects.all()
    context={'book':book}
    
    return render(request,'store/view_books.html',context)

@allowed_users(allowed_roles=['customer'])
def show_book(request,pk):
    book=books.objects.get(id=pk)
    context={'book':book}
    return render(request,'store/show_book.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
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
            group_data=user.groups.all()[0].name
            print(group_data)
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
@allowed_users(allowed_roles=['customer'])
def show_cart(request):
    user=request.user
    cart_val=cart.objects.filter(user=user)
    total_price=0
    for c in cart_val:
        total_price+=c.price*c.quantity
    context={'cart':cart_val,'total_price':total_price}

    return render(request,'store/cart.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
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
@allowed_users(allowed_roles=['customer'])
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

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def view_book_lib(request):

    book=books.objects.all()
    myfilter=BookFilter(request.GET,queryset=book)
    book=myfilter.qs
    context={'book':book,'filter':myfilter}
    return render(request,'store/show_book_library.html',context)

@login_required(login_url='login')
@admin_only
def view_admin(request):

    order_data=order.objects.all()
    total_order=order_data.count()
    total_delivered_order=order_data.filter(status='1').count()
    total_out_for_delivery_order=order_data.filter(status='0').count()
    print(total_order," ",total_delivered_order," ",total_out_for_delivery_order)
    author_data=author.objects.all()
    ord_data=order.objects.values('book__name').annotate(sale=Sum('quantity')).order_by('-sale')
    author_stat=order.objects.values('book__author__name').annotate(sale=Sum('quantity')).order_by('-sale')
    author_dict={}
    this_dict={}
    for d in ord_data:
        this_dict[d['book__name']]=d['sale']
    
    for d in author_stat:
        author_dict[d['book__author__name']]=d['sale']
    
    context={'author':author_data,'select_aut':0,'order_data':this_dict,'author_data':author_dict,
    'total_order':total_order,'total_delivered_order':total_delivered_order,'total_out_for_delivery_order':total_out_for_delivery_order}
    if request.method=='POST':
        return redirect('book_data_admin',pk=request.POST.get('author'))
    return render(request,'store/admin/dashboard.html',context)

@login_required(login_url='login')
@admin_only
def book_data_admin(request,pk):
    order_data=order.objects.all()
    total_order=order_data.count()
    total_delivered_order=order_data.filter(status='1').count()
    total_out_for_delivery_order=order_data.filter(status='0').count()
    print(total_order," ",total_delivered_order," ",total_out_for_delivery_order)
    
    author_data=author.objects.all()
    ord_data=order.objects.values('book__name').annotate(sale=Sum('quantity')).order_by('-sale')
    author_stat=order.objects.values('book__author__name').annotate(sale=Sum('quantity')).order_by('-sale')
    print(author_stat)
    this_dict={}
    author_dict={}
    for d in ord_data:
        this_dict[d['book__name']]=d['sale']
    for d in author_stat:
        author_dict[d['book__author__name']]=d['sale']
    
    author_data=author.objects.all()
    book=books.objects.filter(author=pk)
    thisdict={}
    
    for b in book:
        ord_data=order.objects.filter(book=b).aggregate(Sum('quantity'))
        print(ord_data['quantity__sum'])
        if ord_data['quantity__sum'] == None:
            thisdict[b.name]=0
        else:
            thisdict[b.name]=ord_data['quantity__sum']
        
    context={'author':author_data,'select_aut':int(pk),'book_data':thisdict,'order_data':this_dict,'author_data':author_dict,
    'total_order':total_order,'total_delivered_order':total_delivered_order,'total_out_for_delivery_order':total_out_for_delivery_order}
    return render(request,'store/admin/dashboard.html',context)

@login_required(login_url='login')    
@admin_only
def admin_books(request):
    book=books.objects.all()    
    context={'book':book}
    return render(request,'store/admin/books.html',context)

@login_required(login_url='login')
@admin_only
def admin_books_update(request,pk):
    book_data=books.objects.get(id=pk)
    form=BookForm(instance=book_data)
    if request.method=="POST":
        form=BookForm(request.POST,request.FILES,instance=book_data)
        if form.is_valid():
            form.save()
    
    context={'form':form,'book':book_data}
    return render(request,'store/admin/update_books.html',context)

@login_required(login_url='login')
@admin_only
def admin_create_books(request):
    form=BookForm()
    if request.method == 'POST':
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    context={'form':form,}
    return render(request,'store/admin/create_book.html',context)     


@login_required(login_url='login')
@admin_only
def admin_author(request):
    author_data=author.objects.all()
    context={'author':author_data}
    return render(request,'store/admin/author.html',context)


@login_required(login_url='login')
@admin_only
def admin_author_update(request,pk):
    author_data=author.objects.get(id=pk)
    form=AuthorForm(instance=author_data)
    if request.method=="POST":
        form=AuthorForm(request.POST,request.FILES,instance=author_data)
        if form.is_valid():
            form.save()
    
    context={'form':form,'author':author_data}
    return render(request,'store/admin/update_author.html',context)

@login_required(login_url='login')
@admin_only
def admin_create_author(request):
    form=AuthorForm()
    if request.method == 'POST':
        form=AuthorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    context={'form':form,}
    return render(request,'store/admin/create_author.html',context)     
