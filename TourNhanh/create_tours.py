from apps.tours.models import TourCategory, Tour, TourImage, TourDate
from apps.core.models import Destination
from django.utils.text import slugify
from datetime import datetime, timedelta

# Tạo danh mục tour
categories = [
    {
        'name': 'Tour biển',
        'description': 'Khám phá các bãi biển đẹp nhất Việt Nam',
        'icon': 'fa-umbrella-beach'
    },
    {
        'name': 'Tour núi',
        'description': 'Chiêm ngưỡng vẻ đẹp hùng vĩ của núi non',
        'icon': 'fa-mountain'
    },
    {
        'name': 'Tour văn hóa',
        'description': 'Tìm hiểu văn hóa và lịch sử lâu đời của Việt Nam',
        'icon': 'fa-landmark'
    },
    {
        'name': 'Tour ẩm thực',
        'description': 'Khám phá nền ẩm thực phong phú của Việt Nam',
        'icon': 'fa-utensils'
    },
    {
        'name': 'Tour sinh thái',
        'description': 'Khám phá thiên nhiên hoang sơ và bảo tồn thiên nhiên',
        'icon': 'fa-leaf'
    }
]

for cat in categories:
    slug = slugify(cat['name'])
    # Kiểm tra xem đã tồn tại chưa
    if not TourCategory.objects.filter(slug=slug).exists():
        TourCategory.objects.create(
            name=cat['name'],
            slug=slug,
            description=cat['description'],
            icon=cat['icon']
        )
        print(f'Đã tạo danh mục: {cat["name"]}')
    else:
        print(f'Danh mục {cat["name"]} đã tồn tại')

