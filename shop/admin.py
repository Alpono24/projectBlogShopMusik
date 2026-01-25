from django.contrib import admin
from .models import Product, Category, BrandName, Unit, CurrencyRateUSD, CurrencyRateEUR, Order, CartItem, Seller, \
    OrderDetail


@admin.register(BrandName)
class BrandNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'category__name')
    ordering = ('-name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('-name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','brand', 'quantity', 'unit',  'category', 'description', 'price', 'price_with_vat', 'price_in_byn', 'price_in_eur', 'in_stock','created_at', 'updated_at',  'has_image')
    list_filter = ('in_stock', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('price', 'in_stock','category')
    ordering = ('-category', '-price')

    def has_image(self, obj):
        return 1 if obj.image else None
    has_image.short_description = 'Наличие изображения'
    has_image.boolean = True

class ProductInline(admin.TabularInline):
    model = Product
    extra = 5



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    inlines = [ProductInline]

    def product_count(self, obj):
        return obj.product_set.count()

    product_count.short_description = 'Количество товаров'



@admin.register(CurrencyRateUSD)
class CurrencyRateBYNAdmin(admin.ModelAdmin):
    list_display = ['rate_usd', 'currency_usd', 'created_at']
    search_fields = ['rate_usd']
    ordering = ['-created_at']
    readonly_fields = ('rate_usd', 'currency_usd',)



@admin.register(CurrencyRateEUR)
class CurrencyRateEURAdmin(admin.ModelAdmin):
    list_display = ['rate_eur', 'currency_eur', 'created_at']
    search_fields = ['rate_eur']
    ordering = ['-created_at']
    readonly_fields = ('rate_eur', 'currency_eur',)



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'selected', 'total_price')
    search_fields = ('user__username', 'product__name')
    list_filter = ('selected', )
    readonly_fields = ('total_price', )  # Поля вычисляемые, не подлежат редактированию

    fieldsets = (
        ("Основные данные", {'fields': ('user', 'product', 'quantity', 'selected')}),
        ("Цены", {'fields': ('total_price',)}),
    )


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'address', 'phone_number', 'website')
    search_fields = ('company_name', 'email', 'address')



class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 5
    fields = ('product', 'quantity',)
    readonly_fields = ()
    can_delete = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'created_at', 'status', 'is_sent', 'notes', )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'total_amount', )
    inlines = [OrderDetailInline]

    def total_amount(self, obj):
        return obj.total_amount

    total_amount.short_description = 'Общая сумма'

    def created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    created_at.short_description = 'Дата создания'


