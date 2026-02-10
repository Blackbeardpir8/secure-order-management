from django.urls import path
from orders.views import (
    OrderListCreateAPIView,
    OrderDetailAPIView,
    OrderChoicesAPIView,
)

urlpatterns = [
    path("choices/", OrderChoicesAPIView.as_view(), name="order-choices"),
    path("", OrderListCreateAPIView.as_view(), name="order-list-create"),
    path("<uuid:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
]

