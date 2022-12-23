from django.urls import path, include
#from .views import LNMCallbackUrlAPIView
from .views import ConfirmView



urlpatterns = [
	path('callback/', ConfirmView.as_view(), name='callback'),

]

