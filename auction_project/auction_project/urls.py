"""auction_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from auction_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auction_app/',include('auction_app.urls')),
    path('', views.index, name='index'),
    path('adminDashboard', views.adminDashboard, name='adminDashboard'),
    path('adminDashboardView', views.adminDashboardView, name='adminDashboardView'),
    path('register', views.register, name='register'),
    path('viewRequest', views.viewRequest, name='viewRequest'),
    path('viewDraftDetails/<userId>', views.viewDraftDetails, name='viewDraftDetails'),
    path('acceptUser/<userId>', views.acceptUser, name='acceptUser'),
    path('declineUser/<userId>', views.declineUser, name='declineUser'),
    path('showClients', views.showClients, name='showClients'),
    path('editUser/<userId>', views.editUser, name='editUser'),
    path('deleteUser/<userId>', views.deleteUser, name='deleteUser'),
    path('addCategory', views.addCategory, name='addCategory'),
    path('editCategory/<category_name>', views.editCategory, name='editCategory'),
    path('deleteCategory/<category_name>', views.deleteCategory, name='deleteCategory'),
    path('addUserAdmin', views.addUserAdmin, name='addUserAdmin'),
    path('viewStaff', views.viewStaff, name='viewStaff'),
    path('buyerDashboard', views.buyerDashboard, name='buyerDashboard'),
    path('buyerDashboardView', views.buyerDashboardView, name='buyerDashboardView'),
    path('sellerDashboard', views.sellerDashboard, name='sellerDashboard'),
    path('jointDashboard', views.jointDashboard, name='jointDashboard'),
    path('evaluatorDashboard', views.evaluatorDashboard, name='evaluatorDashboard'),
    path('addAuction', views.addAuction, name='addAuction'),
    path('editAuction/<auction_id>', views.editAuction, name='editAuction'),
    path('deleteAuction/<auction_id>', views.deleteAuction, name='deleteAuction'),
    path('user_login', views.user_login, name='user_login'),
    path('requestItem', views.requestItem, name='requestItem'),
    path('requestItemInfoDrawing/<item>', views.requestItemInfoDrawing, name='requestItemInfoDrawing'),
    path('requestItemInfoPainting/<item>', views.requestItemInfoPainting, name='requestItemInfoPainting'),
    path('requestItemInfoPhotographicImage/<item>', views.requestItemInfoPhotographicImage, name='requestItemInfoPhotographicImage'),
    path('requestItemInfoSculpture/<item>', views.requestItemInfoSculpture, name='requestItemInfoSculpture'),
    path('requestItemInfoCarving/<item>', views.requestItemInfoCarving, name='requestItemInfoCarving'),
    path('myItems', views.myItems, name='myItems'),
    path('verifyItems', views.verifyItems, name='verifyItems'),
    path('acceptedItems', views.acceptedItems, name='acceptedItems'),
    path('viewItemDetails/<item>', views.viewItemDetails, name='viewItemDetails'),
    path('acceptItem/<item>', views.acceptItem, name='acceptItem'),
    path('declineItem/<item>', views.declineItem, name='declineItem'),
    path('viewAuctionItems/<auction_id>', views.viewAuctionItems, name='viewAuctionItems'),
    path('wonItems', views.wonItems, name='wonItems'),
    path('clearPayment/<item_lot>', views.clearPayment, name='clearPayment'),
    path('markSold', views.markSold, name='markSold'),
    path('myPurchases', views.myPurchases, name='myPurchases'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('viewSales', views.viewSales, name='viewSales'),
    path('auctionReport/<auction_id>', views.auctionReport, name='auctionReport'),
    path('viewSoldItems/<auction_id>', views.viewSoldItems, name='viewSoldItems'),
    path('viewHoldItems/<auction_id>', views.viewHoldItems, name='viewHoldItems'),
    path('viewPendingItems/<auction_id>', views.viewPendingItems, name='viewPendingItems'),
    path('browseAuctions', views.browseAuctions, name='browseAuctions'),
    path('showAuctionItemsBuyer/<auction_id>', views.showAuctionItemsBuyer, name='showAuctionItemsBuyer'),
    path('ajax/sendBid/<item_val>',views.sendBid,name='sendBid'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('editProfile', views.editProfile, name='editProfile'),
    path('jointRequest', views.jointRequest, name='jointRequest'),
    path('viewJoint', views.viewJoint, name='viewJoint'),
    path('acceptJointRequest/<userId>', views.acceptJointRequest, name='acceptJointRequest'),
    path('declineJointRequest/<userId>', views.declineJointRequest, name='declineJointRequest'),
    path('landingPage', views.landingPage, name='landingPage'),
    path('categoryItems/<category_name>', views.categoryItems, name='categoryItems'),
    path('allNotifications', views.allNotifications, name='allNotifications'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('normalDashboard', views.normalDashboard, name='normalDashboard'),
    path('editItem/<item>', views.editItem, name='editItem'),
]+static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
