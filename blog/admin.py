from django.contrib import admin

from .models import Post, Category


# Register your models here.

@admin.register(Post)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'author', 'created_at')
    list_editable = ('body', 'author',)
    ordering = ('-created_at',)


class ObjectInline(admin.TabularInline):
    model = Post
    fields = ('title', 'body', 'author')
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ObjectInline]