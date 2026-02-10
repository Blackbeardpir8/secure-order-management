from rest_framework import generics, status
from rest_framework.views import APIView  # Added
from rest_framework.permissions import IsAuthenticated, AllowAny # Added AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from common.permissions import IsOrderOwner
from accounts.models import User
from orders.models import Order
from orders.serializers import OrderSerializer


# =========================================
# Standard Results Set Pagination
# =========================================
class StandardResultsSetPagination(PageNumberPagination):
    """
    # Point 18: Pagination
    Controls page size per-view.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# =========================================
# Order Choices API
# =========================================
class OrderChoicesAPIView(APIView):
    """
    Exposes the available Order statuses to the frontend.
    
    # Point 20: Choice Field API
    """
    permission_classes = [AllowAny] 

    def get(self, request):
        # Transform the tuple choices into a clean list of dictionaries
        choices = [
            {"value": key, "label": label}
            for key, label in Order.Status.choices
        ]
        return Response(choices)


# =========================================
# Order Create + List Orders
# =========================================
class OrderListCreateAPIView(generics.ListCreateAPIView):
    """
    Create and list orders.

    # Point 7: Row-level security (via get_queryset)
    # Point 18: Pagination
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    # FIX: Use the custom class we defined above, not the default one
    pagination_class = StandardResultsSetPagination 

    def get_queryset(self):
        # SECURITY: Row-Level Security
        # Admin sees all; Users see only their own.
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        # Business Logic: Force user assignment
        serializer.save(
            user=self.request.user,
            status=Order.Status.PENDING
        )


# =========================================
# Order Retrieve / Update / Delete Order
# =========================================
class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single order.

    # Point 7: Object-level permissions (IsOrderOwner)
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]

    def get_queryset(self):
        # Note: Even for details, we filter the queryset for extra safety.
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return Order.objects.all()
        return Order.objects.filter(user=user)