from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

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

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/delete.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != self.request.user:
            return redirect('login')
        return super().get(request,*args, **kwargs)

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

@login_required
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.user == user:
        if request.method == 'GET':
            form = SignUpForm(instance=user)
        if request.method == 'POST':
            form = SignUpForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                login(request, user)
                return redirect('hikes:profile', user_id=user.id)
        context = {
            'form': form,
        }
        return render(request, 'registration/update.html', context)
    else:
        return redirect('login')

def index(request):
    all_users = User.objects.all().order_by('-date_joined')
    return render(request, 'user/user_index.html', {'users': all_users})