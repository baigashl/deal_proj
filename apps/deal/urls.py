from django.urls import path
from .views import (
    DealCreateView,
    DealListView,
    CustomerListView,
    CustomerDetailView,
    UploadFileView,
    FileReadAPIView,
)

urlpatterns = [
    path('create/', DealCreateView.as_view(), name='deal-create'),
    path('list/', DealListView.as_view(), name='deal-list'),

    path('customer/list/', CustomerListView.as_view(), name='customer-list'),
    path('customer/<str:username>/', CustomerDetailView.as_view(), name='customer-detail'),

    path('uploadfile/', UploadFileView.as_view(), name='upload-file'),
    path('fileread/', FileReadAPIView.as_view(), name='read-file'),
]