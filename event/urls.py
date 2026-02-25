from django.urls import path
from .views import event_list, book_event, dashboard,my_bookings, admin_dashboard
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', event_list, name='event_list'),
    path('book/<int:event_id>/', book_event, name='book_event'),
    path('dashboard/', dashboard, name='dashboard'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
