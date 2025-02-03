from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Box_Type, Box, Stock, Invoice, InvoiceItem
from datetime import datetime

class UserRegistration(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text="The email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"The email {email} is already taken.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"The username {username} is already taken.")
        return username

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError("Incorrect current password")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Confirm New Password")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class SaveBox_Type(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea())
    status = forms.ChoiceField(choices=[('1', 'Active'), ('2', 'Inactive')])

    class Meta:
        model = Box_Type
        fields = ('name', 'description', 'status')

    def clean_name(self):
        name = self.cleaned_data['name']
        if Box_Type.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise forms.ValidationError(f"A Box Type with the name '{name}' already exists.")
        return name

class SaveBox(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea())
    status = forms.ChoiceField(choices=[('1', 'Active'), ('2', 'Inactive')])

    class Meta:
        model = Box
        fields = ('code', 'name', 'description', 'status', 'price')

    def clean_code(self):
        code = self.cleaned_data['code']
        if Box.objects.exclude(id=self.instance.id).filter(code=code).exists():
            raise forms.ValidationError(f"A Box with the code '{code}' already exists.")
        return code

class SaveStock(forms.ModelForm):
    box = forms.CharField(max_length=30)
    quantity = forms.CharField(max_length=250)
    type = forms.ChoiceField(choices=[('1', 'Stock-in'), ('2', 'Stock-Out')])

    class Meta:
        model = Stock
        fields = ('box', 'quantity', 'type')

    def clean_box(self):
        box_id = self.cleaned_data['box']
        try:
            return Box.objects.get(id=box_id)
        except Box.DoesNotExist:
            raise forms.ValidationError("Invalid Box ID")

class SaveInvoice(forms.ModelForm):
    transaction = forms.CharField(max_length=100)
    customer = forms.CharField(max_length=250)
    total = forms.FloatField()

    class Meta:
        model = Invoice
        fields = ('transaction', 'customer', 'total')

    def clean_transaction(self):
        pref = datetime.today().strftime('%Y%m%d')
        transaction = ''
        code = str(1).zfill(4)
        while Invoice.objects.filter(transaction=str(pref + code)).exists():
            code = str(int(code) + 1).zfill(4)
        return str(pref + code)

class SaveInvoiceItem(forms.ModelForm):
    invoice = forms.CharField(max_length=30)
    box = forms.CharField(max_length=30)
    quantity = forms.CharField(max_length=100)
    price = forms.CharField(max_length=100)

    class Meta:
        model = InvoiceItem
        fields = ('invoice', 'box', 'quantity', 'price')

    def clean_invoice(self):
        invoice_id = self.cleaned_data['invoice']
        try:
            return Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise forms.ValidationError("Invalid Invoice ID")

    def clean_box(self):
        box_id = self.cleaned_data['box']
        try:
            return Box.objects.get(id=box_id)
        except Box.DoesNotExist:
            raise forms.ValidationError("Invalid Box ID")

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if not qty.isnumeric():
            raise forms.ValidationError("Quantity must be a valid number")
        return int(qty)
