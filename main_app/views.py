from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import uuid
import boto3
from .models import Hike, Photo, Review
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

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_delete.html'
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
    authorized = False
    user = User.objects.get(pk=user_id)
    if user == request.user:
        authorized = True
    favorites = user.profile.favorites.all().order_by('name')
    completed = user.profile.completed.all().order_by('name')
    context = {
        'selected': user,
        'favorites': favorites,
        'completed': completed,
        'range': range(5),
        'authorized': authorized,
    }
    return render(request, 'user/profile.html', context)

def calculate_average_rating(hike):
    all_hike_reviews = Review.objects.filter(hike=hike)
    rating_sum  = 0
    for review in all_hike_reviews:
        rating_sum += review.rating
    return rating_sum / len(all_hike_reviews)

@login_required
def add_review(request, hike_id):
    error_message = ''
    print(request.POST)
    user = request.user
    hike = Hike.objects.get(pk=hike_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = user
            new_review.hike = hike
            new_review.save()
            hike.average_rating = calculate_average_rating(hike)
            hike.save()
            return redirect('hikes:detail', hike_id=hike_id)
        else:
            error_message = 'Invalid review - try again'
    form = ReviewForm()
    context = {
        'form': form,
        'error_message': error_message,
        'hike': hike,
    }
    return render(request, 'reviews/review_add.html', context)

@login_required
def update_review(request, review_id):
    error_message = ''
    review = Review.objects.get(pk=review_id)
    if request.user == review.user:
        if request.method == 'GET':
            form = ReviewForm(instance=review)
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                review.hike.average_rating = calculate_average_rating(review.hike)
                review.hike.save()
                return redirect('hikes:profile', user_id=review.user.id)
        context = {
            'form': form,
            'hike': review.hike
        }
        return render(request, 'reviews/review_update.html', context)
    else:
        error_message = 'Not authorized to edit that review - add your own review here'
        form = ReviewForm()
        context = {
            'form': form,
            'hike': review.hike,
            'error_message': error_message,
        }
        return render(request, 'reviews/review_add.html', context)
