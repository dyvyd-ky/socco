# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
#from .LipaNaMpesaOnline import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from .serializers import PaymentTransactionSerializer


class ConfirmView(APIView):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [AllowAny, ]


    def post(self, request):
        # save the data
        request_data = request.data
        #request_data = json.loads(request_data)
        body = request_data.get('Body')
        resultcode = body.get('stkCallback').get('ResultCode')
        
        # Perform your processing here e.g. print it out...
        if resultcode == 0:
            print('Payment successful')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            merchantId = body.get('stkCallback').get('MerchantRequestID')
            desc = body.get('stkCallback').get('ResultDesc')
            metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
            for data in metadata:
                if data.get('Name') == "MpesaReceiptNumber":
                    receipt_number = data.get('Value')
                if data.get('Name') == "Amount":
                    amount = data.get('Value')
                if data.get('Name') == "TransactionDate":
                    trans_date = data.get('Value')
                if data.get('Name') == "PhoneNumber":
                    phone_number = data.get('Value')
            transaction = PaymentTransaction.objects.create(
                CheckoutRequestID=requestId,
                MerchantRequestID=merchantId,
                ResultDesc=desc,
                MpesaReceiptNumber=receipt_number,
                Amount=amount,
                TransactionDate=trans_date,
                PhoneNumber=phone_number,
                )
            transaction.save()

        else:
            print('unsuccessfull')

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1237867865"
        }
        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)

    def get(self, request):
        return Response("Confirm callback", status=HTTP_200_OK)