import datetime
import json
import schedule
import time

from dateutil import parser
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.functional import empty

from . import forms
from .forms import DraftUserInfoForm, UserProfileInfoForm, CategoryForm, AddAdminUserForm, UserForm, AuctionForm, \
    ItemForm, DrawingForm, PaintingForm, PhotographicImageForm, SculptureForm, CarvingForm, AuctionFormStatus, \
    EditProfileForm, ProfilePicForm
from .models import draftUser, User, UserProfileInfo, Category, Auction, Item, Drawing, Painting, PhotographicImage, \
    Sculpture, Carving, Bidding, Commission, StoreBidding, jointAccountRequest, Notification
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from itertools import chain

def user_logout(request):
    logout(request)
    return redirect('index')


def index(request):
    form = DraftUserInfoForm
    draft_user = draftUser()
    if request.method == "POST":
        if 'registerUser' in request.POST:
            draft_form = DraftUserInfoForm(data=request.POST)
            if draft_form.is_valid():
                draft_form.save()
                messages.success(request, 'Your registration request has been successfully sent! Please wait for confirmation!')
                return redirect('index')
            else:
                messages.error(request, 'Failed to send request!')
                return redirect('index')
        if 'loginUser' in request.POST:
            global getReq
            # username in login view
            username = request.POST.get('username')
            password = request.POST.get('password')
            users = User.objects.all().filter(username=username)
            profile = UserProfileInfo.objects.filter(user__in=users).values('client_type').first()
            getFinal = ''
            if (profile != None):
                getFinal = profile.get('client_type')
            # for authentication
            user = authenticate(username=username, password=password)
            # if the user if a teacher
            if user and getFinal == 'Admin':
                login(request, user)
                return HttpResponseRedirect('landingPage')
            # if the user is a student
            elif user and getFinal == 'Evaluator':
                login(request, user)
                return HttpResponseRedirect('landingPage')
            elif user and getFinal == 'Buyer':
                login(request, user)
                return HttpResponseRedirect('landingPage')
            elif user and getFinal == 'Seller':
                login(request, user)
                return HttpResponseRedirect('landingPage')
            elif user and getFinal == 'Joint':
                login(request, user)
                return HttpResponseRedirect('landingPage')
            else:
                messages.error(request, 'Please enter correct credentials!')
    total_buyers = UserProfileInfo.objects.all().filter(client_type='Buyer').values('user').annotate(
        total=Count('user'))
    buyers = total_buyers.aggregate(sum=Sum('total'))['sum']
    total_sellers = UserProfileInfo.objects.all().filter(client_type='Seller').values('user').annotate(
        total=Count('user'))
    sellers = total_sellers.aggregate(sum=Sum('total'))['sum']
    total_auctions = Auction.objects.all().values('auction_id').annotate(
        total=Count('auction_id'))
    auctions = total_auctions.aggregate(sum=Sum('total'))['sum']
    total_items = Item.objects.all().values('item_lot').annotate(
        total=Count('item_lot'))
    items = total_items.aggregate(sum=Sum('total'))['sum']
    return render(request,'index.html',{'form':form,'buyers':buyers,'sellers':sellers,'auctions':auctions,'items':items})

def landingPage(request):
    category = Category.objects.all()
    ac = Auction.objects.all().filter(auction_status='Live') | Auction.objects.all().filter(auction_status='Pending')| Auction.objects.all().filter(auction_status='Advanced Bidding')
    user = User.objects.all().filter(username=request.user).first()
    temp = ''
    profileEdit = UserProfileInfo.objects.all().filter(user=user).first()
    form = ProfilePicForm
    if request.user.is_authenticated:
        getUser = UserProfileInfo.objects.get(user=user)
        notification=''
        if getUser.client_type == "Buyer":
            temp = 'buyerDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
                concerned_to=request.user)
        elif getUser.client_type == "Seller":
            temp = 'sellerDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Seller') | Notification.objects.all().filter(
                concerned_to=request.user)
        elif getUser.client_type == "Joint":
            temp = 'jointDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
                concerned_to='Seller') | Notification.objects.all().filter(
                concerned_to='Joint') | Notification.objects.all().filter(concerned_to=request.user)
        elif getUser.client_type == "Admin":
            temp = 'adminDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Admin').order_by('-notification_date')
        elif getUser.client_type == "Evaluator":
            temp = 'evaluatorDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Evaluator')
    else:
        temp='normalDashboard.html'
        notification=''
    items = Item.objects.all().filter(status='Accepted').annotate(
        total=Count('auction')).order_by('estimated_price')

    if request.method == "POST":
        if 'searchFor' in request.POST:
            print('hahahaha')
            query_dictionary = {
                'artist_name': request.POST.get('searchBar'),
                'category__category_name': request.POST.get('searchBar'),
                # 'auction__auction_date': request.POST.get('auction_date'),
                'classification': request.POST.get('searchBar'),
                'estimated_price': request.POST.get('searchBar  '),
            }
            not_none_parameters = {single_query: query_dictionary.get(single_query) for single_query in query_dictionary
                                   if
                                   query_dictionary.get(single_query) is not None}
            filter_list = Q()
            for item in not_none_parameters:
                filter_list |= Q(**{item: not_none_parameters.get(item)})
            items = Item.objects.filter(filter_list, status='Accepted')
        elif 'filterSearch' in request.POST:
            d= request.POST.get('auction_date')
            if d=='':
                query_dictionary = {
                    'artist_name': request.POST.get('artist_name'),
                    'category__category_name': request.POST.get('category'),
                    'classification': request.POST.get('classification'),
                    'estimated_price': request.POST.get('estimated_price'),
                }
            else:
                query_dictionary = {
                    'artist_name': request.POST.get('artist_name'),
                    'category__category_name': request.POST.get('category'),
                    'auction__auction_date': parser.parse(d),
                    'classification': request.POST.get('classification'),
                    'estimated_price': request.POST.get('estimated_price'),
                }
            not_none_parameters = {single_query: query_dictionary.get(single_query) for single_query in query_dictionary
                                   if
                                   query_dictionary.get(single_query) is not None}
            filter_list = Q()
            for item in not_none_parameters:
                filter_list |= Q(**{item: not_none_parameters.get(item)})
            items = Item.objects.filter(filter_list, status='Accepted')
    return render(request,'landingPage.html',{'temp':temp,'category':category,'items':items,'ac':ac,'notification':notification})


