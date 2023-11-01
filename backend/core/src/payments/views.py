from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from container import container
from utils.pause import check_for_pause_timer, set_pause_timer

from .serializers import CallMeSerializer, PaymentCreateSerializer
from .services.payment_accept import payment_acceptance

bad_request_response = Response(
    status=status.HTTP_400_BAD_REQUEST,
    data='Данные введены неверно, обновите страничку и попробуйте ещё раз',
)


class CreatePaymentAPIView(GenericAPIView):
    serializer_class = PaymentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serialized_data = serializer.validated_data
            if not check_for_pause_timer(request, 'create_order'):
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data='Вы уже сделали заказ, подождите немного прежде, чем сделать ещё один',
                )
        else:
            return bad_request_response

        payment_service = container.payment_service()
        payment_service.fill_in_with_data(serialized_data)
        payment_url = payment_service.create_payment()
        set_pause_timer(request, 'create_order')

        if not payment_url:
            return bad_request_response
        return Response({'payment_url': payment_url}, status=status.HTTP_201_CREATED)


class AcceptPaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if payment_acceptance(request.data):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CallMeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CallMeSerializer(data=request.data)

        call_me_service = container.call_me_service()

        if serializer.is_valid():
            if call_me_service.create_call_me_request(
                request,
                serializer.validated_data.get('phone_number'),
            ):
                set_pause_timer(request, 'call_me')
                return Response(
                    status=status.HTTP_200_OK,
                    data='Спасибо за обращение, скоро мы вам перезвоним!',
                )
            else:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data='Вы уже заказывали звонок недавно, '
                    'подождите немного, прежде, чем заказать ещё один',
                )

        return bad_request_response
