from django.contrib import admin
from .models import Booking, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'full_name', 'tour', 'tour_date', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'tour')
    search_fields = ('booking_number', 'full_name', 'email', 'phone')
    readonly_fields = ('booking_number', 'created_at', 'updated_at')
    inlines = [PaymentInline]
    fieldsets = (
        ('Thông tin đặt tour', {
            'fields': ('booking_number', 'user', 'tour', 'tour_date', 'status')
        }),
        ('Thông tin liên hệ', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Chi tiết đặt tour', {
            'fields': ('adults', 'children', 'special_request')
        }),
        ('Thanh toán', {
            'fields': ('total_price', 'payment_method', 'payment_status', 'payment_date')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid', payment_status=True)
    mark_as_paid.short_description = "Đánh dấu đã thanh toán"
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Đánh dấu đã xác nhận"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Đánh dấu đã hoàn thành"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Đánh dấu đã hủy"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('booking__booking_number', 'transaction_id')
