from django.contrib import admin
from django.urls import path
from index import views

urlpatterns = [
    path('',views.home,name='home'),
    path('index/', views.index,name='index'),
    path('message/',views.chat_with_company_data,name='message'),
    path('chat_with_company_data/',views.chat_with_company_data,name='chat_with_company_data')
]
