from django import forms
from .models import *

class DraftUserInfoForm(forms.ModelForm):
    class Meta():
        model = draftUser
        CHOICES = (('Buyer', 'Buyer'), ('Seller', 'Seller'))
        fields = ('firstName', 'lastName','email', 'dob','country','city', 'zip_code', 'address','country_code',
                  'contact',
                  'bank_account_number','bank_sort_code','client_type')
        # labels = {
        # 'firstName' : " ",
        # 'lastName' : " "
        # }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_sort_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'client_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    # for password
    # password = forms.CharField(widget=forms.PasswordInput())
    # defines how userform class behaves
    class Meta():
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
        }
        label = ""
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','name': 'pass', 'id': 'pass'})
        }

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        CHOICES = (('Buyer', 'Buyer'), ('Seller', 'Seller'),('Joint','Joint'))
        fields = ('firstName', 'lastName','email', 'dob','country','city', 'zip_code', 'address','country_code',
                  'contact',
                  'bank_account_number','bank_sort_code','client_type')
        # labels = {
        # 'firstName' : " ",
        # 'lastName' : " "
        # }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_sort_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'client_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields=('category_name','category_description')
        widgets={
            'category_name':forms.TextInput(attrs={'class': 'form-control'}),
            'category_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AddAdminUserForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        CHOICES = (('Admin', 'Admin'), ('Evaluator', 'Evaluator'))
        fields = ('firstName', 'lastName','email', 'dob','country','city', 'zip_code', 'address','country_code',
                  'contact',
                  'bank_account_number','bank_sort_code','client_type')
        # labels = {
        # 'firstName' : " ",
        # 'lastName' : " "
        # }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_sort_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'client_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        exclude = ['client_type', ]
        fields = ('firstName', 'lastName','email', 'dob','country','city', 'zip_code', 'address','country_code',
                  'contact',
                  'bank_account_number','bank_sort_code',)
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_sort_code': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProfilePicForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        exclude = ['client_type','firstName', 'lastName','email', 'dob','country','city', 'zip_code', 'address','country_code',
                  'contact',
                  'bank_account_number','bank_sort_code', ]
        fields = ('profile_pic',)
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AuctionForm(forms.ModelForm):
    class Meta():
        model = Auction
        fields=('auction_name','auction_description','auction_date')
        widgets = {
            'auction_name':forms.TextInput(attrs={'class': 'form-control'}),
            'auction_description':forms.Textarea(attrs={'class': 'form-control'}),
            'auction_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
        }

class AuctionFormStatus(forms.ModelForm):
    class Meta():
        model = Auction
        CHOICES = (('Pending', 'Pending'),('Advanced Bidding', 'Advanced Bidding'), ('Live', 'Live'), ('Expired', 'Expired'))
        fields=('auction_name','auction_description','auction_date','auction_status')
        widgets = {
            'auction_name':forms.TextInput(attrs={'class': 'form-control','name':'auction_name'}),
            'auction_description':forms.Textarea(attrs={'class': 'form-control'}),
            'auction_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
            'auction_status': forms.Select(choices=CHOICES,attrs={'class': 'form-control'}),
        }

class ItemForm(forms.ModelForm):
    class Meta():
        model = Item
        exclude = ['user','auction',]
        fields = ('auction','artist_name','item_name','category','production_year','classification','description','estimated_price','image1',
                  'image2','image3')
        widgets={
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'artist_name':forms.TextInput(attrs={'class': 'form-control'}),
            'category':forms.Select(attrs={'class': 'form-control','name':'category'}),
            'production_year':forms.NumberInput(attrs={'class': 'form-control'}),
            'classification':forms.Select(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
            'estimated_price':forms.NumberInput(attrs={'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),

        }

class DrawingForm(forms.ModelForm):
    class Meta():
        model = Drawing
        exclude = ['drawing', ]
        fields = ('medium','frame_status','height','length')
        widgets={
            'medium':forms.Select(attrs={'class': 'form-control'}),
            'frame_status': forms.Select(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PaintingForm(forms.ModelForm):
    class Meta():
        model = Painting
        exclude = ['painting', ]
        fields = ('medium','frame_status','height','length')
        widgets={
            'medium':forms.Select(attrs={'class': 'form-control'}),
            'frame_status': forms.Select(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PhotographicImageForm(forms.ModelForm):
    class Meta():
        model = PhotographicImage
        exclude = ['photographic_image', ]
        fields = ('type','height','length')
        widgets={
            'type': forms.Select(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SculptureForm(forms.ModelForm):
    class Meta():
        model = Sculpture
        exclude = ['sculpture', ]
        fields = ('material','height','length','width','weight')
        widgets={
            'material': forms.Select(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CarvingForm(forms.ModelForm):
    class Meta():
        model = Carving
        exclude = ['carving', ]
        fields = ('material','height','length','width','weight')
        widgets={
            'material': forms.Select(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }
