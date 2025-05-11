from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm, UserUpdateForm
from .models import Profile

def register(request):
    """Đăng ký tài khoản mới"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Tạo người dùng mới
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            try:
                with transaction.atomic():
                    user.save()
                    # Tạo profile cho người dùng
                    Profile.objects.create(user=user)
                    
                    # Đăng nhập người dùng
                    user = authenticate(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                    )
                    login(request, user)
                    
                    messages.success(request, 'Đăng ký tài khoản thành công!')
                    return redirect('core:home')
            except Exception as e:
                messages.error(request, f'Đã xảy ra lỗi: {str(e)}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    """Đăng nhập người dùng"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                
                # Chuyển hướng đến trang tiếp theo hoặc trang chủ
                next_page = request.GET.get('next', 'core:home')
                return redirect(next_page)
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    """Xem và cập nhật thông tin cá nhân"""
    # Lấy hoặc tạo profile cho người dùng
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_obj)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Thông tin cá nhân đã được cập nhật!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def change_password(request):
    """Thay đổi mật khẩu"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Kiểm tra mật khẩu cũ
        if not request.user.check_password(old_password):
            messages.error(request, 'Mật khẩu cũ không đúng.')
            return redirect('accounts:change_password')
        
        # Kiểm tra mật khẩu mới và xác nhận
        if new_password != confirm_password:
            messages.error(request, 'Mật khẩu mới và xác nhận mật khẩu không khớp.')
            return redirect('accounts:change_password')
        
        # Thay đổi mật khẩu
        request.user.set_password(new_password)
        request.user.save()
        
        # Đăng nhập lại
        user = authenticate(username=request.user.username, password=new_password)
        login(request, user)
        
        messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/change_password.html')
