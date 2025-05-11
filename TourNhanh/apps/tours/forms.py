from django import forms
from .models import Review
from apps.core.models import Destination

class TourSearchForm(forms.Form):
    """Form tìm kiếm tour"""
    keyword = forms.CharField(
        required=False, 
        label="Từ khóa",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tìm kiếm tour...'})
    )
    destination = forms.ModelChoiceField(
        queryset=Destination.objects.filter(is_active=True),
        required=False,
        empty_label="Tất cả điểm đến",
        label="Điểm đến",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ModelChoiceField(
        queryset=None,  # Sẽ được gán trong __init__
        required=False,
        empty_label="Tất cả loại tour",
        label="Loại tour",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    duration = forms.ChoiceField(
        choices=[
            ('', 'Tất cả thời gian'),
            ('1-3', '1-3 ngày'),
            ('4-7', '4-7 ngày'),
            ('8-14', '8-14 ngày'),
            ('15+', 'Trên 15 ngày'),
        ],
        required=False,
        label="Thời gian",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    price_min = forms.IntegerField(
        required=False,
        min_value=0,
        label="Giá từ",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá thấp nhất'})
    )
    price_max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Đến",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá cao nhất'})
    )
    
    def __init__(self, *args, **kwargs):
        super(TourSearchForm, self).__init__(*args, **kwargs)
        from .models import TourCategory
        self.fields['category'].queryset = TourCategory.objects.all()

class ReviewForm(forms.ModelForm):
    """Form đánh giá tour"""
    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'rating': forms.Select(
                attrs={'class': 'form-select'},
                choices=[(i, f"{i} sao") for i in range(1, 6)]
            ),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Nhận xét của bạn'}),
        }
