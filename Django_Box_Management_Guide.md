
# Django Box Management System Guide

## Step 1: Set Up the Environment
### Install Django and Set Up Virtual Environment
```bash
# Create and activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows 10: .\env\Scripts\activate

# Install Django
pip install django
```

### Create a Django Project
```bashm
django-admin startproject BoxManagement
cd BoxManagement
```

## Step 2: Create the Application
### Create an App for the Project
```bash
python manage.py startapp box_app
```

### Register the App
In `BoxManagement/settings.py`, add `box_app` to the `INSTALLED_APPS` list:
```python
INSTALLED_APPS = [
    ...
    'box_app',
]
```

## Step 3: Set Up Models
### Define Models in `box_app/models.py`
```python
from django.db import models

class Box(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Box {self.id}"
```

### Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 4: Create Admin Interface
### Register the Model in `box_app/admin.py`
```python
from django.contrib import admin
from .models import Box

admin.site.register(Box)
```

### Create a Superuser
```bash
python manage.py createsuperuser
```

## Step 5: Build the Client Portal Views
### Create Views in `box_app/views.py`
```python
from django.shortcuts import render
from .models import Box

def client_portal(request):
    boxes = Box.objects.all()
    return render(request, 'box_app/client_portal.html', {'boxes': boxes})
```

### Create URLs in `box_app/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_portal, name='client_portal'),
]
```

### Include the App’s URLs in `BoxManagement/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('box_app.urls')),
]
```

### Create HTML Templates in `box_app/templates/box_app/client_portal.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Client Portal</title>
</head>
<body>
    <h1>Available Boxes</h1>
    <ul>
        {% for box in boxes %}
            <li>{{ box.id }}: {{ box.length }} x {{ box.width }} x {{ box.height }} - Quantity: {{ box.quantity }} - Price: {{ box.price }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

## Step 6: Build the Admin Portal
### Extend Views in `box_app/views.py`
```python
from django.shortcuts import redirect
from django.http import HttpResponse

def admin_portal(request):
    if request.method == 'POST':
        length = request.POST['length']
        width = request.POST['width']
        height = request.POST['height']
        quantity = request.POST['quantity']
        price = request.POST['price']
        Box.objects.create(length=length, width=width, height=height, quantity=quantity, price=price)
        return redirect('admin_portal')
    return render(request, 'box_app/admin_portal.html')
```

### Update URLs in `box_app/urls.py`
```python
urlpatterns = [
    path('client/', views.client_portal, name='client_portal'),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
]
```

### Create Templates for Admin Portal
`box_app/templates/box_app/admin_portal.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Admin Portal</title>
</head>
<body>
    <h1>Admin Portal</h1>
    <form method="post">
        {% csrf_token %}
        <label>Length: <input type="text" name="length"></label><br>
        <label>Width: <input type="text" name="width"></label><br>
        <label>Height: <input type="text" name="height"></label><br>
        <label>Quantity: <input type="number" name="quantity"></label><br>
        <label>Price: <input type="text" name="price"></label><br>
        <button type="submit">Add Box</button>
    </form>
</body>
</html>
```

## Step 7: Run the Server
### Start the Django Development Server
```bash
python manage.py runserver
```

### Access the Portals
- Client Portal: `http://127.0.0.1:8000/client/`
- Admin Portal: `http://127.0.0.1:8000/admin-portal/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Step 8: Testing and Deployment
### Run Tests
```bash
python manage.py test
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Deployment
Follow the instructions for deploying Django apps on platforms like Heroku, AWS, or any web server.

---

This guide provides step-by-step instructions for building the Box Management System using Django. Copy and paste the commands and code snippets as needed.
