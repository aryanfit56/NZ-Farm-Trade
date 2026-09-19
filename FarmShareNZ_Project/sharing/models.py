from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
class Equipment(models.Model):
 CATEGORIES=[('tractor','Tractor'),('harvest','Harvesting'),('tillage','Tillage'),('seeding','Seeding'),('sprayer','Sprayer'),('trailer','Trailer'),('other','Other')]
 owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='equipment')
 name=models.CharField(max_length=120); category=models.CharField(max_length=30,choices=CATEGORIES)
 description=models.TextField(max_length=1500); location=models.CharField(max_length=120)
 daily_rate=models.DecimalField(max_digits=9,decimal_places=2,validators=[MinValueValidator(0.01)])
 is_available=models.BooleanField(default=True)
 image=models.ImageField(upload_to='equipment/',blank=True,null=True)
 created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=['-created_at']
 def __str__(self): return self.name
class RentalRequest(models.Model):
 STATUS=[('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('cancelled','Cancelled')]
 equipment=models.ForeignKey(Equipment,on_delete=models.CASCADE,related_name='rental_requests')
 requester=models.ForeignKey(User,on_delete=models.CASCADE,related_name='rental_requests')
 start_date=models.DateField(); end_date=models.DateField(); message=models.TextField(max_length=500,blank=True)
 status=models.CharField(max_length=12,choices=STATUS,default='pending'); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=['-created_at']
 def __str__(self): return f'{self.equipment} - {self.requester} ({self.status})'
class Report(models.Model):
 STATUS=[('open','Open'),('reviewed','Reviewed'),('closed','Closed')]
 equipment=models.ForeignKey(Equipment,on_delete=models.CASCADE,related_name='reports')
 reporter=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reports')
 reason=models.TextField(max_length=500); status=models.CharField(max_length=10,choices=STATUS,default='open'); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return f'Report #{self.pk} - {self.equipment}'
