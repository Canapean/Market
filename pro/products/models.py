from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

User = get_user_model()


class Product(models.Model):
    title = models.CharField(verbose_name='Название товара', max_length=255)
    price = models.FloatField(verbose_name='Цена товара')
    description = models.TextField(verbose_name='описание товара', max_length=500)
    thumbnail = models.ImageField(
        verbose_name='Превью товара',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    seller = models.ForeignKey(to=User, verbose_name='Продавец', on_delete=models.SET_DEFAULT, related_name='seller_posts', default=1)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')

    class Meta:
        db_table = 'app_products'
        ordering = ['-time_create']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return self.title


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        return self.title

