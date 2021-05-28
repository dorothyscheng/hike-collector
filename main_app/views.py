from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import uuid
import boto3
from .models import Hike, Photo, Activity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .filters import HikeFilter, ActivityFilter
from .forms import HikeForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'hikecollector'

# Create your views here.
def home(request):
    top_hikes = Hike.objects.exclude(average_rating=None).order_by('-average_rating')[:4]
    all_activities = Activity.objects.all()
    activity_filter = ActivityFilter()
    context = {
        'top_hikes': top_hikes,
        'range': range(5),
        'filter': activity_filter,
        'activities': all_activities,
    }
    return render(request, 'home.html', context)

def index(request):
    all_hikes = Hike.objects.order_by('name')
    hike_filter = HikeFilter(request.GET, queryset=all_hikes)
    context = {
        'filter': hike_filter,
        'range': range(5),
    }
    return render(request, 'hikes/index.html', context)

def detail(request, hike_id):
    selected_hike = get_object_or_404(Hike, pk=hike_id)
    all_activities = Activity.objects.filter(hike=selected_hike)
    context = { 
        'selected': selected_hike, 
        'range': range(5),
        'activities': all_activities,
    }
    return render(request, 'hikes/detail.html', context)

class HikeCreateView(LoginRequiredMixin, CreateView):
    model = Hike
    form_class = HikeForm
    template_name = 'hikes/hike_form.html'

class HikeUpdateView(LoginRequiredMixin, UpdateView):
    model = Hike
    form_class = HikeForm
    template_name = 'hikes/hike_form.html'

class HikeDeleteView(LoginRequiredMixin, DeleteView):
    model = Hike
    template_name = 'hikes/delete.html'
    success_url = '/hikes'

# Reference for configuring photo add: https://git.generalassemb.ly/wc-seir-405/django-aws-config
@login_required
def add_photo(request, hike_id):
    photo_file = request.FILES.get('photo_file')
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            hike = Hike.objects.get(pk=hike_id)
            user = request.user
            photo = Photo(url=url, hike=hike, user=user)
            photo.save()
        except Exception as e:
            print(e)
    return redirect('hikes:detail', hike_id=hike_id)

@login_required
def favorite(request, hike_id):
    if request.method == 'POST':
        user = request.user
        favorite = Hike.objects.get(pk=hike_id)
        if favorite in user.profile.favorites.all():
            user.profile.favorites.remove(favorite)
        else:
            user.profile.favorites.add(favorite)
    return redirect('hikes:detail', hike_id=hike_id)

@login_required
def completed(request, hike_id):
    if request.method == 'POST':
        user = request.user
        completed = Hike.objects.get(pk=hike_id)
        if completed in user.profile.completed.all():
            user.profile.completed.remove(completed)
        else:
            user.profile.completed.add(completed)
    return redirect('hikes:detail', hike_id=hike_id)
