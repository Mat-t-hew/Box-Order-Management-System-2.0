from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import Box, BoxType, Inventory, SalesTransaction

# Home Page
def home(request):
    categories = BoxType.objects.count()
    boxes = Box.objects.count()
    sales = SalesTransaction.objects.count()
    
    context = {
        'categories': categories,
        'products': boxes,
        'sales': sales
    }
    return render(request, 'home.html', context)

# Profile Page
@login_required
def profile(request):
    return render(request, 'profile.html')

# Update Password
@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'update_password.html', {'form': form})

# Register User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'reg_form': form})

# Box Categories (Box Types)
@login_required
def box_types(request):
    categories = BoxType.objects.all()
    return render(request, 'category_mgt.html', {'categories': categories})

# Inventory Page
@login_required
def inventory(request):
    inventory_list = Inventory.objects.all()
    return render(request, 'inventory.html', {'inventory': inventory_list})

# Sales Transactions
@login_required
def sales_transactions(request):
    sales = SalesTransaction.objects.all()
    return render(request, 'sales.html', {'sales': sales})

# Shared Files Page
@login_required
def share_file(request):
    return render(request, 'share-file.html')
