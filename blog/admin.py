from django.contrib import admin
from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'body', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    list_filter = ('author', 'category', 'created_at')

    list_editable = ('title', 'body', 'author', 'category')
    readonly_fields = ('created_at', 'updated_at')

    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    list_per_page = 5

class PostInline(admin.TabularInline):
    model = Post
    extra = 2

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [PostInline]







