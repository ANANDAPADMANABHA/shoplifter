
import imp
from itertools import product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

import random
import re
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import datetime
from django.shortcuts import redirect, render
from theproducts.models import Product
from accounts.models import Account , Address
from cartapp.models import Cart, CartItem
from django.http import HttpResponse
from django.contrib import auth
from orders.models import OrderProduct, Orders
from datetime import date 

def _cart_id(request):
    session_id = request.session.session_key
    if not session_id:
        session_id    =   request.session.create()
    return session_id

def add_cart(request , product_id):
    
    product = Product.objects.get(id=product_id) #get the product
    

    if request.user.is_authenticated:
        
        try:
            
            cart_item = CartItem.objects.get(product = product ,user = request.user)
            cart_item.quantity += 1 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = request.user)
            cart_item.save()
    else:
        
        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1 
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart)
            cart_item.save()

    

    return redirect (cartview)

def cartview(request,total = 0, quantity = 0, cart_items =None,tax = 0,grand_total =0):
    
    if request.user.is_authenticated:
        
        try:
            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }

    else:
        try:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart.save()

            cart_items  = CartItem.objects.filter(cart = cart, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }
    
    
    return render (request,'cart.html' ,context)

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_items = CartItem.objects.get(product= product, cart = cart)

    if cart_items.quantity > 1 :
        cart_items.quantity -= 1
        cart_items.save()

    else:
        cart_items.delete()
    return redirect('cartview')


def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_items = CartItem.objects.get(product= product, cart = cart)

    
    cart_items.delete()

    return redirect('cartview')

def delete_cart_loggedin(request, product_id):
    
    product = get_object_or_404(Product,id = product_id)
    cart_items = CartItem.objects.get(product= product)

    
    cart_items.delete()

    return redirect('cartview')

def checkout(request):
    
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    
    if request.user.is_authenticated:

        try:
            details = Address.objects.filter(user = request.user )
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'details':details,
        }

    else:
        return redirect(cartview)
    return render(request,'checkout.html',context)


def addaddress(request):
    if request.method == "POST":
        firstname    = request.POST.get('firstname')
        lastname    = request.POST.get('lastname')
        housename    = request.POST.get('housename')
        locality    = request.POST.get('locality')
        city    = request.POST.get('city')
        state    = request.POST.get('state')
        pincode    = request.POST.get('pincode')
        phonenumber    = request.POST.get('phonenumber')
        pincode    = request.POST.get('pincode')

        address = Address(firstname=firstname,lastname=lastname,housename=housename,locality=locality,city=city,state=state,pincode=pincode,phonenumber=phonenumber,user = request.user)
        print('11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
        address.save()

        return redirect(checkout)

def addaddress1(request):
    if request.method == "POST":
        firstname    = request.POST.get('firstname')
        lastname    = request.POST.get('lastname')
        housename    = request.POST.get('housename')
        locality    = request.POST.get('locality')
        city    = request.POST.get('city')
        state    = request.POST.get('state')
        pincode    = request.POST.get('pincode')
        phonenumber    = request.POST.get('phonenumber')
        pincode    = request.POST.get('pincode')

        address = Address(firstname=firstname,lastname=lastname,housename=housename,locality=locality,city=city,state=state,pincode=pincode,phonenumber=phonenumber,user = request.user)
        print('11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
        address.save()

        return (checkout)
    return render(request,'addaddress1.html')


def confirmpayment(request):
    if request.method == "POST":
        global theaddress
        theaddress = request.POST.get('address') #address object in the address as we passed address in it
   
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    
    if request.user.is_authenticated:

        try:

            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass #just ignore

        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'details':details,
        
        }
        

    else:
        return redirect(cartview)

    
    return render(request,'confirmorderinvoice.html',context)


def placecod(request):
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    if request.user.is_authenticated:
        
        

        try:

            details = Address.objects.get(id = theaddress ) #passed that spesific address in the details variable
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            user =  request.user
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)

            dates =date.today()   
            oder = Orders(user=user,address=details ,ordertotal = total,orderid =order_id_generated,date=dates)

            oder.save()

            
            cart_items  = CartItem.objects.filter(user = request.user, is_active = True)
           
            

            for x in cart_items:
                order = Orders.objects.get(orderid = order_id_generated)
                Orderproduct = OrderProduct(order=order)
                Orderproduct.product = x.product
                Orderproduct.quantity = x.quantity
                Orderproduct.price = x.product.price
                Orderproduct.save()
                

            for x in cart_items:
                x.delete()
            
        

        except ObjectDoesNotExist:
            pass #just ignore

        
        

    else:
        return redirect(cartview)
        
    order = Orders.objects.get(orderid = order_id_generated)
    Orderproduct = OrderProduct.objects.filter(order=order)
    for cart_item in Orderproduct:
        total += (cart_item.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total + tax
            
            
           

    context = {
    'total':total,
    'quantity':quantity,
    'Orderproduct':Orderproduct,
    'tax':tax,
    'grand_total':grand_total,
    'details':details,
        
        }
    return render(request,'bill.html',context)


