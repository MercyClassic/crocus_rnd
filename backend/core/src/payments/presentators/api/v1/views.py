from dependency_injector.wiring import Provide, inject
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.container import Container
from payments.application.interfaces.services.call_me import CallMeServiceInterface
from payments.application.interfaces.services.payment_accept import PaymentAcceptServiceInterface
from payments.application.interfaces.services.payment_create import PaymentCreateServiceInterface
from payments.application.pause import is_user_paused, set_pause_timer
from payments.application.serializers.call_me import CallMeSerializer
from payments.application.serializers.payment import PaymentCreateSerializer


class CreatePaymentAPIView(APIView):
    @inject
    def post(
            self,
            request,
            payment_service: PaymentCreateServiceInterface = Provide[Container.payment_create_service],
    ) -> Response:
        serializer = PaymentCreateSerializer(data=request.data)

        if serializer.is_valid():
            serialized_data = serializer.validated_data
            if is_user_paused(request, 'create_order'):
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data='Вы уже сделали заказ, подождите немного прежде, чем сделать ещё один',
                )
            else:
                set_pause_timer(request, 'create_order')
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='Данные введены неверно, обновите страничку и попробуйте ещё раз',
            )

        payment_url = payment_service.create_payment(
            products=serialized_data['items'],
            amount=serialized_data['amount'],
            customer_name=serialized_data['customer_name'],
            customer_email=serialized_data['customer_email'],
            receiver_name=serialized_data['receiver_name'],
            customer_phone_number=serialized_data['customer_phone_number'],
            receiver_phone_number=serialized_data['receiver_phone_number'],
            without_calling=serialized_data['without_calling'],
            delivery_address=serialized_data['delivery_address'],
            delivery_date=serialized_data['delivery_date'],
            delivery_time=serialized_data['delivery_time'],
            note=serialized_data['note'],
            cash=serialized_data['cash'],
            delivering=serialized_data['delivering'],
        )

        if not payment_url:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='Данные введены неверно, обновите страничку и попробуйте ещё раз',
            )
        return Response({'payment_url': payment_url}, status=status.HTTP_201_CREATED)


class AcceptPaymentAPIView(APIView):
    @inject
    def post(
            self,
            request,
            payment_service: PaymentAcceptServiceInterface = Provide[Container.payment_accept_service],
    ) -> Response:
        if payment_service.handle_webhook(request_data=request.data):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CallMeAPIView(APIView):
    @inject
    def post(
            self,
            request,
            call_me_service: CallMeServiceInterface = Provide[Container.call_me_service],
    ) -> Response:
        serializer = CallMeSerializer(data=request.data)

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
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='Данные введены неверно, обновите страничку и попробуйте ещё раз',
            )
