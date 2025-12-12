"""
URL configuration for renosic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    CustomerListView,
    CustomerDetailView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    ajax_add_activity,
)

urlpatterns = [
    path('',CustomerListView.as_view(),name='customer_list'),
    path('customer/<int:pk>/',CustomerDetailView.as_view(),name='customer_detail'),
    path('customer/new/', CustomerCreateView.as_view(),name='customer_create'),
    path('customer/<int:pk>/edit',CustomerUpdateView.as_view(),name='customer_update'),
    path('customer/<int:pk>/delete/',CustomerDeleteView.as_view(),name='customer_delete'),
    path('ajax/add_activity/',ajax_add_activity,name='ajax_add_activity'),
]
