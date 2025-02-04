from email import message
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from box_management_system.settings import MEDIA_ROOT, MEDIA_URL
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from backoffice.forms import SaveStock, UserRegistration, UpdateProfile, UpdatePasswords, SaveBox_Type, SaveBox, SaveInvoice, SaveInvoiceItem
from backoffice.models import Box_Type, Box, Stock, Invoice, InvoiceItem
from cryptography.fernet import Fernet
from django.conf import settings
import base64

context = {
    'page_title' : 'File Management System',
}

#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    context['page_title'] = 'Home'
    context['categories'] = Box_Type.objects.count()
    context['boxs'] = Box.objects.count()
    context['sales'] = Invoice.objects.count()
    return render(request, 'home.html',context)

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request,'register.html',context)

@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html',context)

# Box_Type
@login_required
def box_type_mgt(request):
    context['page_title'] = "Box Categories"
    categories = Box_Type.objects.all()
    context['categories'] = categories

    return render(request, 'box_type_mgt.html', context)

@login_required
def save_box_type(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            category = Box_Type.objects.get(pk=request.POST['id'])
        else:
            category = None
        if category is None:
            form = SaveBox_Type(request.POST)
        else:
            form = SaveBox_Type(request.POST, instance= category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Box_Type has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

# Box Type Management
@login_required
def manage_box_type(request, pk=None):
    context['page_title'] = "Manage Box_Type"
    if not pk is None:
        category = Box_Type.objects.get(id = pk)
        context['box_type'] = category
    else:
        context['box_type'] = {}

    return render(request, 'manage_box_type.html', context)

@login_required
def delete_box_type(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            category = Box_Type.objects.get(id = request.POST['id'])
            category.delete()
            messages.success(request, 'Box_Type has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Box_Type has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Box_Type has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")
        
# box
@login_required
def box_mgt(request):
    context['page_title'] = "Box List"
    boxs = Box.objects.all()
    context['boxs'] = boxs

    return render(request, 'box_mgt.html', context)

@login_required
def save_box(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            product = Box.objects.get(pk=request.POST['id'])
        else:
            product = None
        if product is None:
            form = SaveBox(request.POST)
        else:
            form = SaveBox(request.POST, instance= product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Box has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def manage_box(request, pk=None):
    context['page_title'] = "Manage Box"
    if not pk is None:
        product = Box.objects.get(id = pk)
        context['box'] = product
    else:
        context['box'] = {}

    return render(request, 'manage_box.html', context)

@login_required
def delete_box(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            product = Box.objects.get(id = request.POST['id'])
            product.delete()
            messages.success(request, 'Box has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Box has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Box has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

#Inventory
@login_required
def inventory(request):
    context['page_title'] = 'Inventory'

    products = Box.objects.all()
    context['boxs'] = products

    return render(request, 'inventory.html', context)
#Inventory History
@login_required
def inv_history(request, pk= None):
    context['page_title'] = 'Inventory History'
    if pk is None:
        messages.error(request, "Box ID is not recognized")
        return redirect('inventory-page')
    else:
        product = Box.objects.get(id = pk)
        stocks = Stock.objects.filter(product = product).all()
        context['box'] = product
        context['stocks'] = stocks

        return render(request, 'inventory-history.html', context)

#Stock Form
@login_required
def manage_stock(request,pid = None ,pk = None):
    if pid is None:
        messages.error(request, "Box ID is not recognized")
        return redirect('inventory-page')
    context['pid'] = pid
    if pk is None:
        context['page_title'] = "Add New Stock"
        context['stock'] = {}
    else:
        context['page_title'] = "Manage New Stock"
        stock = Stock.objects.get(id = pk)
        context['stock'] = stock
    
    return render(request, 'manage_stock.html', context) 

@login_required
def save_stock(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            stock = Stock.objects.get(pk=request.POST['id'])
        else:
            stock = None
        if stock is None:
            form = SaveStock(request.POST)
        else:
            form = SaveStock(request.POST, instance= stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def delete_stock(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            stock = Stock.objects.get(id = request.POST['id'])
            stock.delete()
            messages.success(request, 'Stock has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Stock has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Stock has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def sales_mgt(request):
    context['page_title'] = 'Sales'
    products = Box.objects.filter(status = 1).all()
    context['boxs'] = products
    return render(request,'sales.html', context)


def get_box(request,pk = None):
    resp = {'status':'failed','data':{},'msg':''}
    if pk is None:
        resp['msg'] = 'Box ID is not recognized'
    else:
        product = Box.objects.get(id = pk)
        resp['data']['box'] = str(box.code + " - " + box.name)
        resp['data']['id'] = box.id
        resp['data']['price'] = box.price
        resp['status'] = 'success'
    
    return HttpResponse(json.dumps(resp),content_type="application/json")


def save_sales(request):
    resp = {'status':'failed', 'msg' : ''}
    id = 2
    if request.method == 'POST':
        pids = request.POST.getlist('pid[]')
        invoice_form = SaveInvoice(request.POST)
        if invoice_form.is_valid():
            invoice_form.save()
            invoice = Invoice.objects.last()
            for pid in pids:
                data = {
                    'invoice':invoice.id,
                    'box':pid,
                    'quantity':request.POST['quantity['+str(pid)+']'],
                    'price':request.POST['price['+str(pid)+']'],
                }
                print(data)
                ii_form = SaveInvoiceItem(data=data)
                # print(ii_form.data)
                if ii_form.is_valid():
                    ii_form.save()
                else:
                    for fields in ii_form:
                        for error in fields.errors:
                            resp['msg'] += str(error + "<br>")
                    break
            messages.success(request, "Sale Transaction has been saved.")
            resp['status'] = 'success'
            # invoice.delete()
        else:
            for fields in invoice_form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")

    return HttpResponse(json.dumps(resp),content_type="application/json")

def export_sales(request):
    return HttpResponse("Export Sales - Not implemented yet")

@login_required
def invoices(request):
    invoice =  Invoice.objects.all()
    context['page_title'] = 'Invoices'
    context['invoices'] = invoice

    return render(request, 'invoices.html', context)

@login_required
def delete_invoice(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            invoice = Invoice.objects.get(id = request.POST['id'])
            invoice.delete()
            messages.success(request, 'Invoice has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Invoice has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Invoice has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")
    