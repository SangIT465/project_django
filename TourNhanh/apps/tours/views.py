from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Tour, TourCategory, TourDate
from apps.core.models import Destination
from .forms import TourSearchForm, ReviewForm

def tour_list(request):
    """Hiển thị danh sách tour với bộ lọc"""
    form = TourSearchForm(request.GET or None)
    tours = Tour.objects.filter(is_active=True)
    
    # Xử lý tìm kiếm
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        destination = form.cleaned_data.get('destination')
        category = form.cleaned_data.get('category')
        duration = form.cleaned_data.get('duration')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        
        if keyword:
            tours = tours.filter(
                Q(title__icontains=keyword) | 
                Q(short_description__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        
        if destination:
            tours = tours.filter(destination=destination)
        
        if category:
            tours = tours.filter(category=category)
        
        if duration:
            if duration == '1-3':
                tours = tours.filter(duration__gte=1, duration__lte=3)
            elif duration == '4-7':
                tours = tours.filter(duration__gte=4, duration__lte=7)
            elif duration == '8-14':
                tours = tours.filter(duration__gte=8, duration__lte=14)
            elif duration == '15+':
                tours = tours.filter(duration__gte=15)
        
        if price_min:
            tours = tours.filter(Q(discount_price__gte=price_min) | (Q(discount_price__isnull=True) & Q(price__gte=price_min)))
        
        if price_max:
            tours = tours.filter(Q(discount_price__lte=price_max) | (Q(discount_price__isnull=True) & Q(price__lte=price_max)))
    
    # Sắp xếp
    sort = request.GET.get('sort', 'default')
    if sort == 'price_asc':
        tours = tours.order_by('price')
    elif sort == 'price_desc':
        tours = tours.order_by('-price')
    elif sort == 'duration_asc':
        tours = tours.order_by('duration')
    elif sort == 'duration_desc':
        tours = tours.order_by('-duration')
    else:
        tours = tours.order_by('-is_featured', 'title')
    
    # Phân trang
    paginator = Paginator(tours, 9)  # 9 tours mỗi trang
    page_number = request.GET.get('page', 1)
    tours_page = paginator.get_page(page_number)
    
    # Danh sách các điểm đến và loại tour cho bộ lọc
    categories = TourCategory.objects.all()
    destinations = Destination.objects.filter(is_active=True)
    
    context = {
        'tours': tours_page,
        'form': form,
        'categories': categories,
        'destinations': destinations,
        'search_params': request.GET,
    }
    return render(request, 'tours/tour_list.html', context)

def tour_detail(request, slug):
    """Hiển thị chi tiết tour và cho phép đánh giá"""
    tour = get_object_or_404(Tour, slug=slug, is_active=True)
    
    # Lấy các ngày khởi hành sắp tới
    upcoming_dates = TourDate.objects.filter(
        tour=tour, 
        is_active=True, 
        available_seats__gt=0
    ).order_by('start_date')[:5]
    
    # Lấy các tour liên quan
    related_tours = Tour.objects.filter(
        destination=tour.destination, 
        is_active=True
    ).exclude(pk=tour.pk)[:4]
    
    # Lấy đánh giá
    reviews = tour.reviews.filter(is_approved=True).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Xử lý form đánh giá
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.tour = tour
            new_review.save()
            messages.success(request, 'Cảm ơn bạn đã đánh giá. Đánh giá của bạn sẽ được hiển thị sau khi được phê duyệt.')
            review_form = ReviewForm()  # Reset form
    
    context = {
        'tour': tour,
        'upcoming_dates': upcoming_dates,
        'related_tours': related_tours,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
    }
    return render(request, 'tours/tour_detail.html', context)

def tours_by_destination(request, destination_slug):
    """Hiển thị tour theo điểm đến"""
    destination = get_object_or_404(Destination, slug=destination_slug, is_active=True)
    tours = Tour.objects.filter(destination=destination, is_active=True)
    
    # Phân trang
    paginator = Paginator(tours, 9)
    page_number = request.GET.get('page', 1)
    tours_page = paginator.get_page(page_number)
    
    context = {
        'destination': destination,
        'tours': tours_page,
    }
    return render(request, 'tours/tours_by_destination.html', context)

def tours_by_category(request, category_slug):
    """Hiển thị tour theo loại"""
    category = get_object_or_404(TourCategory, slug=category_slug)
    tours = Tour.objects.filter(category=category, is_active=True)
    
    # Phân trang
    paginator = Paginator(tours, 9)
    page_number = request.GET.get('page', 1)
    tours_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'tours': tours_page,
    }
    return render(request, 'tours/tours_by_category.html', context)
