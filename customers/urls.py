from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('about/',views.about, name='about'),
    path('create/',views.create_customer, name='create'),
    path('chat/',views.chat, name='chat'),
    path('update/<int:id>/',views.update, name='update'),
    path('delete_customer/<int:id>/',views.delete_customer, name='delete'),
    path('customer_api/', views.customer_api,name='customer_api'),

    # URLS for Order model
    path('view_order/',views.view_order,name='view_order'),
    path('create_order/',views.create_order,name='create_order'),
    path('update_order/<int:id>/',views.update_order,name='update_order'),
    path('delete_order/<int:id>/',views.delete_order,name='delete_order'),
    path('order_api/',views.order_api,name='order_api'),
    # m-pesa api
    path('mpesa_api/',views.mpesa_api,name='mpesa_api'),
    path('mpesa_order/',views.mpesa_order,name='mpesa_order'),
    path('new_order/',views.new_order,name='new_order'),
]