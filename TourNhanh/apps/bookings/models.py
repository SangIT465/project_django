from django.db import models
from django.contrib.auth.models import User
from apps.tours.models import Tour, TourDate
import uuid

class Booking(models.Model):
    """Mô hình đặt tour"""
    STATUS_CHOICES = (
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('paid', 'Đã thanh toán'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('credit_card', 'Thẻ tín dụng'),
        ('momo', 'Ví MoMo'),
        ('zalopay', 'ZaloPay'),
        ('cash', 'Tiền mặt'),
    )
    
    booking_number = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Mã đặt tour")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Người dùng")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Tour")
    tour_date = models.ForeignKey(TourDate, on_delete=models.CASCADE, verbose_name="Ngày khởi hành")
    
    # Thông tin liên hệ
    full_name = models.CharField(max_length=100, verbose_name="Họ tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    
    # Thông tin đặt tour
    adults = models.PositiveSmallIntegerField(default=1, verbose_name="Số người lớn")
    children = models.PositiveSmallIntegerField(default=0, verbose_name="Số trẻ em")
    special_request = models.TextField(blank=True, verbose_name="Yêu cầu đặc biệt")
    
    # Thông tin thanh toán
    total_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Phương thức thanh toán")
    payment_status = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Ngày thanh toán")
    
    # Trạng thái đơn hàng
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    
    class Meta:
        verbose_name = "Đặt tour"
        verbose_name_plural = "Đặt tour"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking_number} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        # Tạo mã đặt tour
        if not self.booking_number:
            prefix = 'TB'  # Tour Booking
            unique_id = str(uuid.uuid4())[:8].upper()
            self.booking_number = f"{prefix}{unique_id}"
        super().save(*args, **kwargs)

class Payment(models.Model):
    """Mô hình thanh toán"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Đơn đặt tour")
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Số tiền")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="Mã giao dịch")
    payment_method = models.CharField(max_length=20, choices=Booking.PAYMENT_METHOD_CHOICES, verbose_name="Phương thức thanh toán")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thanh toán")
    status = models.BooleanField(default=False, verbose_name="Thành công")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    class Meta:
        verbose_name = "Thanh toán"
        verbose_name_plural = "Thanh toán"
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Thanh toán {self.amount} - {self.booking.booking_number}"
