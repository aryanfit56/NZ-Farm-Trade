from datetime import timedelta
from django.test import TestCase
from django.contrib.auth.models import User,Group
from django.urls import reverse
from django.utils import timezone
from .models import Equipment,RentalRequest
class FarmShareTests(TestCase):
 def setUp(self):
  self.owner=User.objects.create_user('owner','owner@example.com','StrongPass123!'); self.other=User.objects.create_user('other','other@example.com','StrongPass123!')
  self.eq=Equipment.objects.create(owner=self.owner,name='John Deere Tractor',category='tractor',description='Farm tractor',location='Waikato',daily_rate='150.00')
 def test_signup_creates_farm_user_group(self):
  r=self.client.post(reverse('signup'),{'username':'newfarmer','email':'new@example.com','first_name':'New','last_name':'Farmer','password1':'ComplexPass987!','password2':'ComplexPass987!'})
  self.assertEqual(r.status_code,302); self.assertTrue(User.objects.get(username='newfarmer').groups.filter(name='Farm Users').exists())
 def test_login_required_for_create(self): self.assertEqual(self.client.get(reverse('equipment_create')).status_code,302)
 def test_non_owner_cannot_edit(self):
  self.client.login(username='other',password='StrongPass123!'); self.assertEqual(self.client.get(reverse('equipment_update',args=[self.eq.pk])).status_code,403)
 def test_owner_can_edit(self):
  self.client.login(username='owner',password='StrongPass123!'); self.assertEqual(self.client.get(reverse('equipment_update',args=[self.eq.pk])).status_code,200)
 def test_cannot_request_own_equipment(self):
  self.client.login(username='owner',password='StrongPass123!'); self.assertEqual(self.client.get(reverse('request_create',args=[self.eq.pk])).status_code,403)
 def test_invalid_dates_rejected(self):
  self.client.login(username='other',password='StrongPass123!'); today=timezone.localdate(); r=self.client.post(reverse('request_create',args=[self.eq.pk]),{'start_date':today+timedelta(days=2),'end_date':today+timedelta(days=1),'message':'Need it'}); self.assertEqual(RentalRequest.objects.count(),0); self.assertContains(r,'End date must be on or after start date.')
 def test_only_owner_can_approve(self):
  rr=RentalRequest.objects.create(equipment=self.eq,requester=self.other,start_date=timezone.localdate()+timedelta(days=1),end_date=timezone.localdate()+timedelta(days=2))
  self.client.login(username='other',password='StrongPass123!'); self.assertEqual(self.client.post(reverse('request_status',args=[rr.pk,'approved'])).status_code,403)
