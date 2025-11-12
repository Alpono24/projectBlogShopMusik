from django.contrib import admin
from .models import Product, Category


# Register your models here.

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price')
#     list_filter = ('in_stock', 'category')
#     search_fields = ('name',)
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


@admin.action(description="Скрыть выбранные товары")
def mark_as_unavailable(modeladmin, request, queryset):
    updated = queryset.update(in_stock=False)
    modeladmin.message_user(request, f"Обновлено {updated} товаров: помечены как недоступные")


@admin.action(description="Добавить выбранные товары")
def mark_as_available(modeladmin, request, queryset):
    updated = queryset.update(in_stock=True)
    modeladmin.message_user(request, f"Обновлено {updated} товаров: помечены как доступные")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_with_vat', 'in_stock', 'category', 'is_expensive',)
    list_filter = ('in_stock', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('price', 'in_stock')
    ordering = ('-category', '-price')
    actions = [mark_as_unavailable, mark_as_available]

    def is_expensive(self, obj):
        return obj.price > 1000

    is_expensive.short_description = 'Дорогой товар'
    is_expensive.boolean = True


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    inlines = [ProductInline]

    def product_count(self, obj):
        return obj.product_set.count()

    product_count.short_description = 'Количество товаров'
