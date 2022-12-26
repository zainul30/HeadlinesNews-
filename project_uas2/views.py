from blog.models import Artikel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.db import  transaction
from django.contrib.auth.hashers import make_password

from blog.models import Artikel
from users.models import Biodata
import requests

def home(request):
    template_name = 'front/home.html'
    context = {
        'title':'my home',
        'welcome':'welcome my home',
    }
    return render(request, template_name, context)

def blog_page(request):
    url = "https://newsapi.org/v2/top-headlines?country=id&apiKey=dc045a8f7399442b8d20d4b80f8b7cd3"

    data = requests.get(url).json()

    a = data['articles']
    nama = []
    judul = []
    desc = []
    link = []
    isi = []
    tanggal = []
    image = []

    for i in range(len(a)):
        f = a[i]
        judul.append(f['title'])
        nama.append(f['author'])
        desc.append(f['description'])
        link.append(f['url'])
        isi.append(f['content'])
        tanggal.append(f['publishedAt'])
        image.append(f['urlToImage'])
        


    mylist = zip(nama,judul,desc,link,isi,tanggal,image)
    context ={'mylist':mylist}

    return render(request, 'front/blog-page.html', context)

def blog_post(request):
    template_name = 'front/blog-post.html'
    context = {
        'title':'about me',
        'welcome':'ini page about',
    }
    return render(request, template_name, context)
# def blog_page(request):
#     template_name = 'front/blog-page.html'
#     artikel = Artikel.objects.all()
#     context = {
#         'title':'Blog me',
#         'welcome':'ini page about',
#         'artikel' : artikel
#     }
#     return render(request, template_name, context)

def base(request):
    template_name = 'front/base.html'
    context = {
        'title':'Tabel',
    }
    return render(request, template_name, context)

def about_us(request):
    template_name = 'front/about-us.html'
    context = {
        'title':'form',
    }
    return render(request, template_name, context)
def contact_us(request):
    template_name = 'front/contact-us.html'
    context = {
        'title':'form',
    }
    return render(request, template_name, context)
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    template_name = 'account/login.html'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None :
            pass
            print("username benar" )
            auth_login(request, user)
            return redirect('home')
        else:
            pass
            print("username salah" )
    context = {
        'title':'form',
    }
    return render(request, template_name, context)
def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    template_name = 'account/register.html'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        telp = request.POST.get('telp')

        try:
            with transaction.atomic():
                User.objects.create(
                    username = username,
                    password = make_password(password),
                    first_name = nama_depan,
                    last_name= nama_belakang,
                    email = email
                )
                get_user = User.objects.get(username = username)
                Biodata.objects.create(
                    user = get_user,
                    alamat = alamat,
                    telp = telp,
                )
            return redirect(home)
        except:pass
        print(username,password,nama_depan,nama_belakang,email,alamat,telp)
    context = {
        'title':'form register',
    }
    return render(request, template_name, context)