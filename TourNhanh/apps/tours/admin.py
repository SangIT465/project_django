from django.contrib import admin
from .models import TourCategory, Tour, TourImage, TourDate, Review

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 1

@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'category', 'duration', 'price', 'is_featured', 'is_active')
    list_filter = ('category', 'destination', 'is_featured', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TourImageInline, TourDateInline]
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'category', 'destination', 'duration', 'transport')
        }),
        ('Mô tả', {
            'fields': ('short_description', 'description', 'main_image')
        }),
        ('Giá', {
            'fields': ('price', 'discount_price')
        }),
        ('Chi tiết tour', {
            'fields': ('itinerary', 'includes', 'excludes', 'terms')
        }),
        ('Trạng thái', {
            'fields': ('is_featured', 'is_active')
        }),
    )

@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ('tour', 'start_date', 'end_date', 'price', 'available_seats', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('tour__title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'name', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved')
    search_fields = ('name', 'comment', 'tour__title')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Duyệt các đánh giá đã chọn"
