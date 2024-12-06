from django import forms
from customers.models import Customer,Order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs= {
                'class': 'form-control',
                'placeholder':'Enter your name',
                }),
            'email': forms.EmailInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'gender': forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Whats your gender'
            }),
            'age': forms.NumberInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Enter age'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class':'form-control','accept':'images/*', 'title':'Upload your image here'
            }),
            'admission_number':forms.TextInput(attrs = {
                'class':'form-control','placeholder':'Enter your admission number'
            }),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name','price','quantity']