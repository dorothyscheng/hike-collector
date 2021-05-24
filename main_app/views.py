from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import uuid
import boto3
from .models import Hike, Photo

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'hikecollector'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    all_hikes = Hike.objects.order_by('name')
    return render(request, 'hikes/index.html', {'hikes': all_hikes})

def detail(request, hike_id):
    selected_hike = get_object_or_404(Hike, pk=hike_id)
    return render(request, 'hikes/detail.html', {'selected': selected_hike})

class HikeCreateView(CreateView):
    model = Hike
    fields = ['name', 'location', 'state', 'description', 'length', 'elevation_gain', 'route_type', 'difficulty']
    template_name = 'hikes/hike_form.html'

class HikeUpdateView(UpdateView):
    model = Hike
    fields = ['name', 'location', 'state', 'description', 'length', 'elevation_gain', 'route_type', 'difficulty']
    template_name = 'hikes/hike_form.html'

class HikeDeleteView(DeleteView):
    model = Hike
    template_name = 'hikes/delete.html'
    success_url = '/hikes'

# Reference for configuring photo add: https://git.generalassemb.ly/wc-seir-405/django-aws-config
def add_photo(request, hike_id):
    photo_file = request.FILES.get('photo_file')
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            hike = Hike.objects.get(pk=hike_id)
            photo = Photo(url=url, hike=hike)
            photo.save()
        except Exception as e:
            print(e)
    return redirect('hikes:detail', hike_id=hike_id)