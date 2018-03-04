from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.views.decorators.http import require_POST

from PIL import Image
from .getGPS import get_lat_lon_dt
from .adjust_location import transform
from .models import Position, Picture
from .forms import PositionForm, PositionEditForm

# Create your views here.
def home(request):
    form = PositionForm()
    return render(request, "onmap/home.html", {'form': form})


def manual(request):
    return render(request, "onmap/manual.html")


def privacy(request):
    return render(request, "onmap/privacy-policy-html-english.html")

    
def _position_list(request, template, position_list):
    paginator = Paginator(position_list, 8)
    page = request.GET.get('page')
    try:
        position_list = paginator.page(page)
    except PageNotAnInteger:
        position_list = paginator.page(1)
    except EmptyPage:
        position_list = paginator.page(paginator.num_pages)

    context = {'positions': position_list}
    return render(request, template, context)


@login_required
def mylist(request):
    user = request.user
    positions = Position.objects.prefetch_related('pictures').filter(author = user)
    return _position_list(request, "onmap/position_mylist.html", positions)


@login_required
def mylist_ajax(request):
    user = request.user
    positions = Position.objects.prefetch_related('pictures').filter(author = user)
    return _position_list(request, "onmap/position_mylist_ajax.html", positions)


def popularlist(request):
    positions = Position.objects.prefetch_related('pictures').order_by('-likes')
    return _position_list(request, "onmap/position_popularlist.html", positions)


def popularlist_ajax(request):
    positions = Position.objects.prefetch_related('pictures').order_by('-likes')
    return _position_list(request, "onmap/position_popularlist_ajax.html", positions)


def detail(request, slug):
    position = Position.objects.prefetch_related('pictures').get(slug=slug)
    client_ip = request.META['REMOTE_ADDR']
    country = getCountry(client_ip)
    if country == "CN" or country == "ZZ":
        context = {'position': position, 'china': True}
    else:
        context = {'position': position, 'china': False}
    return render(request, "onmap/position_detail.html", context)


@login_required
def edit(request, slug):
    position = Position.objects.prefetch_related('pictures').get(slug=slug)
    user = request.user 
    add_picture_set = []

    if request.method == "POST":
        form = PositionEditForm(request.POST, instance=position)
        if form.is_valid():
            position = form.save()

            add_pictures = request.POST.getlist('add_pictures')
            print("Picture ID : ", add_pictures)

            for picture_id in add_pictures:
                picture = get_object_or_404(Picture, id=picture_id)
                add_picture_set.append(picture)

            position.pictures.set(add_picture_set)

            return redirect(position)
    else:
        form = PositionEditForm(instance=position)
        pictures = position.pictures.all()

        picture_ids = [ picture.id for picture in pictures ]
        notpictures = Picture.objects.filter(author=user).exclude(id__in=picture_ids)

    return render(request, "onmap/position_edit.html", 
            {'form': form, 'pictures':pictures, 'notpictures':notpictures})


@login_required
def delete(request, slug):
    position = Position.objects.prefetch_related('pictures').get(slug=slug)

    if request.method == "POST":
        pass
    
    return render(request, "onmap/position_edit.html", 
            {'position': position, })


def apicall(request, slug):
    position = Position.objects.select_related('author') \
        .prefetch_related('pictures').get(slug=slug)
    if position.public == True:
        position.views = F('views') + 1;
        position.save();
        position.refresh_from_db()

        client_ip = request.META['REMOTE_ADDR']
        country = getCountry(client_ip)
        if country == "CN" or country == "ZZ":
            context = {'position': position, 'china': True}
        else:
            context = {'position': position, 'china': False}
    else:
        context = {'error': True}
    return render(request, "onmap/position_apicall.html", context)


@require_POST
def userlike(request):
    slug = request.POST.get('slug', None)
    position = get_object_or_404(Position, slug=slug)
    position.likes = F('likes') + 1;
    position.save()
    position.refresh_from_db()
    return JsonResponse({'like_count': position.likes })


import sys
from django.utils.six import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def add(request):
    mgLat, mgLng = (0.0, 0.0)
    picture_files = []

    print("Login Check : ", request.user)
    if request.method == 'POST':
        form = PositionForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST.get('name')
            position = form.save(commit=False)

            if request.user.is_authenticated():
                position.author = request.user
            
            pictures = request.FILES.getlist('pictures')

            index = 0
            file_length = len(pictures)

            for filename in pictures:
                
                index += 1
                picture = Picture()

                if file_length >= 2:
                    tempname = name + " " + str(index)
                else:
                    tempname = name

                picture.name = tempname
                image = Image.open(filename)
            # 위도 경도 값 가져오기
                lat, lng, dt = get_lat_lon_dt(image)
                if lat != 0.0:
                    mgLat, mgLng = transform(lat, lng)

                if mgLat:
                    picture.lat = mgLat
                    picture.lng = mgLng
                    picture.locname, picture.address = getAddress(mgLat, mgLng)

            # 사진의 수직/수평 조정
                try:
                    exif = dict(image._getexif().items())
                    if exif:
                        if exif[274] == 3:
                            image = image.rotate(180, expand=True)
                            image.save(filename)
                        elif exif[274] == 6:
                            image = image.rotate(270, expand=True)
                            image.save(filename)
                        elif exif[274] == 8:
                            image = image.rotate(90, expand=True)
                            image.save(filename)
                except:
                    print("There is no EXIF INFO")
            
            # 사진 축약 
                output = BytesIO()
                image = image.resize((80,80))
                image.save(output, format='JPEG', quality=90)
                output.seek(0)

                picture.file = InMemoryUploadedFile(output,  
                        'ImageField', "%s.jpg" % filename.name.split('.')[0], 
                        'image/jpeg', sys.getsizeof(output), None)

                picture.save()
                picture_files.append(picture)

                if file_length >= 2:
                    pos = Position()
                    pos.name = tempname
                    if request.user.is_authenticated():
                        pos.author = request.user
                    pos.save()

                    pos.pictures.add(picture)


            position.save()
            position.pictures.set(picture_files)
            
            return redirect(position)

    else:
        form = PositionForm()
        return render(request, 'onmap/position_add.html', {'form': form})

import requests
import json
def getAddress(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key=AIzaSyD03p1K9oToraWXg-EsjsV7I06xwKaQ1do"
    response = requests.get(url)
    result = json.loads(response.text)
    return (result["results"][0]["address_components"][3]["long_name"], result["results"][0]["formatted_address"])


def getCountry(ipaddress):
    url = "http://ip2c.org/"+str(ipaddress)
    response = requests.get(url)
    return response.text.split(";")[1]