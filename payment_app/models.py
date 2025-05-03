from django.db import models
from user_app.models import User


PLAN_ATTEMPTS = {
    "free": 5, 
    "pro": 10,   
    "premium": 50  
}
class Payment(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]
    
    FREE = 'free'
    PRO = 'pro'
    PREMIUM = 'premium'
    
    PLAN_CHOICES = [
        (FREE, 'Free'),
        (PRO, 'Pro'),
        (PREMIUM, 'Premium'),
    ]
    
    PLAN_PRICES = {
        PRO: 499,
        PREMIUM: 999
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    method = models.CharField(max_length=20, default='card')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=FREE)

    def __str__(self):
        return f"{self.user.email} - ₹{self.amount} - {self.status} - {self.plan}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.COMPLETED:
            plan_type = self.plan
            if plan_type in PLAN_ATTEMPTS:
                self.user.membership_type = plan_type
                self.user.attempt = PLAN_ATTEMPTS[plan_type]
                self.user.save()