def adminDashboard(request):
    user = User.objects.all().filter(username=request.user).first()
    info = UserProfileInfo.objects.all().filter(user=user)
    return render(request, 'adminDashboard.html', {'info':info})

def normalDashboard(request):
    return render(request, 'normalDashboard.html', {})

def adminDashboardView(request):
    item = Commission.objects.all()
    user_type = UserProfileInfo.objects.all().values('client_type').annotate(
        total=Count('firstName')).order_by('client_type')
    total_items = Item.objects.all().values('category').annotate(
        total=Count('item_lot')).order_by('category')
    notification = Notification.objects.all().filter(concerned_to='Admin')
    total_buyers = UserProfileInfo.objects.all().filter(client_type='Buyer').annotate(
        total=Count('firstName'))
    buyers = total_buyers.aggregate(sum=Sum('total'))['sum']
    print(buyers)
    total_sellers = UserProfileInfo.objects.all().filter(client_type='Seller').annotate(
        total=Count('firstName'))
    sellers = total_sellers.aggregate(sum=Sum('total'))['sum']
    total_joint = UserProfileInfo.objects.all().filter(client_type='Joint').annotate(
        total=Count('firstName'))
    joint = total_joint.aggregate(sum=Sum('total'))['sum']
    total_auction = Auction.objects.all().annotate(
        total=Count('auction_name'))
    auctions = total_auction.aggregate(sum=Sum('total'))['sum']
    tt = Item.objects.all().annotate(total=Count('item_lot'))
    items = tt.aggregate(sum=Sum('total'))['sum']
    return render(request, 'adminDashboardView.html', {'user_type':user_type,'item':item, 'total_items':total_items,'notification':notification,
                                                       'buyers':buyers,'sellers':sellers,'joint':joint,'auctions':auctions,'items':items})

#register draft user
def register(request):
    form = DraftUserInfoForm
    if request.method=="POST":
        draft_form = DraftUserInfoForm(request.POST)
        print(request.POST.get('password'))
        if draft_form.is_valid():
            df = draft_form.save(commit=False)
            df.password = make_password(request.POST.get('password'))
            df.save()
            # send_mail('Your registration request has been confirmed for Fotheby Auction House!',
            #           'Your Username is: ' + request.POST.get(
            #               'username') + ' and your password is: ' + request.POST.get('password')
            #           , 'sagunrupakheti@gmail.com', [getRequestInfo.email], fail_silently=False)
    return render(request,'register.html',{'form':form})

def viewRequest(request):
    getRequest = draftUser.objects.all().filter(status='Pending')
    notification = Notification.objects.all().filter(concerned_to='Admin')
    return render(request,'viewRequest.html',{'users':getRequest,'notification':notification})


def viewDraftDetails(request,userId):
    getRequestInfo = draftUser.objects.all().filter(id=userId)
    return render(request, 'viewDraftDetails.html', {'getRequestInfo':getRequestInfo})

def acceptUser(request,userId):
    getRequestInfo = draftUser.objects.get(id=userId)
    userModel = User()
    infoModel = UserProfileInfo()
    if request.method == "POST":
        try:
            userModel.username = request.POST.get('username')
            print(request.POST.get('password'))
            userModel.password = make_password(request.POST.get('password'))
            userModel.save()
            getUser = User.objects.all().filter(username=request.POST.get('username')).first()
            infoModel.user = getUser
            infoModel.firstName = getRequestInfo.firstName
            infoModel.lastName = getRequestInfo.lastName
            infoModel.email = getRequestInfo.email
            infoModel.dob = getRequestInfo.dob
            infoModel.country = getRequestInfo.country
            infoModel.city = getRequestInfo.city
            infoModel.zip_code = getRequestInfo.zip_code
            infoModel.address = getRequestInfo.address
            infoModel.country_code = getRequestInfo.country_code
            infoModel.contact = getRequestInfo.contact
            infoModel.bank_account_number = getRequestInfo.bank_account_number
            infoModel.bank_sort_code = getRequestInfo.bank_sort_code
            infoModel.client_type = getRequestInfo.client_type
            infoModel.save()
            draftUser.objects.all().filter(id=userId).update(status='Accepted')
            noti = Notification()
            noti.notification_text= 'A new '+getRequestInfo.client_type+ ' user has been added to the system!'
            noti.concerned_to= 'Admin'
            noti.save()
            send_mail('Your registration request has been confirmed for Fotheby Auction House!','Your Username is: ' + request.POST.get('username')+ ' and your password is: '+ request.POST.get('password')
                      ,'sagunrupakheti@gmail.com',[getRequestInfo.email],fail_silently=False)
            messages.success(request, 'User has been successfully confirmed! An email has been sent to the user to notify!')
            return redirect('viewRequest')
        except Exception:
            messages.error(request, 'Please enter a unique username!')
    return render(request,'acceptUser.html',{})

def declineUser(request,userId):
    draftUser.objects.all().filter(id=userId).update(status='Declined')
    getUser = draftUser.objects.get(id=userId)
    send_mail('Registration Declined Fotheby Auction House','Your registration request has been declined for Fotheby Auction House! Please contact the help desk for further explanation.',
               'sagunrupakheti@gmail.com', [getUser.email], fail_silently=False)
    messages.success(request, 'User has been successfully declined. An email has been sent to the user to notify!')
    return redirect('viewRequest')
    return render(request,'viewDraftDetails.html',{})

def showClients(request):
    userInfo = UserProfileInfo.objects.all().filter(client_type='Buyer') |UserProfileInfo.objects.all().filter(client_type='Seller')|UserProfileInfo.objects.all().filter(client_type='Joint')
    notification = Notification.objects.all().filter(concerned_to='Admin')
    return render(request,'showClients.html',{'userInfo':userInfo,'notification':notification})

def editUser(request,userId):
    user = User.objects.all().filter(username=userId).first()
    userInfo = UserProfileInfo.objects.all().filter(user=user).first()
    print(userInfo)
    getInfo = UserProfileInfo.objects.get(user=user)
    form = UserProfileInfoForm(instance=userInfo)
    if request.method == 'POST':
        user_form = UserProfileInfoForm(request.POST, instance=userInfo)
        if user_form.is_valid():
            user_form.save()
            if getInfo.client_type == 'Buyer':
                messages.success(request, 'Successfully edited the buyer information!')
                return redirect('showClients')
            elif  getInfo.client_type == 'Seller':
                messages.success(request, 'Successfully edited the seller information!')
                return redirect('showClients')
            elif getInfo.client_type == 'Joint':
                messages.success(request, 'Successfully edited the user information!')
                return redirect('showClients')
        else:
            messages.error(request, 'Please enter valid data!')
            # return redirect('editUser/'+userId)
    return render(request,'editUser.html',{'form':form})

