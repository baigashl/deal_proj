from django.urls import path
from .views import (
    DealListView,
    UploadFileView,
)

urlpatterns = [
    path('list/', DealListView.as_view(), name='deal-list'),
    path('uploadfile/', UploadFileView.as_view(), name='upload-file'),
]