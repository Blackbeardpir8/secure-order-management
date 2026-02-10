from rest_framework import serializers
from orders.models import Order


# =============================================
# Order Serializer
# =============================================
class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer.
    
    # Point 8 & 13: Input sanitization & Validation
    # Point 20: Exposing Choice Fields
    """
    
    # Point 20: Choice Field
    # 'source' calls the Django method get_status_display() automatically.
    # The frontend gets "Pending Payment" instead of just "PENDING".
    status_display = serializers.CharField(
        source="get_status_display", 
        read_only=True
    )

    # Point 13: Strong Validation
    # Prevent negative numbers directly in the serializer.
    total_amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=1.00 # Minimum order value of 1.00
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "status_display", # Add the human-readable field here
            "total_amount",
            "created_at",
        )
        # SECURITY: 
        # - User cannot set the Status (it defaults to CREATED).
        # - User cannot fake the Timestamp.
        # - User cannot pick the Order ID.
        read_only_fields = ("id", "status", "created_at")

    def create(self, validated_data):
        # We will pass the user from the View later using perform_create
        # This ensures the order is ALWAYS linked to the logged-in user.
        return super().create(validated_data)