def deleteUser(request,userId):
    users = User.objects.all().filter(username=userId).first()
    print(users)
    userInfo = UserProfileInfo.objects.all().filter(user=users)
    getInfo = UserProfileInfo.objects.get(user=users)
    print(userInfo)
    userInfo.delete()
    users.delete()
    if getInfo.client_type == 'Buyer':
        messages.success(request, 'Buyer has been successfully deleted!')
        return redirect('showBuyers')
    elif  getInfo.client_type == 'Seller':
        messages.success(request, 'Seller has been successfully deleted!')
        return redirect('showSellers')
    elif getInfo.client_type == 'Joint':
        messages.success(request, 'User has been successfully deleted!')
        return redirect('showJoint')

def addCategory(request):
    form = CategoryForm
    categoryInfo = Category.objects.all()
    if request.method == "POST":
        category_form = CategoryForm(data=request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category has been successfully added!')
        else:
            messages.error(request, 'Please enter a unique category!')
    notification = Notification.objects.all().filter(concerned_to='Admin')
    return render(request, 'addCategory.html', {'form': form, 'categoryInfo':categoryInfo,'notification':notification})

def editCategory(request,category_name):
    category_info = Category.objects.all().filter(category_name=category_name).first()
    form = CategoryForm(instance=category_info)
    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category_info)
        if category_form.is_valid():
            try:
                category_form.save()
                messages.success(request, 'Category has been successfully edited!')
                return redirect('../addCategory')
            except Exception:
                messages.error(request, 'Please enter a unique category!')
                return redirect('../addCategory')
    return render(request, 'editCategory.html', {'form': form})


def deleteCategory(request,category_name):
    category_info = Category.objects.all().filter(category_name=category_name).first()
    try:
        category_info.delete()
        messages.success(request, 'Category has been successfully deleted!')
        return redirect('../addCategory')
    except Exception:
        messages.error(request, 'Cannot not delete category!')
        return redirect('../addCategory')

def addUserAdmin(request):
    form = AddAdminUserForm
    detailsForm = UserForm
    notification = Notification.objects.all().filter(concerned_to='Admin')
    if request.method == "POST":
        details_form = UserForm(data=request.POST)
        user_form = AddAdminUserForm(data=request.POST)
        try:
            username_pass= details_form.save(commit=False)
            username_pass.password = make_password(username_pass.password)
            username_pass.save()
            details = user_form.save(commit=False)
            details.user =username_pass
            details.save()
            messages.success(request, 'User Successfully added!')
            return redirect('../viewStaff')
        except Exception:
            messages.error(request, 'Please enter valid information!')
    return render(request,'addUserAdmin.html', {'form':form,'detailsForm':detailsForm,'notification':notification})


def deleteAuction(request,auction_id):
    auction_info = Auction.objects.all().filter(auction_id=auction_id).first()
    try:
        auction_info.delete()
        messages.success(request, 'Auction has been successfully deleted!')
        return redirect('../addAuction')
    except Exception:
        messages.error(request, 'Cannot delete auction!')
        return redirect('../addAuction')


def editAuction(request,auction_id):
    auction_info = Auction.objects.all().filter(auction_id=auction_id).first()
    form = AuctionFormStatus(instance=auction_info)
    if request.method == "POST":
        auction_form = AuctionFormStatus(request.POST, instance=auction_info)
        if auction_form.is_valid():
            try:
                auction_form.save()
                getStatus = Auction.objects.get(auction_id=auction_id)
                print(getStatus.auction_status)
                if getStatus.auction_status == "Expired":
                    items = Item.objects.all().filter(auction=auction_info)
                    for i in items:
                        bid = Bidding.objects.all().filter(item=i)
                        for b in bid:
                            if b.current_bid > b.estimated_price:
                                name = 'item_lot'
                                Item.objects.all().filter(item_lot=getattr(b.item, name)).update(status='Processing')
                                commission = Commission()
                                commission.item = b
                                commission.user = b.bidding_by
                                commission.item_info = b.item
                                commission.sold_price = b.current_bid
                                commission.commission_amount = (0.15* int(b.current_bid))+int(b.current_bid)
                                commission.payment_status= 'Pending'
                                commission.save()
                                # Commission.objects.update_or_create(item=b, item_info= b.item,
                                #                                       defaults={'sold_price': b.current_bid,'commission_amount': (0.15* int(b.current_bid))+int(b.current_bid),
                                #                                     'payment_status': 'Pending',})
                                messages.success(request, 'Auction has been successfully edited!')
                                return redirect('../addAuction')
                            elif b.current_bid == b.estimated_price:
                                name = 'item_lot'
                                Item.objects.all().filter(item_lot=getattr(b.item, name)).update(status='Not Sold')
                                messages.success(request, 'Auction has been successfully edited!')
                                return redirect('../addAuction')

                elif getStatus.auction_status == "Live":
                    noti = Notification()
                    noti.notification_text= 'Hurry up! The auction: '+ getStatus.auction_name + ' is live now! Place a bid on your favorite items' \
                                                                                                'to get a deal!'
                    noti.concerned_to= 'Buyer'
                    noti.save()
                elif getStatus.auction_status == "Advanced Bidding":
                    noti = Notification()
                    noti.notification_text= 'Hurry up! The auction: '+ getStatus.auction_name + ' is open for advanced bidding! Place a bid on your favorite items' \
                                                                                                'to get a deal!'
                    noti.concerned_to= 'Buyer'
                    noti.save()
                messages.success(request, 'Auction has been successfully edited!')

                return redirect('../addAuction')
            except Exception:
                messages.error(request, 'Please enter a valid auction date!')
                return redirect('../addAuction')
    return render(request, 'editAuction.html', {'form': form})


def viewStaff(request):
    userInfo = UserProfileInfo.objects.all().filter(client_type='Admin') | UserProfileInfo.objects.all().filter(client_type='Evaluator')
    notification=Notification.objects.all().filter(concerned_to='Admin')
    return render(request,'staff.html',{'userInfo':userInfo,'notification':notification})