# Tạo tour du lịch
tours = [
    # Hà Nội - Tour văn hóa
    {
        'title': 'Khám phá Hà Nội - Vốn văn hóa nghìn năm',
        'category_name': 'Tour văn hóa',
        'destination_name': 'Hà Nội',
        'short_description': 'Khám phá trọn vẹn vốn văn hóa của Hà Nội qua các di tích lịch sử, phố cổ, làng nghề truyền thống và ẩm thực đặc sắc.',
        'description': 'Tour du lịch Hà Nội sẽ đưa bạn qua các di tích lịch sử nổi tiếng như Hồ Gươm, Văn Miếu - Quốc Tử Giám, Hoàng Thành Thăng Long. Tận hưởng vẻ đẹp của phố cổ Hà Nội, thưởng thức cà phê truyền thống và khám phá các làng nghề như Bát Tràng, Văn Phuc. Đặc biệt, bạn sẽ được thưởng thức các món ăn đặc sắc của Hà Nội như phở, bún chả, chá cá... Tour Hà Nội mang đến cho bạn trải nghiệm văn hóa phong phú, ấm cúng và rất "Hà Nội".',
        'duration': 3,
        'price': 2500000,
        'discount_price': 2200000,
        'main_image': 'https://images.unsplash.com/photo-1627894483216-2138af692e32?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'itinerary': '**Ngày 1: Khám phá phố cổ Hà Nội**\n\n- Sáng: Tham quan Hồ Hoàn Kiếm, đền Ngọc Sơn\n- Trưa: Ăn trưa tại nhà hàng đặc sản, thưởng thức bún chả\n- Chiều: Tham quan phố cổ Hà Nội, mua sắm tại phố Hàng Đào\n- Tối: Ăn tối và thưởng thức cà phê phố cổ\n\n**Ngày 2: Di tích lịch sử**\n\n- Sáng: Tham quan Lăng Bác Hồ, Chùa Một Cột\n- Trưa: Ăn trưa tại nhà hàng, thưởng thức phở Hà Nội\n- Chiều: Tham quan Văn Miếu - Quốc Tử Giám, Hoàng Thành Thăng Long\n- Tối: Xem biểu diễn múa rối nước tại nhà hát lớn\n\n**Ngày 3: Văn hóa làng nghề**\n\n- Sáng: Tham quan làng gốm Bát Tràng\n- Trưa: Ăn trưa tại làng nghề\n- Chiều: Tham quan làng lụa Văn Phuc\n- Tối: Ăn tối chia tay',
        'includes': '- Vé tham quan các điểm trong chương trình\n- Hướng dẫn viên tiếng Việt nhiệt tình, kinh nghiệm\n- Xe ô tô đưa đón theo lịch trình\n- 2 đêm khách sạn 3 sao (2 người/phòng)\n- Ăn uống theo chương trình (2 bữa sáng, 3 bữa trưa, 3 bữa tối)\n- Nước uống trên xe\n- Bảo hiểm du lịch',
        'excludes': '- Đồ uống trong các bữa ăn\n- Chi phí cá nhân phát sinh\n- Tip cho hướng dẫn viên và lái xe\n- Các dịch vụ không được đề cập trong phần bao gồm',
        'terms': '- Trẻ em dưới 2 tuổi: Miễn phí, ăn ngủ cùng bố mẹ\n- Trẻ em từ 2-5 tuổi: Tính 50% giá tour\n- Trẻ em từ 6-11 tuổi: Tính 75% giá tour\n- Trẻ em từ 12 tuổi trở lên: Tính như người lớn\n\n- Hủy tour trước 7 ngày: Hoàn lại 80% tổng giá tour\n- Hủy tour trước 5 ngày: Hoàn lại 50% tổng giá tour\n- Hủy tour trong vòng 3 ngày: Không hoàn tiền',
        'transport': 'car',
        'is_featured': True,
        'images': [
            'https://images.unsplash.com/photo-1583417319070-4a69db38a482?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
            'https://images.unsplash.com/photo-1470004914212-05527e49370b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80'
        ],
        'dates': [
            {'start': 7, 'available': 15},
            {'start': 14, 'available': 20},
            {'start': 21, 'available': 10}
        ]
    },
    # Đà Nẵng - Tour biển
    {
        'title': 'Đà Nẵng - Ngũ Hành Sơn - Hội An',
        'category_name': 'Tour biển',
        'destination_name': 'Đà Nẵng',
        'short_description': 'Khám phá thành phố Đà Nẵng năng động, tắm biển Mỹ Khê, leo núi Ngũ Hành Sơn và dạo phố cổ Hội An.',
        'description': 'Tour du lịch Đà Nẵng mang đến cho bạn trải nghiệm tuyệt vời tại thành phố đáng sống nhất Việt Nam. Tận hưởng không khí trong lành và nước biển xanh mát tại bãi biển Mỹ Khê. Chiêm ngưỡng vẻ đẹp của cầu Rồng biểu tượng của thành phố. Khám phá núi Ngũ Hành Sơn huyền bí với các hang động và chùa chiền. Và đắm mình trong không gian cổ kính của phố cổ Hội An - Di sản Văn hóa Thế giới được UNESCO công nhận.',
        'duration': 4,
        'price': 4500000,
        'discount_price': 4000000,
        'main_image': 'https://images.unsplash.com/photo-1564310452-b4bec5261dc5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
        'itinerary': '**Ngày 1: Đà Nẵng - Biển Mỹ Khê**\n\n- Sáng: Đón sân bay, nhận phòng khách sạn\n- Trưa: Ăn trưa, nghỉ ngơi\n- Chiều: Tắm biển Mỹ Khê, tự do thưởng thức hải sản tươi sống\n- Tối: Khám phá phố đêm Đà Nẵng, ngắm cầu Rồng phun lửa\n\n**Ngày 2: Bán đảo Sơn Trà - Ngũ Hành Sơn**\n\n- Sáng: Tham quan bán đảo Sơn Trà, chùa Linh Ứng\n- Trưa: Ăn trưa tại nhà hàng địa phương\n- Chiều: Tham quan núi Ngũ Hành Sơn, động Huyền Không, chùa Non Nước\n- Tối: Ăn tối, tự do khám phá thành phố\n\n**Ngày 3: Hội An**\n\n- Sáng: Di chuyển đến Hội An\n- Trưa: Ăn trưa, thưởng thức đặc sản Hội An\n- Chiều: Tham quan phố cổ Hội An: Chùa Cầu, Nhà cổ Phùng Hưng, Hội quán Phước Kiến\n- Tối: Ăn tối, ngắm phố cổ với đèn lồng đông đảo\n\n**Ngày 4: Bà Nà Hills - Tiễn sân bay**\n\n- Sáng: Tham quan Bà Nà Hills, cầu Vàng\n- Trưa: Ăn trưa tại Bà Nà\n- Chiều: Mua sắm đặc sản, tiễn sân bay',
        'includes': '- Vé tham quan các điểm trong chương trình\n- Hướng dẫn viên tiếng Việt nhiệt tình, kinh nghiệm\n- Xe ô tô đưa đón theo lịch trình\n- 3 đêm khách sạn 4 sao (2 người/phòng)\n- Ăn uống theo chương trình (3 bữa sáng, 4 bữa trưa, 4 bữa tối)\n- Nước uống trên xe\n- Vé cáp treo Bà Nà Hills\n- Bảo hiểm du lịch',
        'excludes': '- Vé máy bay khứ hồi\n- Đồ uống trong các bữa ăn\n- Chi phí cá nhân phát sinh\n- Tip cho hướng dẫn viên và lái xe\n- Các dịch vụ không được đề cập trong phần bao gồm',
        'terms': '- Trẻ em dưới 2 tuổi: Miễn phí, ăn ngủ cùng bố mẹ\n- Trẻ em từ 2-5 tuổi: Tính 50% giá tour\n- Trẻ em từ 6-11 tuổi: Tính 75% giá tour\n- Trẻ em từ 12 tuổi trở lên: Tính như người lớn\n\n- Hủy tour trước 7 ngày: Hoàn lại 80% tổng giá tour\n- Hủy tour trước 5 ngày: Hoàn lại 50% tổng giá tour\n- Hủy tour trong vòng 3 ngày: Không hoàn tiền',
        'transport': 'car',
        'is_featured': True,
        'images': [
            'https://images.unsplash.com/photo-1528127269322-539801943592?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80',
            'https://images.unsplash.com/photo-1579873542903-b9064ba3ef9a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1600&q=80'
        ],
        'dates': [
            {'start': 5, 'available': 10},
            {'start': 12, 'available': 15},
            {'start': 19, 'available': 20}
        ]
    }
]

