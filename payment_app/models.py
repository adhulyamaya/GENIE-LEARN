from django.db import models
from user_app.models import User

# Create your models here.
class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    method = models.CharField(max_length=20,  default='card')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} - {self.status}"