def addAuction(request):
    form = AuctionForm
    auctionInfo = Auction.objects.all()
    if request.method == "POST":
        addInForm = AuctionForm(data=request.POST)
        try:
            addInForm.save()
            noti= Notification()
            noti.notification_text= 'A new auction: '+request.POST.get('auction_name') +' has been added to the system. You can request for items ' \
                                                                                       'for this auction!'
            noti.concerned_to= 'Seller'
            noti.save()
            messages.success(request, 'Auction Successfully added!')
            return redirect('../addAuction')
        except Exception :
            messages.error(request, 'Please add a future auction date!')
    notification = Notification.objects.all().filter(concerned_to='Admin')
    return render(request,'addAuction.html',{'form':form,'auctionInfo':auctionInfo,'notification':notification})

def buyerDashboard(request):
    return render(request, 'buyerDashboard.html', {})

def checkTime():
    print('asd')

schedule.every(10).seconds.do(checkTime)

def buyerDashboardView(request):
    items = ''
    auctions = Auction.objects.all()
    end_date=''
    status = ''
    category = Category.objects.all()

    ac = Auction.objects.all().filter(auction_status= 'Advanced Bidding') | Auction.objects.all().filter(auction_status= 'Live')
    items=''
    if request.method == "POST":
        query_dictionary = {
            'artist_name': request.POST.get('artist_name'),
            'category__category_name': request.POST.get('category'),
            # 'auction__auction_date': request.POST.get('auction_date'),
            'classification': request.POST.get('classification'),
            'estimated_price': request.POST.get('estimated_price'),
        }
        not_none_parameters = {single_query: query_dictionary.get(single_query) for single_query in query_dictionary if
                               query_dictionary.get(single_query) is not None}
        filter_list = Q()
        for item in not_none_parameters:
            filter_list |= Q(**{item: not_none_parameters.get(item)})
        items = Item.objects.filter(filter_list, status='Accepted', auction__auction_status = 'Live')|Item.objects.filter(filter_list, status='Accepted', auction__auction_status = 'Advanced Bidding')
        print(query_dictionary)
    else:
        for a in auctions:
            if a.auction_status == 'Advanced Bidding' or  a.auction_status == 'Live':
                if a.auction_status == 'Advanced Bidding':
                    end_date = a.auction_date
                    status = 'Advanced'
                elif a.auction_status == 'Live':
                    status = 'Live'
                getAuction = Auction.objects.all().filter(auction_id= a.auction_id).first()
                items= Item.objects.all().filter(status='Accepted', auction__auction_status = 'Live').annotate(total=Count('auction')).order_by('estimated_price')|Item.objects.all().filter(status='Accepted',auction__auction_status = 'Advanced Bidding').annotate(total=Count('auction')).order_by('estimated_price')
    return render(request, 'buyerDashboardView.html', {'items':items,'status':status,'end_date':end_date, 'ac':ac,'category':category})

def sellerDashboard(request):
    noti = Notification.objects.all().filter(concerned_to='Seller')|Notification.objects.all().filter(concerned_to=request.user)
    return render(request, 'sellerDashboard.html', {'notification':noti})

def jointDashboard(request):
    noti = Notification.objects.all().filter(concerned_to='Buyer')|Notification.objects.all().filter(concerned_to='Seller')| Notification.objects.all().filter(concerned_to=request.user)
    return render(request, 'jointDashboard.html', {'notification':noti})

def evaluatorDashboard(request):
    noti = Notification.objects.all().filter(concerned_to='Evaluator')|Notification.objects.all().filter(concerned_to=request.user)
    return render(request, 'evaluatorDashboard.html', {'notification':noti})

# def login(request):
#     form = UserForm
#     return render(request, 'login.html', {'form':form})

def user_login(request):
    global getReq
    if request.method == 'POST':
        # username in login view
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.all().filter(username=username)
        profile = UserProfileInfo.objects.filter(user__in=users).values('client_type').first()
        getFinal = ''
        if (profile != None):
            getFinal = profile.get('client_type')
        # for authentication
        user = authenticate(username=username, password=password)
        # if the user if a teacher
        if user and getFinal == 'Admin':
            login(request, user)
            return HttpResponseRedirect('landingPage')
        # if the user is a student
        elif user and getFinal == 'Evaluator':
            login(request, user)
            return HttpResponseRedirect('landingPage')
        elif user and getFinal == 'Buyer':
            login(request, user)
            return HttpResponseRedirect('landingPage')
        elif user and getFinal == 'Seller':
            login(request, user)
            return HttpResponseRedirect('landingPage')
        elif user and getFinal == 'Joint':
            login(request, user)
            return HttpResponseRedirect('landingPage')
        else:
            messages.error(request, 'Please enter correct credentials!')
    return render(request, 'login.html', {})

def requestItem(request):
    user = User.objects.all().filter(username=request.user).first()
    temp=''
    getUser = UserProfileInfo.objects.get(user=user)
    if getUser.client_type == "Seller":
        temp='sellerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller').order_by('-notification_date')|Notification.objects.all().filter(concerned_to=request.user).order_by('-notification_date')
    elif getUser.client_type == "Joint":
        temp = 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Buyer').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to=request.user).order_by(
            '-notification_date')

    form = ItemForm
    items = Item
    if request.method == "POST":
        item_form = ItemForm(request.POST)
        # Item.user = request.user
        item = item_form.save(commit=False)
        item.user = request.user
        if request.FILES:
            if 'image1' in request.FILES:
                print('there is image')
                item.image1  = request.FILES['image1']
            if 'image2' in request.FILES:
                item.image2  = request.FILES['image2']
            if 'image3' in request.FILES:
                item.image3  = request.FILES['image3']
            item.save()
        #check all the categories
        if request.POST.get('category') == "Drawings":
            getItem = Item.objects.latest('item_lot')
            itemLot = getItem.item_lot
            return redirect('requestItemInfoDrawing/'+str(itemLot))
        elif request.POST.get('category') == "Paintings":
            getItem = Item.objects.latest('item_lot')
            itemLot = getItem.item_lot
            return redirect('requestItemInfoPainting/'+str(itemLot))
        elif request.POST.get('category') == "Photographic Images":
            getItem = Item.objects.latest('item_lot')
            itemLot = getItem.item_lot
            return redirect('requestItemInfoPhotographicImage/'+str(itemLot))
        elif request.POST.get('category') == "Sculptures":
            getItem = Item.objects.latest('item_lot')
            itemLot = getItem.item_lot
            return redirect('requestItemInfoSculpture/'+str(itemLot))
        elif request.POST.get('category') == "Carvings":
            getItem = Item.objects.latest('item_lot')
            itemLot = getItem.item_lot
            return redirect('requestItemInfoCarving/'+str(itemLot))
    return render(request, 'requestItem.html', {'form':form,'temp':temp,'notification':notification})


