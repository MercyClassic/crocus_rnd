from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'
    verbose_name = 'Оплата'

    def ready(self):
        from config.container import container
        container.wire(modules=['payments.api.v1.views'])
