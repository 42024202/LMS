from django.urls import path
from . import views

urlpatterns = [
    # CRUD operations
    path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),

    # Payment processing
    path('payments/<int:pk>/process/', views.process_payment, name='process-payment'),
    path('payments/<int:pk>/status/', views.payment_status, name='payment-status'),
    path('payments/<int:pk>/refund/', views.refund_payment, name='refund-payment'),

    # Statistics (admin only)
    path('stats/', views.payment_stats, name='payment-stats'),
]

