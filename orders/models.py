import uuid6  # Changed from 'uuid' to 'uuid6'
from django.conf import settings
from django.db import models
from django.utils import timezone

# =======================================
#Order Modal
# =======================================
class Order(models.Model):
    """
    Core Order model.

    # Point 7: Ownership-based access control (via user field)
    # Point 13: Strong data validation (via can_transition)
    """

    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        PENDING = "PENDING", "Pending Payment"
        PAID = "PAID", "Paid"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        EXPIRED = "EXPIRED", "Expired"

    # SECURITY & PERFORMANCE: UUIDv7
    # - Time-sortable: Orders appear in the DB in the order they were created.
    # - No fragmentation: Inserts are faster than random UUIDv4.
    id = models.UUIDField(primary_key=True, default=uuid6.uuid7, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders",)

    status = models.CharField(max_length=15,choices=Status.choices,default=Status.CREATED,)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def can_transition(self, new_status: str) -> bool:
        """
        Enforce valid order state transitions.
        Example: You cannot go from SHIPPED -> CREATED.
        """
        transitions = {
            self.Status.CREATED: [self.Status.PENDING, self.Status.CANCELLED],
            self.Status.PENDING: [self.Status.PAID, self.Status.EXPIRED, self.Status.CANCELLED],
            self.Status.PAID: [self.Status.SHIPPED, self.Status.CANCELLED], # Allow refunds/cancels
            self.Status.SHIPPED: [self.Status.DELIVERED],
            # Delivered, Cancelled, and Expired are terminal states (no way out)
        }

        return new_status in transitions.get(self.status, [])

    def __str__(self):
        return f"Order {self.id} ({self.status})"