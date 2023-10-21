from django.db.models import Manager, QuerySet


class ProductQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductManager(Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()