# Xử lý dữ liệu tour
for tour_data in tours:
    # Lấy danh mục và điểm đến
    try:
        category = TourCategory.objects.get(name=tour_data['category_name'])
        destination = Destination.objects.get(name=tour_data['destination_name'])
        
        # Tạo slug
        slug = slugify(tour_data['title'])
        
        # Kiểm tra xem tour đã tồn tại chưa
        if not Tour.objects.filter(slug=slug).exists():
            # Tạo tour mới
            tour = Tour.objects.create(
                category=category,
                destination=destination,
                title=tour_data['title'],
                slug=slug,
                short_description=tour_data['short_description'],
                description=tour_data['description'],
                duration=tour_data['duration'],
                price=tour_data['price'],
                discount_price=tour_data.get('discount_price'),
                main_image=tour_data['main_image'],
                itinerary=tour_data['itinerary'],
                includes=tour_data['includes'],
                excludes=tour_data['excludes'],
                terms=tour_data['terms'],
                transport=tour_data['transport'],
                is_featured=tour_data.get('is_featured', False)
            )
            print(f'Đã tạo tour: {tour_data["title"]}')
            
            # Thêm hình ảnh cho tour
            for i, image_url in enumerate(tour_data.get('images', [])):
                TourImage.objects.create(
                    tour=tour,
                    image_url=image_url,
                    caption=f'Hình ảnh {i+1} của {tour.title}',
                    order=i
                )
            
            # Tạo các ngày khởi hành
            today = datetime.now().date()
            for date_info in tour_data.get('dates', []):
                # Tính ngày khởi hành (ngày hiện tại + số ngày trong date_info['start'])
                start_date = today + timedelta(days=date_info['start'])
                end_date = start_date + timedelta(days=tour.duration - 1)
                
                TourDate.objects.create(
                    tour=tour,
                    start_date=start_date,
                    end_date=end_date,
                    available_seats=date_info.get('available', 20),
                    is_active=True
                )
                print(f'  - Đã tạo ngày khởi hành: {start_date}')
        else:
            print(f'Tour {tour_data["title"]} đã tồn tại')
    except TourCategory.DoesNotExist:
        print(f'Không tìm thấy danh mục: {tour_data["category_name"]}')
    except Destination.DoesNotExist:
        print(f'Không tìm thấy điểm đến: {tour_data["destination_name"]}')
    except Exception as e:
        print(f'Lỗi khi tạo tour {tour_data["title"]}: {str(e)}')
