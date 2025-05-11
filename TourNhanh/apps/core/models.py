from django.db import models

class Destination(models.Model):
    """Mô hình điểm đến du lịch"""
    name = models.CharField(max_length=100, verbose_name="Tên địa điểm")
    slug = models.SlugField(unique=True, verbose_name="Slug URL")
    description = models.TextField(verbose_name="Mô tả", blank=True)
    image = models.CharField(max_length=255, verbose_name="Đường dẫn hình ảnh")
    is_popular = models.BooleanField(default=False, verbose_name="Phổ biến")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Điểm đến"
        verbose_name_plural = "Điểm đến"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Banner(models.Model):
    """Mô hình banner quảng cáo"""
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Tiêu đề phụ")
    image_url = models.CharField(max_length=255, verbose_name="Đường dẫn hình ảnh")
    link = models.CharField(max_length=255, blank=True, verbose_name="Đường dẫn liên kết")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['order']
    
    def __str__(self):
        return self.title
