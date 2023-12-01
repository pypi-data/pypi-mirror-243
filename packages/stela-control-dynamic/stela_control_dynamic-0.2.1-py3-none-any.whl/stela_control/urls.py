from django.urls import path, include
from . import views

    
app_name="stela"

urlpatterns = [
    #stela Home
    path('i18n/', include('django.conf.urls.i18n')),
    path('stela-api/', views.requestAPI, name="requestAPI"),
    path('meta-data/', views.metaID, name="meta_data"),
    path('ig-data/', views.igID, name="ig_data"),
    path('meta-api/', views.metaAPI, name="meta_request"),
    path('test/', views.test, name="test"),
    path('validators/', views.validators, name="validators"),

    #Stela Dashboard
    path('console/newcomer', views.newcomer, name="newcomer"),
    path('console/home', views.console, name="console"),
    path('pro-stela/chats/', views.stelaChat, name="chats"),
    path('pro-stela/expert', views.stelaExpert, name="expert"),

    #access
    path('', views.loginstela, name='login'),
    path('logout/', views.logout_view, name="logout"),

    #Inbox
    path('content/inbox', views.contactMessage, name="inbox"), 
    
    #Support 
    path('support-center', views.supportCenter, name="support"),
    path('support-case/<int:id>', views.updateSupport, name="support-update"),

    #Comments
    path('comments-blog', views.commentsBlog, name="commentsBlog"),

    #StelaContent
    path('dycontent', views.mainContent, name="main-content"),
    path('dycontent/main', views.siteMain, name="site-main"),
    path('dycontent/docs', views.siteDocs, name="site-docs"),
    path('dycontent/userconnect', views.userConnect, name="user-connect"),
    path('dycontent/stela-story', views.stelaStory, name="stela_story"),
    
    #inventory
    path('inventory-control/services', views.services, name="service"),
    path('inventory-control/products', views.products, name="products"),
    path('inventory-control/update-product/<int:id>', views.updateProduct, name="updateProduct"),
    path('inventory-control/templates', views.templates, name="template"),

    #metaplatform
    path('marketing/business-suite', views.metaSuite, name="meta_business"),
    path('marketing/business-suite/<int:id>', views.metaDetail, name="meta_detail"),
    path('marketing/business-suite/<int:id>/content-pro', views.page, name="fb_page"),
    path('marketing/business-suite/<int:id>/analythics', views.pageAnalythics, name="page_insights"),
    path('marketing/<int:id>/icreative-actions/<int:ig>/', views.IcreativeActions, name="ic_actions"),
    path('marketing/business-suite/<int:id>/insight-creative/<int:ig>', views.insightCreative, name="increative"),
    path('marketing/business-suite/<int:id>/analyzer/<int:ig>', views.igAnalyzer, name="iganalyzer"),
    path('marketing/business-suite/fbmedia', views.fbmedia, name="fb_media"),
    path('marketing/business-suite/igmedia', views.igmedia, name="ig_media"),
    path('marketing/business-suite/ig-counter/<int:id>/', views.igCounter, name="ig_counter"),
    path('marketing/business-suite/ig-check/<int:id>/', views.igCheckPost, name="check_ig_post"),
    path('marketing/<int:id>/grid/<int:ig>/', views.grid, name="ig_grid"),
    
    #googlePlatform
    path('googleapis/auth', views.googleAuth, name="google_auth"),

    #orders
    path('orders', views.orders, name="orders_list"),
    path('orders/<int:id>/', views.orders_update, name="orders_update"),
    path('orders-request/', views.orders_requests, name="delete_request"),

    # #reviews
    # path('reviews-list', views.reviews_list, name="review_list"),
    # path('update-review/<int:id>/', views.update_review, name="update_review"),
    # path('delete-review/', views.delete_reviews, name="delete_review"),
    # path('search-auto/review/', views.autocompleteReview, name="autocomplete_review"),
    
    #users
    path('users-control', views.users, name="users"),
    path('users/<int:id>/', views.update_users, name="update_user"),
    path('subscribers-control', views.subscribers, name="subscribers"),
    path('subscribers-control/<int:id>/', views.update_subscribers, name="update_subscribers"),

    #email-events
#    path('store/send-email/order-confirmation/', views.send_order_confirm_store, name="email_order_confirm_store"),
    
    #stelaPayments
    path('payments/home', views.paymentsHome, name="homebrew"),
    path('payments/add-wallet', views.addWallet, name="addwallet"),
    path('payments/wallets', views.Wallets, name="wallets"),
    path('payments/withdrawals/', views.withdrawals, name="withdrawals"),

    #StelaBilling
    path('billings/home', views.stelaBilling, name="billing"),
    path('billings/new-bill/', views.createBill, name="bill_new"),
    path('billings/edit-bill/<int:id>', views.editBill, name="edit_billing"),
    path('billings/preview/<int:id>', views.previewBilling, name="previewBill"),
    path('billings/get-billing/<int:id>', views.get_billing, name="get_billing"),
    path('billings/bill-detail/<int:id>', views.get_invoice, name="get_invoice"),
    path('billings/recipt-detail/<int:id>', views.get_invoice, name="get_invoice"),
    path('billings/recipt-detail-ves/<int:id>', views.get_invoice_ves, name="get_invoice_ves"),

 ]   