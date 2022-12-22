from django.urls import path, include
from .views import LNMCallbackUrlAPIView



urlpatterns = [
	path('callback/', LNMCallbackUrlAPIView.as_view(), name='callback'),

]

