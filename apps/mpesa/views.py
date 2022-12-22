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
        print(request.data, "this is request.data")

        request_data = json.dumps(request.body.decode())
        request_data = json.loads(request_data)
        merchant_request_id = request_data["Body"]["stkCallback"]["MerchantRequestID"]
        print(merchant_request_id, "this should be MerchantRequestID")
        checkout_request_id = request_data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request_data["Body"]["stkCallback"]["ResultCode"]
        result_description = request_data["Body"]["stkCallback"]["ResultDesc"]
        amount = request_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0][
            "Value"
        ]
        print(amount, "this should be an amount")
        mpesa_receipt_number = request_data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][1]["Value"]
        print(mpesa_receipt_number, "this should be an mpesa_receipt_number")

        transaction_date = request_data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][2]["Value"]
        print(transaction_date, "this should be an transaction_date")

        phone_number = request_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
            3
        ]["Value"]
        print(phone_number, "this should be an phone_number")

        from datetime import datetime

        str_transaction_date = str(transaction_date)
        print(str_transaction_date, "this should be an str_transaction_date")

        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
        print(transaction_datetime, "this should be an transaction_datetime")

        import pytz
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)
        print(aware_transaction_datetime, "this should be an aware_transaction_datetime")


        from mpesa.models import LNMOnline

        our_model = LNMOnline.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
        )

        our_model.save()

        from rest_framework.response import Response

        return Response({"OurResultDesc": "..and it all worked out!"})


