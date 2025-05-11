from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    """Form đặt tour"""
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'address', 'adults', 'children', 'special_request']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ'}),
            'adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Yêu cầu đặc biệt (nếu có)'}),
        }
    
    def clean_adults(self):
        adults = self.cleaned_data.get('adults')
        if adults < 1:
            raise forms.ValidationError("Phải có ít nhất 1 người lớn")
        return adults
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Kiểm tra định dạng số điện thoại
        if not phone.isdigit() or (len(phone) != 10 and len(phone) != 11):
            raise forms.ValidationError("Số điện thoại không hợp lệ")
        return phone

class PaymentForm(forms.Form):
    """Form chọn phương thức thanh toán"""
    payment_method = forms.ChoiceField(
        choices=Booking.PAYMENT_METHOD_CHOICES,
        label="Phương thức thanh toán",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
