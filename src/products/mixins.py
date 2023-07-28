from django.db.models import Q


class FilterQueryMixin:
    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.all()
        search = self.request.GET.get('search')
        product_type = self.request.GET.get('type')
        category = self.request.GET.get('category')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search),
            )
        if product_type:
            queryset = queryset.filter(kind=product_type)
        if category:
            queryset = queryset.filter(categories__name=category, categories__is_active=True)
        return queryset


class CountCartProductsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_products = self.request.session.get('cart_products')
        context.setdefault(
            'count_cart_products',
            (len(cart_products)) if cart_products else 0,
        )
        return context
