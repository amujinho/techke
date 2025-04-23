from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class PlanRequest(models.Model):
    PLAN_CHOICES =  [
       ('basic', 'Basic Plan'),
       ('premium', 'Premium Plan'),
       ('vip', 'VIP Plan'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    reason = models.CharField(max_length=20, choices=PLAN_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.reason}"
    
class Testimonial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.content[:50]}"

class StockPrediction(models.Model):
    stock_symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    predicted_price = models.FloatField()
    actual_price = models.FloatField(null=True, blank=True)
    action_taken = models.CharField(max_length=10, choices=[("BUY", "Buy"), ("SELL", "Sell"), ("HOLD", "Hold")])
    reward = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock_symbol} Prediction at {self.timestamp}"
    
    
