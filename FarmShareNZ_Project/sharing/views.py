from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Equipment,RentalRequest
from .forms import SignupForm,EquipmentForm,RentalRequestForm,ReportForm
def signup(request):
 if request.user.is_authenticated: return redirect('equipment_list')
 form=SignupForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  user=form.save(); group,_=Group.objects.get_or_create(name='Farm Users'); user.groups.add(group); login(request,user); messages.success(request,'Account created successfully.'); return redirect('dashboard')
 return render(request,'registration/signup.html',{'form':form})
class EquipmentListView(ListView):
 model=Equipment; template_name='sharing/equipment_list.html'; context_object_name='equipment_list'
 def get_queryset(self):
  qs=Equipment.objects.filter(is_available=True).select_related('owner'); q=self.request.GET.get('q','').strip(); category=self.request.GET.get('category','').strip()
  if q: qs=qs.filter(Q(name__icontains=q)|Q(description__icontains=q)|Q(location__icontains=q)|Q(category__icontains=q))
  if category: qs=qs.filter(category=category)
  return qs
 def get_context_data(self,**kwargs): c=super().get_context_data(**kwargs); c['categories']=Equipment.CATEGORIES; return c
class EquipmentDetailView(DetailView): model=Equipment; template_name='sharing/equipment_detail.html'
class EquipmentCreateView(LoginRequiredMixin,CreateView):
 model=Equipment; form_class=EquipmentForm; template_name='sharing/equipment_form.html'
 def form_valid(self,form): form.instance.owner=self.request.user; messages.success(self.request,'Equipment listing created.'); return super().form_valid(form)
 def get_success_url(self): return reverse_lazy('equipment_detail',kwargs={'pk':self.object.pk})
class OwnerRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
 def test_func(self): return self.request.user.is_staff or self.get_object().owner==self.request.user
 def handle_no_permission(self): raise PermissionDenied('You do not have permission to manage this listing.')
class EquipmentUpdateView(OwnerRequiredMixin,UpdateView):
 model=Equipment; form_class=EquipmentForm; template_name='sharing/equipment_form.html'
 def get_success_url(self): messages.success(self.request,'Equipment listing updated.'); return reverse_lazy('equipment_detail',kwargs={'pk':self.object.pk})
class EquipmentDeleteView(OwnerRequiredMixin,DeleteView):
 model=Equipment; template_name='sharing/equipment_confirm_delete.html'; success_url=reverse_lazy('dashboard')
@login_required
def dashboard(request):
 own=Equipment.objects.filter(owner=request.user); outgoing=RentalRequest.objects.filter(requester=request.user).select_related('equipment'); incoming=RentalRequest.objects.filter(equipment__owner=request.user).select_related('equipment','requester')
 return render(request,'sharing/dashboard.html',{'own_equipment':own,'outgoing':outgoing,'incoming':incoming})
@login_required
def request_equipment(request,pk):
 equipment=get_object_or_404(Equipment,pk=pk,is_available=True)
 if equipment.owner==request.user: raise PermissionDenied('You cannot request your own equipment.')
 form=RentalRequestForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  rr=form.save(commit=False); rr.equipment=equipment; rr.requester=request.user; rr.save(); messages.success(request,'Request submitted to the equipment owner.'); return redirect('dashboard')
 return render(request,'sharing/request_form.html',{'form':form,'equipment':equipment})
@login_required
@require_POST
def update_request_status(request,pk,action):
 rr=get_object_or_404(RentalRequest,pk=pk)
 if not (request.user.is_staff or rr.equipment.owner==request.user): raise PermissionDenied('Only the equipment owner can update this request.')
 if rr.status!='pending': messages.error(request,'Only pending requests can be changed.'); return redirect('dashboard')
 if action not in {'approved','rejected'}: raise PermissionDenied('Invalid action.')
 rr.status=action; rr.save(update_fields=['status','updated_at']); messages.success(request,f'Request {action}.'); return redirect('dashboard')
@login_required
def report_listing(request,pk):
 equipment=get_object_or_404(Equipment,pk=pk); form=ReportForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  report=form.save(commit=False); report.equipment=equipment; report.reporter=request.user; report.save(); messages.success(request,'Report submitted for administrator review.'); return redirect('equipment_detail',pk=pk)
 return render(request,'sharing/report_form.html',{'form':form,'equipment':equipment})
