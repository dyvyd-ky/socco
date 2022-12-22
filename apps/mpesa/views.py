import json
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from .models import LNMOnline
from .serializers import LNMOnlineSerializer


class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):

        #request_data = request.data
        payload = request.data
        info = {}
        callback = payload['Body']['stkCallback']
        info['ResultCode'] = callback['ResultCode']
        info['ResultDesc'] = callback['ResultDesc']
        info['MerchantRequestID'] = callback['MerchantRequestID']
        info['CheckoutRequestID'] = callback['CheckoutRequestID']
        metadata = callback.get('CallbackMetadata')
        if metadata:
            metadata_items = metadata.get('Item')
            for item in metadata_items:
                info[item['Name']] = item.get('Value')

        
        our_model = LNMOnline.objects.create(
            CheckoutRequestID=info['CheckoutRequestID'],
            MerchantRequestID=info['MerchantRequestID'],
            Amount=info[item['Amount']],
            ResultCode=info['ResultCode'],
            ResultDesc=info['ResultDesc'],
            MpesaReceiptNumber=info[item['MpesaReceiptNumber']],
            TransactionDate=info[item['TransactionDate']],
            PhoneNumber=info[item['PhoneNumber']]
        )

        our_model.save()

        from rest_framework.response import Response

        return Response({"OurResultDesc": "..and it all worked out!"})


