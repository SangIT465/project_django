from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('tour/<int:tour_id>/', views.booking_form, name='booking_form'),
    path('tour/<int:tour_id>/date/<int:date_id>/', views.booking_form, name='booking_form_with_date'),
    path('confirm/<int:booking_id>/', views.booking_confirm, name='booking_confirm'),
    path('bank-transfer/<int:booking_id>/', views.bank_transfer_payment, name='bank_transfer_payment'),
    path('online-payment/<int:booking_id>/', views.online_payment, name='online_payment'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('history/', views.booking_history, name='booking_history'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
