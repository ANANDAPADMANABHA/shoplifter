
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.cartview, name='cartview'),  
    path('add_cart/<int:product_id>/',views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name ='remove_cart' ),
    path('delete/<int:product_id>/',views.delete_cart,name ='delete_cart' ),
    path('deleteloggedin/<int:product_id>/',views.delete_cart_loggedin,name ='deleteloggedin' ),
    path('checkout',views.checkout,name='checkout'), 
    path('addaddress',views.addaddress,name='addaddress') , 
    path('addaddress1',views.addaddress1,name='addaddress1') , 
    path('confirmpayment',views.confirmpayment,name='confirmpayment') , 
    path('placecod',views.placecod,name='placecod') , 



]