def editItem(request,item):
    user = User.objects.all().filter(username=request.user).first()
    temp=''
    getUser = UserProfileInfo.objects.get(user=user)
    if getUser.client_type == "Seller":
        temp='sellerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller').order_by('-notification_date')|Notification.objects.all().filter(concerned_to=request.user).order_by('-notification_date')
    elif getUser.client_type == "Joint":
        temp = 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Buyer').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to=request.user).order_by(
            '-notification_date')
    u = Item.objects.all().filter(item_lot=item).first()
    form = ItemForm(instance=u)
    if request.method=='POST':
        try:
            editForm = ItemForm(request.POST, instance=u)
            editForm.save()
            messages.success(request,'Item successfully edited!')
            return redirect('../../../myItems')
        except:
            messages.error(request, 'Cannot edit the item!')
    return render(request,'requestItem.html',{'form':form,'temp':temp,'notification':notification})


def requestItemInfoDrawing(request,item):
    form = DrawingForm
    getItem = Item.objects.all().filter(item_lot= item).first()
    if request.method == "POST":
        item_form = DrawingForm(request.POST)
        drawings = item_form.save(commit=False)
        drawings.drawing = getItem
        drawings.save()
        #notification
        noti = Notification()
        noti.notification_text= 'A new drawing item has been requested for evaluation!'
        noti.concerned_to= 'Evaluator'
        noti.save()
        #save user info
        messages.success(request, 'Request for the item has been sent!')
        return redirect('../requestItem')
    return render(request,'requestItemInfo.html',{'form':form})

def requestItemInfoPainting(request,item):
    form = PaintingForm
    getItem = Item.objects.all().filter(item_lot=item).first()
    if request.method == "POST":
        item_form = PaintingForm(request.POST)
        paintings = item_form.save(commit=False)
        paintings.painting = getItem
        paintings.save()
        #notification
        noti = Notification()
        noti.notification_text= 'A new painting item has been requested for evaluation!'
        noti.concerned_to= 'Evaluator'
        noti.save()
        messages.success(request, 'Request for the painting has been sent!')
        return redirect('../requestItem')
    return render(request,'requestItemInfo.html',{'form':form})

def requestItemInfoPhotographicImage(request,item):
    form = PhotographicImageForm
    getItem = Item.objects.all().filter(item_lot=item).first()
    if request.method == "POST":
        item_form = PhotographicImageForm(request.POST)
        photo = item_form.save(commit=False)
        photo.photographic_image = getItem
        photo.save()
        #notification
        noti = Notification()
        noti.notification_text= 'A new painting photographic image item has been requested for evaluation!'
        noti.concerned_to= 'Evaluator'
        noti.save()
        messages.success(request, 'Request for the Photographic Image has been sent!')
        return redirect('../requestItem')
    return render(request,'requestItemInfo.html',{'form':form})

def requestItemInfoSculpture(request,item):
    form = SculptureForm
    getItem = Item.objects.all().filter(item_lot=item).first()
    if request.method == "POST":
        item_form = SculptureForm(request.POST)
        sculptures = item_form.save(commit=False)
        sculptures.sculpture = getItem
        sculptures.save()
        #notification
        noti = Notification()
        noti.notification_text= 'A new sculpture item has been requested for evaluation!'
        noti.concerned_to= 'Evaluator'
        noti.save()
        messages.success(request, 'Request for the Sculpture has been sent!')
        return redirect('../requestItem')
    return render(request,'requestItemInfo.html',{'form':form})

def requestItemInfoCarving(request,item):
    form = CarvingForm
    getItem = Item.objects.all().filter(item_lot=item).first()
    if request.method == "POST":
        item_form = CarvingForm(request.POST)
        carvings = item_form.save(commit=False)
        carvings.carving = getItem
        carvings.save()
        #notification
        noti = Notification()
        noti.notification_text= 'A new carving item has been requested for evaluation!'
        noti.concerned_to= 'Evaluator'
        noti.save()
        messages.success(request, 'Request for the Carving has been sent!')
        return redirect('../requestItem')
    return render(request,'requestItemInfo.html',{'form':form})

def myItems(request):
    user = User.objects.all().filter(username=request.user).first()
    temp=''
    getUser = UserProfileInfo.objects.get(user=user)
    if getUser.client_type == "Seller":
        temp = 'sellerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to=request.user).order_by(
            '-notification_date')
    elif getUser.client_type == "Joint":
        temp = 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Buyer').order_by(
            '-notification_date')| Notification.objects.all().filter(concerned_to=request.user).order_by(
            '-notification_date')

    itemInfo = Item.objects.all().filter(user=request.user)
    return render(request, 'myItems.html', {'itemInfo':itemInfo,'temp':temp,'notification':notification})

def verifyItems(request):
    itemInfo = Item.objects.all().filter(status='Pending')
    return render(request, 'verifyItems.html', {'itemInfo':itemInfo})

def acceptedItems(request):
    itemInfo = Item.objects.all().filter(status='Accepted')
    return render(request, 'acceptedItems.html', {'itemInfo':itemInfo})

def int_or_0(value):
    try:
        return int(value)
    except:
        return 0



