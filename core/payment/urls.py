from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/process/', views.process_payment, name='process-payment'),
    path('payments/<int:pk>/status/', views.payment_status, name='payment-status'),
]