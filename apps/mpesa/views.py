import json
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from .models import LNMOnline
from .serializers import LNMOnlineSerializer
from rest_framework.response import Response
from django.http import HttpResponse

class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):

        #request_data = request.data
        payload = request.data
        callback = payload['Body']['stkCallback']
        code = callback['ResultCode']
        desc = callback['ResultDesc']
        merchant = callback['MerchantRequestID']
        checkout = callback['CheckoutRequestID']
        metadata = callback.get('CallbackMetadata')
        
        '''metadata_items = metadata.get('Item')
        for item in metadata_items:
            info[item['Name']] = item.get('Value')'''
        

        

        
        our_model = LNMOnline.objects.create(
            CheckoutRequestID=checkout,
            MerchantRequestID=merchant,
            ResultCode=code,
            ResultDesc=desc,
            metadata = metadata
        )

        our_model.save()
        return Response({"OurResultDesc": "YEEY!!! It worked!"})


        