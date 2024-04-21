from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Товары'

    def ready(self):
        from config.container import container
        container.wire(modules=['.views'])
