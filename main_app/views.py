from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from django.shortcuts import render, get_object_or_404
from .models import Hike

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