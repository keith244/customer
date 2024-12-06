from rest_framework import serializers
from . models import Customer,Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name','email','gender','age','image']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['name','price','quantity']