from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.core.models import Destination

class TourCategory(models.Model):
    """Mô hình loại tour du lịch"""
    name = models.CharField(max_length=100, verbose_name="Tên loại tour")
    slug = models.SlugField(unique=True, verbose_name="Slug URL")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon")
    
    class Meta:
        verbose_name = "Loại tour"
        verbose_name_plural = "Loại tour"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tour(models.Model):
    """Mô hình tour du lịch"""
    TRANSPORT_CHOICES = (
        ('car', 'Ô tô'),
        ('plane', 'Máy bay'),
        ('train', 'Tàu hỏa'),
        ('ship', 'Tàu thủy'),
        ('mixed', 'Kết hợp'),
    )
    
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, verbose_name="Loại tour")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name="Điểm đến")
    title = models.CharField(max_length=200, verbose_name="Tên tour")
    slug = models.SlugField(unique=True, verbose_name="Slug URL")
    short_description = models.TextField(verbose_name="Mô tả ngắn")
    description = models.TextField(verbose_name="Mô tả chi tiết")
    duration = models.PositiveSmallIntegerField(verbose_name="Số ngày")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá tour")
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá khuyến mãi")
    main_image = models.CharField(max_length=255, verbose_name="Ảnh chính")
    itinerary = models.TextField(verbose_name="Lịch trình")
    includes = models.TextField(verbose_name="Bao gồm")
    excludes = models.TextField(verbose_name="Không bao gồm")
    terms = models.TextField(verbose_name="Điều khoản")
    transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES, default='car', verbose_name="Phương tiện")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    
    class Meta:
        verbose_name = "Tour du lịch"
        verbose_name_plural = "Tour du lịch"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tours:tour_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_on_sale(self):
        return bool(self.discount_price)
    
    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    
    @property
    def discount_percentage(self):
        if self.discount_price:
            return int(100 - (self.discount_price * 100 / self.price))
        return 0

class TourImage(models.Model):
    """Mô hình hình ảnh của tour"""
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE, verbose_name="Tour")
    image_url = models.CharField(max_length=255, verbose_name="Đường dẫn hình ảnh")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Chú thích")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Thứ tự")
    
    class Meta:
        verbose_name = "Hình ảnh tour"
        verbose_name_plural = "Hình ảnh tour"
        ordering = ['order']
    
    def __str__(self):
        return f"Ảnh {self.order} của {self.tour.title}"

class TourDate(models.Model):
    """Mô hình ngày khởi hành của tour"""
    tour = models.ForeignKey(Tour, related_name='dates', on_delete=models.CASCADE, verbose_name="Tour")
    start_date = models.DateField(verbose_name="Ngày khởi hành")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá riêng")
    available_seats = models.PositiveSmallIntegerField(default=20, verbose_name="Số chỗ còn lại")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    class Meta:
        verbose_name = "Ngày khởi hành"
        verbose_name_plural = "Ngày khởi hành"
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.tour.title} - {self.start_date}"
    
    @property
    def is_full(self):
        return self.available_seats <= 0
    
    @property
    def tour_price(self):
        if self.price:
            return self.price
        return self.tour.final_price

class Review(models.Model):
    """Mô hình đánh giá cho tour"""
    tour = models.ForeignKey(Tour, related_name='reviews', on_delete=models.CASCADE, verbose_name="Tour")
    name = models.CharField(max_length=100, verbose_name="Họ tên")
    email = models.EmailField(verbose_name="Email")
    rating = models.PositiveSmallIntegerField(verbose_name="Đánh giá (1-5)")
    comment = models.TextField(verbose_name="Nhận xét")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_approved = models.BooleanField(default=False, verbose_name="Đã duyệt")
    
    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating}/5 - {self.tour.title}"
