from django.urls import path, include
#from .views import LNMCallbackUrlAPIView
from .views import create



urlpatterns = [
	path('callback/', create, name='callback'),

]

