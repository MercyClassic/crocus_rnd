from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ioc.ioc import provider
from payments.pause import is_user_paused, set_pause_timer
from payments.serializers import CallMeSerializer, PaymentCreateSerializer

bad_request_response = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data='Данные введены неверно, обновите страничку и попробуйте ещё раз',
)


class CreatePaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)

        if serializer.is_valid():
            serialized_data = serializer.validated_data
            if is_user_paused(request, 'create_order'):
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data='Вы уже сделали заказ, подождите немного прежде, чем сделать ещё один',
                )
        else:
            return bad_request_response

        payment_service = provider.provide_payment_create_service()
        payment_service.fill_in_with_data(serialized_data)
        payment_url = payment_service.create_payment()
        set_pause_timer(request, 'create_order')

        if not payment_url:
            return bad_request_response
        return Response({'payment_url': payment_url}, status=status.HTTP_201_CREATED)


class AcceptPaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payment_service = provider.provide_payment_accept_service(request.data)
        if payment_service.handle_webhook():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CallMeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CallMeSerializer(data=request.data)

        call_me_service = provider.provide_call_me_service()

        if serializer.is_valid():
            serialized_data = serializer.validated_data
            if is_user_paused(request, 'call_me'):
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data='Вы уже заказывали звонок недавно, '
                    'подождите немного, прежде, чем заказать ещё один',
                )
            call_me_service.create_call_me_request(
                request,
                serialized_data.get('phone_number'),
            )
            set_pause_timer(request, 'call_me')
            return Response(
                status=status.HTTP_200_OK,
                data='Спасибо за обращение, скоро мы вам перезвоним!',
            )

        return bad_request_response
