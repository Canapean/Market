from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'title')
    list_display_links = ('title',)


admin.site.register(Product)

