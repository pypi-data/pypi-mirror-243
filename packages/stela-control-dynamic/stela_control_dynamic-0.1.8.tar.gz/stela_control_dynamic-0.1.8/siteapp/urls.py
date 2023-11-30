from django.urls import path, include
from . import views


    
app_name="siteapp"

urlpatterns = [
    path('', views.home, name="home"),
    #path('product-detail/<slug:slug>', views.product_detail, name="product_detail"),
    path('gallery/<int:id>', views.userGallery, name="user_gallery"),
    path('gallery/', views.gallery, name="gallery"),
    path('blog-detail/<slug:slug>', views.blog_detail, name="blog_detail"),
    #path('pricing', views.pricing, name="pricing"),
    path('contact', views.new_message, name="contact"),
    path('checkout', views.checkout, name="checkout"),
    #path('get-date/', views.getDate, name="get_date"),
    path('cart_add', views.cart_add, name="cart_add"),
    path('reorder', views.reorder, name="reorder"),
    # path('extra_add', views.extra_add, name="extra_add"),
    path('order-placed', views.order_placed, name="order-placed"),
    path('newsletter/suscribe/', views.newsletter, name="newsletter"),
    #docs
    path('about-us', views.aboutUs, name="about_us"),
    path('terms', views.terms, name="terms"),

]


