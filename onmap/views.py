from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from PIL import Image
from .getGPS import get_lat_lon_dt
from .adjust_location import transform
from .models import Position, Picture
from .forms import PositionForm

# Create your views here.
def home(request):
    form = PositionForm()
    return render(request, "onmap/home.html", {'form': form})

def manual(request):
    return render(request, "onmap/manual.html")

def privacy(request):
    return render(request, "onmap/privacy-policy-html-english.html")


@login_required
def mylist(request):
    user = request.user
    positions = Position.objects.prefetch_related('pictures').filter(author = user)
    return render(request, "onmap/position_home.html", {'positions': positions})

def detail(request, id):
    position = Position.objects.prefetch_related('pictures').get(id=id)
    client_ip = request.META['REMOTE_ADDR']
    country = getCountry(client_ip)
    if country == "CN" or country == "ZZ":
        context = {'position': position, 'china': True}
    else:
        context = {'position': position, 'china': False}
    return render(request, "onmap/position_detail.html", context)


def apicall(request, id):
    position = Position.objects.prefetch_related('pictures').get(id=id)
    client_ip = request.META['REMOTE_ADDR']
    country = getCountry(client_ip)
    if country == "CN" or country == "ZZ":
        context = {'position': position, 'china': True}
    else:
        context = {'position': position, 'china': False}

    return render(request, "onmap/position_call.html", context)

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
            position.name += " All" 

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
                image = image.resize((50,50))
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
            
            return redirect('onmap:detail', position.id)

    else:
        form = PositionForm()
        return render(request, 'onmap/position_add.html', {'form': form})

import requests
import json
def getAddress(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key=AIzaSyD03p1K9oToraWXg-EsjsV7I06xwKaQ1do"
    response = requests.get(url)
    print(response.text)
    result = json.loads(response.text)
    return (result["results"][0]["address_components"][3]["long_name"], result["results"][0]["formatted_address"])


def getCountry(ipaddress):
    url = "http://ip2c.org/"+str(ipaddress)
    response = requests.get(url)
    return response.text.split(";")[1]