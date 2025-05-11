from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponseBadRequest
from .models import Booking, Payment
from .forms import BookingForm, PaymentForm
from apps.tours.models import Tour, TourDate

def booking_form(request, tour_id, date_id=None):
    """Hiển thị form đặt tour"""
    tour = get_object_or_404(Tour, id=tour_id, is_active=True)
    
    # Kiểm tra ngày khởi hành
    if date_id:
        tour_date = get_object_or_404(TourDate, id=date_id, tour=tour, is_active=True)
    else:
        # Lấy ngày khởi hành đầu tiên nếu không chỉ định
        tour_date = TourDate.objects.filter(tour=tour, is_active=True, available_seats__gt=0).first()
        if not tour_date:
            messages.error(request, 'Hiện không có ngày khởi hành nào khả dụng cho tour này.')
            return redirect('tours:tour_detail', slug=tour.slug)
    
    # Kiểm tra số chỗ còn trống
    if tour_date.available_seats <= 0:
        messages.error(request, 'Ngày khởi hành này đã hết chỗ. Vui lòng chọn ngày khác.')
        return redirect('tours:tour_detail', slug=tour.slug)
    
    # Danh sách ngày khởi hành khả dụng
    available_dates = TourDate.objects.filter(tour=tour, is_active=True, available_seats__gt=0)
    
    # Xử lý đặt tour
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Tính toán tổng tiền
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            
            # Kiểm tra số chỗ
            total_people = adults + children
            if total_people > tour_date.available_seats:
                messages.error(request, f'Chỉ còn {tour_date.available_seats} chỗ trống cho ngày khởi hành này.')
                return render(request, 'bookings/booking_form.html', {'form': form, 'tour': tour, 'tour_date': tour_date, 'available_dates': available_dates})
            
            # Tính giá tour
            from decimal import Decimal
            tour_price = tour_date.tour_price
            child_price = tour_price * Decimal('0.7')  # Giá trẻ em bằng 70% giá người lớn
            total_price = (adults * tour_price) + (children * child_price)
            
            try:
                with transaction.atomic():
                    # Tạo đơn đặt tour
                    booking = form.save(commit=False)
                    booking.tour = tour
                    booking.tour_date = tour_date
                    booking.total_price = total_price
                    if request.user.is_authenticated:
                        booking.user = request.user
                    booking.save()
                    
                    # Cập nhật số chỗ còn lại
                    tour_date.available_seats -= total_people
                    tour_date.save()
                    
                    # Lưu thông tin vào session để xử lý thanh toán
                    request.session['booking_id'] = booking.id
                    
                    return redirect('bookings:booking_confirm', booking_id=booking.id)
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
    else:
        # Lấy thông tin mặc định từ người dùng đã đăng nhập
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = BookingForm(initial=initial_data)
    
    context = {
        'form': form,
        'tour': tour,
        'tour_date': tour_date,
        'available_dates': available_dates,
    }
    return render(request, 'bookings/booking_form.html', context)

def booking_confirm(request, booking_id):
    """Xác nhận đặt tour và chọn phương thức thanh toán"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Kiểm tra quyền truy cập
    if request.user.is_authenticated and booking.user and booking.user != request.user:
        return HttpResponseBadRequest("Bạn không có quyền truy cập đơn đặt tour này")
    
    # Nếu không đăng nhập, kiểm tra xem có phải chủ đơn hàng không thông qua session
    if not request.user.is_authenticated and request.session.get('booking_id') != booking.id:
        return HttpResponseBadRequest("Bạn không có quyền truy cập đơn đặt tour này")
    
    # Xử lý form thanh toán
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            # Cập nhật thông tin thanh toán
            booking.payment_method = payment_method
            booking.save()
            
            if payment_method == 'bank_transfer':
                return redirect('bookings:bank_transfer_payment', booking_id=booking.id)
            elif payment_method in ['credit_card', 'momo', 'zalopay']:
                # Giả lập thanh toán online
                return redirect('bookings:online_payment', booking_id=booking.id)
            else:  # Thanh toán tiền mặt
                messages.success(request, 'Đặt tour thành công! Vui lòng thanh toán tại văn phòng của chúng tôi.')
                return redirect('bookings:booking_success', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'bookings/booking_confirm.html', context)

def bank_transfer_payment(request, booking_id):
    """Hiển thị thông tin chuyển khoản ngân hàng"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Thông tin ngân hàng (đây là thông tin giả)
    bank_info = {
        'bank_name': 'Ngân hàng TMCP Ngoại thương Việt Nam (Vietcombank)',
        'account_number': '1234567890',
        'account_name': 'CÔNG TY DU LỊCH ABC',
        'branch': 'Chi nhánh Hà Nội',
        'message': f'Thanh toan {booking.booking_number}'
    }
    
    context = {
        'booking': booking,
        'bank_info': bank_info,
    }
    return render(request, 'bookings/bank_transfer.html', context)

def online_payment(request, booking_id):
    """Mô phỏng thanh toán trực tuyến"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Trong thực tế, đây sẽ kết nối với cổng thanh toán
    # Ở đây chỉ mô phỏng thanh toán thành công
    if request.method == 'POST':
        # Tạo thanh toán mới
        payment = Payment(
            booking=booking,
            amount=booking.total_price,
            transaction_id=f"TRANS-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            payment_method=booking.payment_method,
            status=True
        )
        payment.save()
        
        # Cập nhật thông tin đặt tour
        booking.payment_status = True
        booking.payment_date = timezone.now()
        booking.status = 'paid'
        booking.save()
        
        messages.success(request, 'Thanh toán thành công!')
        return redirect('bookings:booking_success', booking_id=booking.id)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/online_payment.html', context)

def booking_success(request, booking_id):
    """Trang thông báo đặt tour thành công"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Lấy danh sách các tour đề xuất (cùng điểm đến hoặc cùng loại tour)
    from apps.tours.models import Tour
    recommended_tours = Tour.objects.filter(
        destination=booking.tour.destination,
        is_active=True
    ).exclude(id=booking.tour.id)[:4]  # Lấy tối đa 4 tour
    
    context = {
        'booking': booking,
        'recommended_tours': recommended_tours,
    }
    return render(request, 'bookings/booking_success.html', context)

@login_required
def booking_history(request):
    """Hiển thị lịch sử đặt tour của người dùng"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/booking_history.html', context)

@login_required
def booking_detail(request, booking_id):
    """Hiển thị chi tiết đặt tour"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def cancel_booking(request, booking_id):
    """Hủy đặt tour"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Kiểm tra xem có thể hủy không
    if booking.status in ['completed', 'cancelled']:
        messages.error(request, 'Không thể hủy đơn đặt tour này.')
        return redirect('bookings:booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        # Cập nhật trạng thái
        booking.status = 'cancelled'
        booking.save()
        
        # Cập nhật lại số chỗ còn trống
        tour_date = booking.tour_date
        tour_date.available_seats += (booking.adults + booking.children)
        tour_date.save()
        
        messages.success(request, 'Đã hủy đơn đặt tour thành công.')
        return redirect('bookings:booking_history')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/cancel_booking.html', context)
