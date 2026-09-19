from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Equipment,RentalRequest,Report
class SignupForm(UserCreationForm):
 email=forms.EmailField(required=True)
 class Meta: model=User; fields=('username','email','first_name','last_name','password1','password2')
 def clean_email(self):
  email=self.cleaned_data['email'].lower()
  if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('An account already uses this email.')
  return email
class EquipmentForm(forms.ModelForm):
 class Meta: model=Equipment; fields=('name','category','description','location','daily_rate','is_available','image')
 def clean_daily_rate(self):
  rate=self.cleaned_data['daily_rate']
  if rate<=0: raise forms.ValidationError('Daily rate must be greater than zero.')
  return rate
class RentalRequestForm(forms.ModelForm):
 class Meta: model=RentalRequest; fields=('start_date','end_date','message'); widgets={'start_date':forms.DateInput(attrs={'type':'date'}),'end_date':forms.DateInput(attrs={'type':'date'})}
 def clean(self):
  data=super().clean(); start=data.get('start_date'); end=data.get('end_date')
  if start and start<timezone.localdate(): self.add_error('start_date','Start date cannot be in the past.')
  if start and end and end<start: self.add_error('end_date','End date must be on or after start date.')
  return data
class ReportForm(forms.ModelForm):
 class Meta: model=Report; fields=('reason',); widgets={'reason':forms.Textarea(attrs={'rows':4})}
