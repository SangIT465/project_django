from django import forms

class ContactForm(forms.Form):
    """Form liên hệ cho khách hàng"""
    name = forms.CharField(
        max_length=100, 
        label="Họ và tên",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ và tên'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ email'})
    )
    phone = forms.CharField(
        max_length=15, 
        label="Số điện thoại",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'})
    )
    message = forms.CharField(
        label="Nội dung",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Nhập nội dung tin nhắn'})
    )
