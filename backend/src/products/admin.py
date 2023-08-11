from django.contrib import admin
from django.contrib.sessions.models import Session

from products.models import Category, Product, ProductCategory, ProductImage


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    readonly_fields = ['thumbnail']

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('product')
            .only('image', 'product_id')
        )


class ProductCategoryInline(admin.StackedInline):
    model = ProductCategory
    readonly_fields = ['get_category_thumbnail']

    def get_category_thumbnail(self, obj):
        return obj.category.thumbnail()
    get_category_thumbnail.short_description = 'Изображение категории'

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('category')
            .select_related('product')
            .only('product__title', 'category__name', 'category__image')
        )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'thumbnail', 'slug', 'price', 'kind', 'is_active')
    list_display_links = ('id', 'title', 'slug')
    search_fields = ('title', 'description')
    list_editable = ('is_active', )
    list_filter = ('is_active', )
    fields = ('title', 'slug', 'description', 'image', 'thumbnail', 'price', 'kind', 'is_active')
    readonly_fields = ('thumbnail', )
    prepopulated_fields = {'slug': ('title', )}
    inlines = [ProductImageInline, ProductCategoryInline]
    show_full_result_count = False


class ProductImageAdmin(admin.ModelAdmin):
    show_full_result_count = False


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product_title', 'get_category_name')
    list_display_links = ('id', 'get_product_title', 'get_category_name')
    show_full_result_count = False

    def get_product_title(self, obj):
        return obj.product.title
    get_product_title.short_description = 'Название товара'

    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = 'Название категории'

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('product')
            .select_related('category')
            .only('product__title', 'category__name')
        )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'thumbnail', 'is_active')
    fields = ('name', 'image', 'thumbnail', 'is_active')
    readonly_fields = ('thumbnail', )
    list_display_links = ('id', 'name', 'thumbnail')
    search_fields = ('name', )
    list_editable = ('is_active', )
    list_filter = ('is_active', )
    show_full_result_count = False


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Session, SessionAdmin)

admin.site.site_header = 'Административная панель'
admin.site.site_title = 'Админ-панель'
