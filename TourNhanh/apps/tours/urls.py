from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('<slug:slug>/', views.tour_detail, name='tour_detail'),
    path('diem-den/<slug:destination_slug>/', views.tours_by_destination, name='tours_by_destination'),
    path('loai-tour/<slug:category_slug>/', views.tours_by_category, name='tours_by_category'),
]
