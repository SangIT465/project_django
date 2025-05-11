from django.shortcuts import render
from .models import Destination, Banner
from apps.tours.models import Tour

def home(request):
    """Hiển thị trang chủ với các tour nổi bật và điểm đến phổ biến"""
    popular_destinations = Destination.objects.filter(is_popular=True, is_active=True)[:6]
    featured_tours = Tour.objects.filter(is_featured=True, is_active=True)[:8]
    banners = Banner.objects.filter(is_active=True).order_by('order')

    context = {
        'popular_destinations': popular_destinations,
        'featured_tours': featured_tours,
        'banners': banners,
    }
    return render(request, 'home.html', context)

def about(request):
    """Hiển thị trang giới thiệu"""
    return render(request, 'about.html')

def contact(request):
    """Hiển thị trang liên hệ"""
    return render(request, 'contact.html')
