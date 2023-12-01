from django.urls import path, re_path
from . import views
    
app_name="nexus"

urlpatterns = [
    path('console', views.console, name="console"),
    path('settings', views.profile, name="profile"),
    path('edit', views.edit_profile, name="edit_profile"),
    path('appointments', views.appointments, name="appointments"),
    path('search-auto/appointments/', views.autocompleteBooking, name="autocomplete_booking"),
    path('order-detail/<int:id>/', views.order_detail, name="order_detail"),
    path('review/<int:id>/', views.comment_view, name="comment_view"),
    path('clubpoints', views.clubpoints, name="clubpoints"),
    path('support', views.support_view, name="support"),
    path('create-case/<int:id>', views.create_case, name="create_case"),
    path('update-case/<int:id>', views.update_case, name="update_case"),
    path('search-auto/support/', views.autocompleteSupport, name="autocomplete_support"),
]