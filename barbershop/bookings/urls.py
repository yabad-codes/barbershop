from django.urls import path
from .views import BookingView

urlpatterns = [
	path('bookings/', BookingView.as_view()),
	path('bookings/<int:id>/', BookingView.as_view())
]