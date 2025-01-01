from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
# Create your views here.
from django.contrib import messages
from .form import *
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    product=Products.objects.filter(trending=1)
    return render(request,'shop/index.html',{'products':product})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form=CustomUserForm()
        if request.method == 'POST':
            username=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=username,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in Successfully')
                return redirect('/')
            else:
                messages.error(request,'invalid user Name or Password')
                return redirect('/login')

    return render(request,'shop/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"loggedout Successfully")
        return redirect('/')
    
    
def register(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'registreation Success you can Login Now..!')
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})
from django.http import JsonResponse
import json
from .models import Products, Cart

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']

            # Get the product based on the product_id
            try:
                product_status = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                return JsonResponse({'status': 'Product not found'}, status=404)

            # Check if the product already exists in the user's cart
            if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Cart'}, status=200)
            else:
                # Check if the requested quantity is available
                if product_status.quantity >= product_qty:
                    # Create a new Cart entry for the user
                    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    
                    # Reduce the quantity of the product in the database
                    product_status.quantity -= product_qty
                    product_status.save()

                    return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        print(cart)
        return render(request,'shop/cart.html',{'cart':cart})
    else:
        return redirect('/')
 
def collections(request):
    catagory=Category.objects.filter(status=0)
  
    return render(request,'shop/collections.html',{
        'catagory':catagory
    })
    

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Products

def collectionview(request, name):
    # Check if the category exists and is active (status=0)
    if Category.objects.filter(name=name, status=0).exists():
        # Fetch products that belong to the specified category
        products = Products.objects.filter(Category__name=name)  # Correct usage
        return render(request, 'shop/products/index.html', {
            'products': products,  # Pass the products to the template
            'name': name
        })
    else:
        messages.warning(request, 'No such category found')
        return redirect('collections')


def product_details(request, cname, pname):
    if Category.objects.filter(name=cname, status=0).exists():
        category = Category.objects.get(name=cname, status=0)
        if Products.objects.filter(name=pname, status=0, Category=category).exists():
            product = Products.objects.get(name=pname, status=0, Category=category)
            return render(request, 'shop/products/product_details.html', {'products': product})
        else:
            messages.error(request, 'No such product found in the category')
            return redirect('collections')
    else:
        messages.error(request, 'No such category found')
        return redirect('collections')



def remove_cart(request,cid):
    cart_item=Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect('/cart')



def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Products.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
 
def remove_fav(request,fid):
    cart_item=Favourite.objects.get(id=fid)
    cart_item.delete()
    return redirect('/cart')

