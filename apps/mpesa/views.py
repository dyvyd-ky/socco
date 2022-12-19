# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import utils

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .core import MpesaClient
from decouple import config
from datetime import datetime

from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from .models import LNMOnline
from .serializers import LNMOnlineSerializer



class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0][
            "Value"
        ]
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][1]["Value"]
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][2]["Value"]

        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
            3
        ]["Value"]

        from datetime import datetime

        str_transaction_date = str(transaction_date)

        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")

        import pytz
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)

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

        return Response({"OurResultDesc": "YEEY!!! It worked!"})

