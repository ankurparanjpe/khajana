from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect, HttpResponseRedirect
from django.views.generic import (TemplateView, ListView, DetailView, CreateView,UpdateView, DeleteView)
from .models import Post,Comment,City,Subtitle
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm,CommentForm,CityForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
import requests
import json


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post, Comment

    def get_queryset(self):
        return Post.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')


class PostDetailsView(DetailView):
    model = Post


class SubTitleDetailsView(DetailView):
    model = Subtitle, Post, Comment

    def get_queryset(self):
        return Subtitle.objects.filter().order_by('subs')


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


#model query doesnt exist, dont use this class until required for a draft post
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(create_date__isnull=True).order_by('create_date')    #since its a draft view, craete model query for pub_date and replace create_date with published_date

#model query doesnt exist, dont use this function until required for a draft post
@login_required
def post_published(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


def user_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "registration/login.html",
                    context={"form":form})
"""
    if request == "POST":
        username = request.POST.get('username')  #check this in login.html where username key is defined
        password = request.POST.get('password')  #similarly check this for pwd key in login.html

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('post_detail'))

            else:
                return HttpResponse("account not active or created")
        else:
            print("someone is trying to login and failed badly! Username: "+username+" and password: "+password)
            return HttpResponse("Invalid login!")
    else:
        return render(request,'registration/login.html',{})
"""
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm
    return render(request,'registration/signup.html',{'form':form})


def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0034c43d09fffeec3e6936495d7cdc4e'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['city']
            existing_city_count = City.objects.filter(city=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = "City Already exists!"

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    print(city_weather)

    return render(request, "blog/weather.html",context)


def city_remove(request,city_name):
    City.objects.get(city=city_name).delete()
    return redirect('weather')