def viewItemDetails(request,item):
    item_val = item
    user_info = User.objects.all().filter(username=request.user).first()
    if request.user.is_authenticated:
        getUser = UserProfileInfo.objects.get(user=user_info)
        notification = ''
        if getUser.client_type == "Buyer":
            temp = 'buyerDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
                concerned_to=request.user)
        elif getUser.client_type == "Seller":
            temp = 'sellerDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Seller') | Notification.objects.all().filter(
                concerned_to=request.user)
        elif getUser.client_type == "Joint":
            temp = 'jointDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
                concerned_to='Seller') | Notification.objects.all().filter(
                concerned_to='Joint') | Notification.objects.all().filter(concerned_to=request.user)
        elif getUser.client_type == "Admin":
            temp = 'adminDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Admin').order_by('-notification_date')
        elif getUser.client_type == "Evaluator":
            temp = 'evaluatorDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Evaluator')
    else:
        temp = 'normalDashboard.html'
        notification = ''
    auction = Auction.objects.all()
    itemInfo = Item.objects.all().filter(item_lot=item)
    getItem = Item.objects.all().filter(item_lot=item).first()
    it = Item.objects.all().filter(item_lot=item).first()
    checkItem = Item.objects.get(item_lot=item)
    bid=''
    status = checkItem.status
    st=''
    end_date=''
    getAuction = Auction.objects.all().filter(auction_name= checkItem.auction).first()
    if getAuction.auction_status == 'Advanced Bidding' or getAuction.auction_status == 'Pending':
        end_date = getAuction.auction_date
        st = 'Advanced'
    elif getAuction.auction_status == 'Live':
        end_date = getAuction.auction_date
        st = 'Advanced'
    if checkItem.status == "Accepted":
        bid = Bidding.objects.all().filter(item=it)
    val = ''
    ex=''
    if str(getItem.category) == "Drawings":
        extra_info= Drawing.objects.all().filter(drawing=getItem)
        ex = zip(itemInfo,extra_info)
        val='D'
    elif str(getItem.category) == "Paintings":
        extra_info = Painting.objects.all().filter(painting=getItem)
        ex = zip(itemInfo, extra_info)
        val = 'P'
    elif str(getItem.category) == "Photographic Images":
        extra_info = PhotographicImage.objects.all().filter(photographic_image=getItem)
        ex = zip(itemInfo, extra_info)
        val = 'PI'
    elif str(getItem.category) == "Sculptures":
        extra_info = Sculpture.objects.all().filter(sculpture=getItem)
        ex = zip(itemInfo, extra_info)
        val = 'S'
    elif str(getItem.category) == "Carvings":
        extra_info = Carving.objects.all().filter(carving=getItem)
        ex = zip(itemInfo, extra_info)
        val = 'C'
    print(val)
    if checkItem.status == "Accepted":
        getBid = Bidding.objects.all().filter(item=it).first()
    #place bidding
    if request.method == "POST":
        if 'placeBid' in request.POST:
            getCurrentBid = getBid.current_bid
            getAddedBid = request.POST.get('bidAmount')
            if int_or_0(getAddedBid)<getCurrentBid or int_or_0(getAddedBid)==getCurrentBid:
                messages.error(request,'Please add a greater bid amount!')
            else:
                Bidding.objects.all().filter(item=it).update(current_bid=getAddedBid,old_bid= getCurrentBid, bidding_by= request.user)
                #store for graphical representation
                storeBid = StoreBidding.objects.update_or_create(item= getItem, bidding_by=request.user, defaults={'old_bid':getCurrentBid,'current_bid':getAddedBid })
                # add notification
                noti = Notification()
                noti.notification_text = 'Buyer by the username '+ str(request.user) + ' has placed a bid of £'+ getAddedBid+ ' for your item '+ getItem.item_name
                noti.concerned_to = getItem.user
                a= noti.save()
                messages.success(request, 'Successfully placed a bid! Please monitor the auction for further bids!')
        elif 'auctionLive' in request.POST:
            try:
                itemInfo = Item.objects.all().filter(item_lot=item)
                it = Item.objects.all().filter(item_lot=item).first()
                items = Item.objects.get(item_lot=item)
                print(str(request.POST.get('selectedAuction')),'**************')
                auc = Auction.objects.get(auction_id=request.POST.get('selectedAuction'))
                user = User.objects.all().filter(username=request.user).first()
                Item.objects.all().filter(item_lot=item).update(auction=auc,status='Accepted',evaluation_text=request.POST.get('evaluationText'))
                noti = Notification()
                noti.notification_text = 'Your item ' + items.item_name + ' has been accepted for an auction which is scheduled to be held on ' + str(
                    auc.auction_date) + ' !'
                noti.concerned_to = items.user
                noti.save()
                bid = Bidding()
                bid.item = it
                bid.estimated_price = items.estimated_price
                bid.current_bid = items.estimated_price
                bid.old_bid = items.estimated_price
                bid.bidding_by = user
                bid.save()
                messages.success(request, 'Item has been successfully accepted!')
            except:
                messages.error(request, 'Please fill in information correctly!')
    return render(request, 'viewItemDetails.html', {'itemInfo':itemInfo,'ex':ex,'val':val,'temp':temp,'bid':bid,'status':status,
                                                    'st':st,'end_date':end_date,'item':item,'auction':auction})

def sendBid(request,item_val):
    it = Item.objects.all().filter(item_lot=item_val).first()
    getBid = Bidding.objects.all().filter(item=it).first()
    getCurrentBid = getBid.current_bid
    return JsonResponse({'currBid':getCurrentBid})

def acceptItem(request,item):
    itemInfo = Item.objects.all().filter(item_lot=item)
    it = Item.objects.all().filter(item_lot=item).first()
    items = Item.objects.get(item_lot=item)
    auction = Auction.objects.get(auction_name= request.POST.get('selectedAuction'))
    user = User.objects.all().filter(username=request.user).first()
    Item.objects.all().filter(item_lot=item).update(status='Accepted')
    noti = Notification()
    noti.notification_text = 'Your item '+items.item_name +' has been accepted for an auction which is scheduled to be held on '+ str(auction.auction_date) + ' !'
    noti.concerned_to = items.user
    noti.save()
    bid = Bidding()
    bid.item = it
    bid.estimated_price= items.estimated_price
    bid.current_bid = items.estimated_price
    bid.old_bid = items.estimated_price
    bid.bidding_by= user
    bid.save()
    messages.success(request, 'Item has been successfully accepted!')
    return render(request, 'verifyItems.html', {'itemInfo':itemInfo})

def declineItem(request,item):
    itemInfo = Item.objects.all().filter(item_lot=item)
    Item.objects.all().filter(item_lot=item).update(status='Declined')
    messages.success(request, 'Item has been successfully declined!')
    return render(request, 'verifyItems.html', {'itemInfo':itemInfo})

def viewAuctionItems(request,auction_id):
    auction_info = Auction.objects.all().filter(auction_id=auction_id).first()
    itemInfo = Item.objects.all().filter(auction=auction_info,status='Accepted')
    return render(request, 'viewAuctionItems.html', {'itemInfo': itemInfo})

def wonItems(request):
    user = User.objects.all().filter(username=request.user).first()
    temp=''
    getUser = UserProfileInfo.objects.get(user=user)
    notification = ''
    if getUser.client_type == "Buyer":
        temp = 'buyerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer').order_by('-notification_date')
    elif getUser.client_type == "Joint":
        temp = 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date')
    won = Commission.objects.all().filter(user=request.user)
    ex = ''
    c= Commission.objects.all().filter(user=request.user).first()
    if Commission.objects.all().filter(user=request.user).first():
        commission = Commission.objects.get(user=request.user)
        name = 'item_lot'
        # item_info = Item.objects.all().filter(item_lot=getattr(commission.item_info, name)).update(status='Processing')
        info = Item.objects.all().filter(item_lot=getattr(commission.item_info, name))
        # print(item_info)
        ex = zip(info, won)
    return render(request, 'wonItems.html', {'won': won,'ex':ex,'temp':temp,'notification':notification})

