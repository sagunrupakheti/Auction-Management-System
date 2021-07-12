from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
from datetime import datetime, date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
def eighteenYears(value):
    today = date.today()
    #check years
    if (value.year + 18, value.month, value.day) > (today.year, today.month, today.day):
        raise ValidationError('User needs to be of atleast 18 years of age!')

def no_past(value):
    today = date.today()
    if value < today or value == today:
        raise ValidationError('Exam Date cannot be past day')

def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Production date cannot be future date')


class draftUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    firstName = models.CharField(max_length=255, )
    lastName = models.CharField(max_length=255, )
    email = models.EmailField(max_length=255,)
    dob = models.DateField(auto_now_add=False, auto_now=False, blank=True, validators=[eighteenYears])
    country = models.CharField(max_length=255, )
    city = models.CharField(max_length=255, )
    zip_code = models.CharField(max_length=5, )
    address = models.CharField(max_length=255, )
    country_code = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, blank=True)
    bank_account_number = models.IntegerField()
    bank_sort_code= models.IntegerField()
    client_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Pending')


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    firstName = models.CharField(max_length=255, )
    lastName = models.CharField(max_length=255, )
    email = models.EmailField(max_length=255,)
    dob = models.DateField(auto_now_add=False, auto_now=False, blank=True, validators=[eighteenYears])
    country = models.CharField(max_length=255, )
    city = models.CharField(max_length=255, )
    zip_code = models.CharField(max_length=5, )
    address = models.CharField(max_length=255, )
    country_code = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, blank=True)
    bank_account_number = models.IntegerField()
    bank_sort_code= models.IntegerField()
    client_type = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)


class Auction(models.Model):
    auction_id = models.AutoField(primary_key=True, unique=True)
    auction_name = models.CharField(max_length=255, )
    auction_description = models.TextField()
    auction_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, validators=[no_past])
    auction_status = models.CharField(max_length=255,default='Pending')

    def __str__(self):
        return self.auction_name


class Category(models.Model):
    category_name = models.CharField(max_length=255, primary_key=True)
    category_description = models.TextField()
    def __str__(self):
        return self.category_name

def current_year():
    return date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Item(models.Model):
    CHOICES = (('Landscape', 'Landscape'), ('Seascape', 'Seascape'), ('Portrait', 'Portrait'), ('Figure', 'Figure'),
               ('Still Life', 'Still Life'), ('Nude', 'Nude'), ('Animal', 'Animal'), ('Abstract', 'Abstract'), ('Other', 'Other'))
    item_lot = models.AutoField(primary_key=True, unique=True)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT, default=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user")
    item_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    production_year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1400), max_value_current_year])
    classification = models.CharField(max_length=255,choices= CHOICES)
    description =  models.TextField()
    estimated_price =  models.CharField(max_length=255)
    image1 = models.ImageField(upload_to='item_pics', blank=True)
    image2 = models.ImageField(upload_to='item_pics', blank=True)
    image3 = models.ImageField(upload_to='item_pics', blank=True)
    status = models.CharField(max_length=255,default='Pending')
    evaluation_text = models.TextField(default='Evaluated')

class Drawing(models.Model):
    MEDIUM = (('Pencil', 'Pencil'), ('Ink', 'Ink'), ('Charcoal', 'Charcoal'),('Other', 'Other'))
    FRAME = (('Yes', 'Yes'), ('No', 'No'))
    drawing = models.ForeignKey(Item, on_delete=models.PROTECT)
    medium = models.CharField(max_length=255,choices= MEDIUM)
    frame_status = models.CharField(max_length=255,choices= FRAME)
    height = models.IntegerField()
    length = models.IntegerField()

    @property
    def url(self):
        return self.drawing

class Painting(models.Model):
    MEDIUM = (('Oil', 'Oil'), ('Acrylic', 'Acrylic'), ('Watercolor', 'Watercolor'),('Other', 'Other'))
    FRAME = (('Yes', 'Yes'), ('No', 'No'))
    painting = models.ForeignKey(Item, on_delete=models.PROTECT)
    medium = models.CharField(max_length=255,choices= MEDIUM)
    frame_status = models.CharField(max_length=255,choices= FRAME)
    height = models.IntegerField()
    length = models.IntegerField()

class PhotographicImage(models.Model):
    TYPE = (('Black', 'Black'), ('White', 'White'))
    photographic_image = models.ForeignKey(Item, on_delete=models.PROTECT)
    type = models.CharField(max_length=255,choices= TYPE)
    height = models.IntegerField()
    length = models.IntegerField()

class Sculpture(models.Model):
    MATERIAL = (('Bronze', 'Bronze'), ('Marble', 'Marble'), ('Pewter', 'Pewter'),('Other', 'Other'))
    sculpture = models.ForeignKey(Item, on_delete=models.PROTECT)
    material = models.CharField(max_length=255,choices= MATERIAL)
    height = models.IntegerField()
    length = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()

class Carving(models.Model):
    MATERIAL = (('Oak', 'Oak'), ('Beach', 'Beach'), ('Pine', 'Pine'),('Willow', 'Willow'),('Other', 'Other'))
    carving = models.ForeignKey(Item, on_delete=models.PROTECT)
    material = models.CharField(max_length=255,choices= MATERIAL)
    height = models.IntegerField()
    length = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()

class StoreBidding(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    old_bid = models.IntegerField()
    current_bid = models.IntegerField()
    bidding_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Bidding(models.Model):
    item = models.OneToOneField(Item, on_delete=models.PROTECT)
    estimated_price = models.IntegerField()
    old_bid = models.IntegerField()
    current_bid = models.IntegerField()
    bidding_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Commission(models.Model):
    item = models.OneToOneField(Bidding, on_delete=models.PROTECT)
    item_info = models.ForeignKey(Item, on_delete=models.PROTECT, blank=True, default=1)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    sold_price = models.IntegerField()
    commission_amount = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)

class jointAccountRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, unique=True)
    notification_text = models.CharField(max_length=255)
    concerned_to = models.CharField(max_length=255)
    notification_date = models.DateField(auto_now=True)