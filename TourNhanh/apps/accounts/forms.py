from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    """Form đăng ký người dùng mới"""
    password = forms.CharField(
        label="Mật khẩu", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'})
    )
    confirm_password = forms.CharField(
        label="Xác nhận mật khẩu", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại")
        return email
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Mật khẩu không khớp")
        
        return confirm_password

class UserLoginForm(forms.Form):
    """Form đăng nhập"""
    username = forms.CharField(
        label="Tên đăng nhập hoặc Email", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên đăng nhập hoặc email'})
    )
    password = forms.CharField(
        label="Mật khẩu", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Cho phép đăng nhập bằng email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                pass
        return username

class UserUpdateForm(forms.ModelForm):
    """Form cập nhật thông tin người dùng"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class ProfileForm(forms.ModelForm):
    """Form cập nhật thông tin hồ sơ người dùng"""
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
