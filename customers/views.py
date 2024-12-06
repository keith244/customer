from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from customers.Serializers import CustomerSerializer, OrderSerializer
from . models import Customer,Order
from customers.forms import CustomerForm,OrderForm
from django.contrib import messages
import os
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django_daraja.mpesa.core import MpesaClient
# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    data = Customer.objects.all()
    context = { 'data': data }
    return render(request,'about.html', context)

def chat(request):
    return render(request, 'chat.html')

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('about')
        else:
            form = CustomerForm()

    return render(request,'contact.html',{'form' : CustomerForm(),})

# view for order model



def update(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            if 'image' in request.FILES:
                file_name = os.path.basename(request.FILES['image'].name)
                messages.success (request, f'Customer updated successfully! {file_name} uploaded.')
            else:
                messages.success(request, f'Customer details updated successfully')
            return redirect('about')
        else:
            messages.error (request, f'Please confirm your changes')
    else:
        form = CustomerForm(instance = customer)
    return render (request, 'update.html', {'form':form, 'customer':customer})

def delete_customer(request,id):
    customer = get_object_or_404(Customer, id=id)
    try:
        customer.delete()
        messages.success(request,'Customer deleted successfully')
    except Exception as e:
        messages.error(request, f'Customer not deleted: str{e} ')
    return redirect('about')

# api for customer model
@api_view(['GET','POST'])
def customer_api(request):
    if request.method == 'GET':
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def order_api(request):
    if request.method == 'GET':
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return JsonResponse(serializer.data,safe=False)
    
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"These views handle Order model CRUD operations"

# create 
def create_order (request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_order')
        else:
            form = OrderForm()
    return render(request, 'create_order.html',{'form':OrderForm(),})

# read
def view_order(request):
    data = Order.objects.all()
    context = {'data':data}
    return render(request, 'view_order.html', context)

# update
def update_order(request, id):
    order = get_object_or_404(Order,id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order has been placed successfully')
            return redirect('view_order')
        else:
            messages.error(request,f'Error processing order')
            return render(request, 'update_order.html',{'form':OrderForm()})
    else:
        form = OrderForm(instance = order)
    return render (request, 'update_order.html',{'form':form,'order':order})

# delete
def delete_order (request,id):
    order = get_object_or_404(Order, id=id)
    try:
        order.delete()
        messages.success(request, 'Customer deleted successfully')
    except Exception as e:
        messages.error (request, f'Customer not deleted: str{e}')
    return redirect('view_order')

def mpesa_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))
        quantity = int(request.POST.get('quantity'))
        total = price * quantity

        client = MpesaClient()
        phone_number = '254111255419'
        amount = int(total)
        account_reference = 'Order' + name
        transaction_desc = f'Payment for {quantity} items'
        callback_url = 'https://darajambili.herokuapp.com/express-payment'
        repsonse = client.stk_push(phone_number,amount,account_reference,transaction_desc,callback_url)
        return HttpResponse(repsonse)

def new_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))
        quantity = int(request.POST.get('quantity'))
        phone = request.POST.get('phone')
        total = price * quantity

        # Save order
        order = Order.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            phone=phone,
            total=total
        )

        # Process payment
        client = MpesaClient()
        phone_number = '254' + phone.replace(' ', '')[-9:]  # Format phone number
        amount = int(total)
        account_reference = f'Order-{order.id}'
        transaction_desc = f'Payment for {quantity} items'
        callback_url = 'https://darajambili.herokuapp.com/express-payment'
        
        try:
            response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            return HttpResponse(response)
        except Exception as e:
            order.delete()  # Delete order if payment fails
            return HttpResponse(f"Payment failed: {str(e)}")

    return render(request, 'create_order.html')

"MPESA API done here"

def mpesa_api(request):
    client = MpesaClient()
    phone_number = '254111255419'
    amount = 1
    account_reference = 'eMobilis'
    transaction_desc = 'Payment for Web Dev '
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = client.stk_push (phone_number,amount,account_reference,transaction_desc,callback_url)
    return HttpResponse(response)
