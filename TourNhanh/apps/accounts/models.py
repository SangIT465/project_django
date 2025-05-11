from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Mô hình thông tin chi tiết của người dùng"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    address = models.CharField(max_length=255, blank=True, verbose_name="Địa chỉ")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    avatar = models.CharField(max_length=255, blank=True, verbose_name="Đường dẫn ảnh đại diện")
    
    class Meta:
        verbose_name = "Hồ sơ người dùng"
        verbose_name_plural = "Hồ sơ người dùng"
    
    def __str__(self):
        return f"Hồ sơ của {self.user.username}"