def clearPayment(request,item_lot):
    item_info = Item.objects.all().filter(item_lot=item_lot)
    ii = Item.objects.all().filter(item_lot=item_lot).first()
    commission_info = Commission.objects.all().filter(item_info=ii)
    ex = zip(item_info, commission_info)
    return render(request,'clearPayment.html',{'ex':ex})

def markSold(request):
    body = json.loads(request.body)
    i = Item.objects.all().filter(item_lot=body['item_id'])
    print('yooooo',i)
    getItem = Item.objects.all().filter(item_lot=body['item_id']).update(status='Sold')
    print(getItem)
    item = Item.objects.all().filter(item_lot=body['item_id']).first()
    getCom = Commission.objects.all().filter(item_info=item).update(payment_status='Cleared')
    com = Commission.objects.all().filter(item_info=item)
    # print(com)
    print('BODY:',body)
    return JsonResponse('Payment Done',safe=False)

def myPurchases(request):
    user = User.objects.all().filter(username=request.user).first()
    temp=''
    getUser = UserProfileInfo.objects.get(user=user)
    notification = ''
    if getUser.client_type == "Buyer":
        temp = 'buyerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer').order_by('-notification_date')
    elif getUser.client_type == "Joint":
        temp = 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer').order_by(
            '-notification_date') | Notification.objects.all().filter(concerned_to='Seller').order_by(
            '-notification_date')

    ex = ''
    won=''
    if Commission.objects.all().filter(user=request.user):
        won = Commission.objects.all().filter(user=request.user,payment_status="Cleared")
        if Commission.objects.get(user=request.user):
            commission = Commission.objects.get(user=request.user)
            name = 'item_lot'
            item_info = Item.objects.all().filter(item_lot=getattr(commission.item_info, name))
            ex = zip(item_info, won)
            print(item_info)
    return render(request, 'myPurchases.html', {'won': won,'ex':ex,'temp':temp,'notification':notification})


def loginPage(request):
    return render(request,'loginPage.html',{})

def viewSales(request):
    auctionInfo = Auction.objects.all().filter(auction_status='Expired')
    notification = Notification.objects.all().filter(concerned_to='Admin')
    return render(request,'viewSales.html',{'auctionInfo':auctionInfo,'notification':notification})

def viewSoldItems(request,auction_id):
    auctionInfo = Auction.objects.all().filter(auction_id=auction_id).first()
    item = Item.objects.all().filter(auction= auctionInfo, status ='Sold')
    heading = 'Sold Items'
    return render(request, 'viewAuctionItemExpire.html', {'itemInfo': item, 'heading':heading})

def viewPendingItems(request,auction_id):
    auctionInfo = Auction.objects.all().filter(auction_id=auction_id).first()
    item = Item.objects.all().filter(auction= auctionInfo, status = 'Accepted')
    heading = 'No Bid Items (Pending)'
    return render(request, 'viewAuctionItemExpire.html', {'itemInfo': item, 'heading': heading})

def viewHoldItems(request,auction_id):
    auctionInfo = Auction.objects.all().filter(auction_id=auction_id).first()
    item = Item.objects.all().filter(auction= auctionInfo, status = 'Processing')
    heading = 'Not Paid Items (On Hold)'
    return render(request, 'viewAuctionItemExpire.html', {'itemInfo': item, 'heading': heading})

def browseAuctions(request):
    auction = Auction.objects.all().filter(auction_status='Live') | Auction.objects.all().filter(auction_status='Advanced Bidding')
    user = User.objects.all().filter(username=request.user).first()
    temp=''
    getUser = UserProfileInfo.objects.get(user=user)
    notification=''
    if getUser.client_type == "Buyer":
        temp= 'buyerDashboard.html'
        notification= Notification.objects.all().filter(concerned_to='Buyer').order_by('-notification_date')
    elif getUser.client_type == "Joint":
        temp= 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer').order_by('-notification_date') | Notification.objects.all().filter(concerned_to='Seller').order_by('-notification_date')
    return  render(request,'browseAuctions.html',{'auction':auction,'temp':temp,'notification':notification})

def showAuctionItemsBuyer(request,auction_id):
    auction = Auction.objects.all().filter(auction_id=auction_id).first()
    name = auction.auction_name
    description = auction.auction_description
    items = Item.objects.all().filter(auction=auction, status='Accepted')|Item.objects.all().filter(auction=auction, status='Sold')
    st=''
    end_date=''
    if auction.auction_status == 'Advanced Bidding':
        end_date = auction.auction_date
        st = 'Advanced'
    elif auction.auction_status == 'Live':
        st = 'Advanced'
    return render(request, 'showAuctionItemsBuyer.html', {'items': items,'name':name,'description':description,'st':st,'end_date':end_date})

def myProfile(request):
    user = User.objects.all().filter(username=request.user).first()
    userInfo = UserProfileInfo.objects.all().filter(user=user)
    temp=''
    profileEdit = UserProfileInfo.objects.all().filter(user=user).first()
    form = ProfilePicForm
    getUser = UserProfileInfo.objects.get(user=user)
    notification=''
    if getUser.client_type == "Buyer":
        temp= 'buyerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(concerned_to=request.user)
    elif getUser.client_type == "Seller":
        temp= 'sellerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller') | Notification.objects.all().filter(concerned_to=request.user)
    elif getUser.client_type == "Joint":
        temp= 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(concerned_to='Seller') | Notification.objects.all().filter(concerned_to='Joint') | Notification.objects.all().filter(concerned_to=request.user)
    elif getUser.client_type == "Admin":
        temp= 'adminDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Admin').order_by('-notification_date')
    elif getUser.client_type == "Evaluator":
        temp= 'evaluatorDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Evaluator')
    if request.method == "POST":
        if request.FILES:
            getPic = ProfilePicForm(request.POST,request.FILES, instance=profileEdit)
            print(request.FILES)
            if getPic.is_valid():
                try:
                    getPic.save()
                    messages.success(request, 'Successfully edited your profile information!')
                    return redirect('myProfile')
                except:
                    print('Error')
        else:
            print('no files')
    return render(request,'myProfile.html',{'temp':temp,'userInfo':userInfo,'form':form,'notification':notification})


