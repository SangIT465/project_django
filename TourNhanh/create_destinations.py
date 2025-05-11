from apps.core.models import Destination
from django.utils.text import slugify
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourapp.settings')

# Tạo một số điểm đến phổ biến
destinations = [
    {
        'name': 'Hà Nội',
        'description': 'Thủ đô nghìn năm văn hiến với nhiều di tích lịch sử và văn hóa.',
        'image': 'https://images.unsplash.com/photo-1557750255-c76072a7aad1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'is_popular': True
    },
    {
        'name': 'TP Hồ Chí Minh',
        'description': 'Thành phố năng động nhất Việt Nam với nhiều điểm tham quan hấp dẫn.',
        'image': 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'is_popular': True
    },
    {
        'name': 'Đà Nẵng',
        'description': 'Thành phố đáng sống nhất Việt Nam với bãi biển đẹp và cầu Rồng nổi tiếng.',
        'image': 'https://images.unsplash.com/photo-1564310452-b4bec5261dc5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'is_popular': True
    },
    {
        'name': 'Nha Trang',
        'description': 'Thành phố biển với bãi biển đẹp và nhiều đảo hoang sơ.',
        'image': 'https://images.unsplash.com/photo-1577948000111-9c970dfe3743?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'is_popular': True
    },
    {
        'name': 'Phú Quốc',
        'description': 'Đảo ngọc với bãi biển cát trắng và nước biển trong xanh.',
        'image': 'https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'is_popular': True
    },
    {
        'name': 'Đà Lạt',
        'description': 'Thành phố ngàn hoa với khí hậu mát mẻ quanh năm.',
        'image': 'https://images.unsplash.com/photo-1575330933415-cea1e7ce53eb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'is_popular': True
    }
]

# Lưu vào cơ sở dữ liệu
for dest in destinations:
    slug = slugify(dest['name'])
    # Kiểm tra xem đã tồn tại chưa
    if not Destination.objects.filter(slug=slug).exists():
        Destination.objects.create(
            name=dest['name'],
            slug=slug,
            description=dest['description'],
            image=dest['image'],
            is_popular=dest['is_popular']
        )
        print(f'Đã tạo điểm đến: {dest["name"]}')
    else:
        print(f'Điểm đến {dest["name"]} đã tồn tại')
