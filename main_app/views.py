from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import uuid
import boto3
from .models import Hike, Photo
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import SignUpForm, ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .filters import HikeFilter

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'hikecollector'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    all_hikes = Hike.objects.order_by('name')
    hike_filter = HikeFilter(request.GET, queryset=all_hikes)
    return render(request, 'hikes/index.html', {'filter': hike_filter})

def detail(request, hike_id):
    selected_hike = get_object_or_404(Hike, pk=hike_id)
    context = { 'selected': selected_hike, 'range': range(5) }
    return render(request, 'hikes/detail.html', context)

class HikeCreateView(LoginRequiredMixin, CreateView):
    model = Hike
    fields = ['name', 'location', 'state', 'description', 'length', 'elevation_gain', 'route_type', 'difficulty']
    template_name = 'hikes/hike_form.html'

class HikeUpdateView(LoginRequiredMixin, UpdateView):
    model = Hike
    fields = ['name', 'location', 'state', 'description', 'length', 'elevation_gain', 'route_type', 'difficulty']
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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hikes:index')
        else:
            error_message = 'Invalid sign up - try again'
    form = SignUpForm()
    context = {
        'form': form,
        'error_message' : error_message,
    }
    return render(request, 'registration/signup.html', context)

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

@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    favorites = user.profile.favorites.all().order_by('name')
    completed = user.profile.completed.all().order_by('name')
    context = {
        'selected': user,
        'favorites': favorites,
        'completed': completed,
        'range': range(5),
    }
    return render(request, 'user/profile.html', context)

@login_required
def add_review(request, hike_id):
    error_message = ''
    user = request.user
    hike = Hike.objects.get(pk=hike_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = user
            new_review.hike = hike
            new_review.save()
            return redirect('hikes:detail', hike_id=hike_id)
        else:
            error_message = 'Invalid review - try again'
    form = ReviewForm()
    context = {
        'form': form,
        'error_message': error_message,
        'hike': hike,
    }
    return render(request, 'reviews/review_form.html', context)