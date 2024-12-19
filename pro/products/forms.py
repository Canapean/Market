from django import forms
from django.contrib.auth.models import User

from .models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'price', 'category', 'description', 'thumbnail')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class ProductUpdateForm(ProductCreateForm):
    class Meta:
        model = Product
        fields = ProductCreateForm.Meta.fields


class FeedbackForm(forms.ModelForm):
    problem = forms.CharField(max_length=1000)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