def allNotifications(request):
    user = User.objects.all().filter(username=request.user).first()
    getUser = UserProfileInfo.objects.get(user=user)
    notification = ''
    if getUser.client_type == "Buyer":
        temp = 'buyerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
            concerned_to=request.user)
    elif getUser.client_type == "Seller":
        temp = 'sellerDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Seller') | Notification.objects.all().filter(
            concerned_to=request.user)
    elif getUser.client_type == "Joint":
        temp = 'jointDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
            concerned_to='Seller') | Notification.objects.all().filter(
            concerned_to='Joint') | Notification.objects.all().filter(concerned_to=request.user)
    elif getUser.client_type == "Admin":
        temp = 'adminDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Admin').order_by('-notification_date')
    elif getUser.client_type == "Evaluator":
        temp = 'evaluatorDashboard.html'
        notification = Notification.objects.all().filter(concerned_to='Evaluator')
    return render(request, 'viewAllNotification.html',
                  {'temp': temp, 'notification': notification})

def editProfile(request):
    user = User.objects.all().filter(username=request.user).first()
    userInfo = UserProfileInfo.objects.all().filter(user=user)
    temp=''
    u = UserProfileInfo.objects.all().filter(user=user).first()
    form = EditProfileForm(instance=u)
    getUser = UserProfileInfo.objects.get(user=user)
    if getUser.client_type == "Buyer":
        temp= 'buyerDashboard.html'
    elif getUser.client_type == "Seller":
        temp= 'sellerDashboard.html'
    elif getUser.client_type == "Joint":
        temp= 'jointDashboard.html'
    elif getUser.client_type == "Admin":
        temp= 'adminDashboard.html'
    elif getUser.client_type == "Evaluator":
        temp= 'evaluatorDashboard.html'

    if request.method == "POST":
        editForm =  EditProfileForm(request.POST, instance=u)
        if editForm.is_valid():
            editForm.save()
            messages.success(request,'Successfully edited your profile information!')
            return redirect('myProfile')
    return render(request,'editProfile.html',{'temp':temp,'userInfo':userInfo,'form':form})

def jointRequest(request):
    req = jointAccountRequest()
    user = User.objects.all().filter(username=request.user).first()
    req.user= user
    try:
        req.save()
        messages.success(request, 'Successfully sent your joint account request!')
        return redirect('editProfile')
    except Exception:
        messages.error(request, 'Please try again later!')
        return redirect('editProfile')

def viewJoint(request):
    getReq = jointAccountRequest.objects.all()
    userInfo=''
    for r in getReq:
        userInfo = UserProfileInfo.objects.all().filter(user=r.user)

    return render(request, 'viewJoint.html', {'userInfo':userInfo})

def acceptJointRequest(request,userId):
    user = User.objects.all().filter(username=userId).first()
    UserProfileInfo.objects.all().filter(user=user).update(client_type='Joint')
    getUser = UserProfileInfo.objects.get(user=user)
    send_mail('Request accepted for joint account in Fotheby Auction House!','Your request for a buyer/seller account has been accepted! Please enjoy your new features!', 'sagunrupakheti@gmail.com', [getUser.email], fail_silently = False)
    messages.success(request, 'A new buyer/seller account added!')
    return redirect('viewJoint')


def declineJointRequest(request,userId):
    user = User.objects.all().filter(username=userId).first()
    getUser = UserProfileInfo.objects.get(user=user)
    deleteReq = jointAccountRequest.objects.all().filter(user=user)
    deleteReq.delete()
    send_mail('Request declined for joint account in Fotheby Auction House!','Your request for a buyer/seller account has been declined! Sorry for the inconvenience!', 'sagunrupakheti@gmail.com', [getUser.email], fail_silently = False)
    messages.success(request, 'Successfully Declined')
    return redirect('viewJoint')

def auctionReport(request,auction_id):
    auction = Auction.objects.all().filter(auction_id=auction_id).first()
    auction_sales = Item.objects.all().filter(auction=auction,status='Sold').values('item_lot').annotate(
        total=Count('item_lot'))
    approved_items = Item.objects.all().filter(auction=auction,status='Approved').values('item_lot').annotate(
        total=Count('item_lot'))
    pending_payment = Item.objects.all().filter(auction=auction,status='Processing').values('item_lot').annotate(
        total=Count('item_lot'))
    itm = Item.objects.all().filter(auction=auction).values('item_lot').annotate(total=Count('item_lot'))
    all_items= itm.aggregate(sum=Sum('total'))['sum']
    commission = Commission.objects.all().filter(item_info__auction = auction)
    final_sale_amount = commission.aggregate(sum=Sum('commission_amount'))['sum']
    final_commission_amount = final_sale_amount*15/100
    total_bids = Commission.objects.all().filter(item_info__auction = auction).values('item_info').annotate(
        total=Count('item_info'))
    notification = Notification.objects.all().filter(concerned_to='Admin')
    return render(request,'auctionReport.html',{'auction_sales':auction_sales,'approved_items':approved_items,'pending_payment':pending_payment,
                                                'all_items':all_items,'final_sale_amount':final_sale_amount,'final_commission_amount':final_commission_amount,'commission':commission,
                                                'total_bids':total_bids,'notification':notification})

def categoryItems(request,category_name):
    category = Category.objects.all().filter(category_name=category_name).first()
    name = category.category_name
    items = Item.objects.all().filter(category=category,status='Accepted')
    print(items)
    user = User.objects.all().filter(username=request.user).first()
    if request.user.is_authenticated:
        getUser = UserProfileInfo.objects.get(user=user)
        notification = ''
        if getUser.client_type == "Buyer":
            temp = 'buyerDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
                concerned_to=request.user)
        elif getUser.client_type == "Seller":
            temp = 'sellerDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Seller') | Notification.objects.all().filter(
                concerned_to=request.user)
        elif getUser.client_type == "Joint":
            temp = 'jointDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Buyer') | Notification.objects.all().filter(
                concerned_to='Seller') | Notification.objects.all().filter(
                concerned_to='Joint') | Notification.objects.all().filter(concerned_to=request.user)
        elif getUser.client_type == "Admin":
            temp = 'adminDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Admin').order_by('-notification_date')
        elif getUser.client_type == "Evaluator":
            temp = 'evaluatorDashboard.html'
            notification = Notification.objects.all().filter(concerned_to='Evaluator')
    else:
        temp = 'normalDashboard.html'
        notification = ''
    return render(request,'categoryItems.html',{'items':items,'temp':temp,'name':name})