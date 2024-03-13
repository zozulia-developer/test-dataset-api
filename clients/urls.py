from django.urls import path

from . import views
from .views import ExportAPIView

urlpatterns = [
    path('clients/', views.ClientList.as_view(), name='client-list'),
    path('clients/<int:pk>/', views.ClientDetail.as_view(), name='client-detail'),
    path('export/', ExportAPIView.as_view(), name='export'),
]
