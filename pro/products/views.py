from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from .models import Product, Category
from .forms import ProductCreateForm, ProductUpdateForm, FeedbackForm
from .mixins import AuthorRequiredMixin
from pro import settings


class ProductListView(ListView, FormView, SuccessMessageMixin):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    form_class = FeedbackForm
    success_url = ('/')
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort', 'asc')

        if query:
            queryset = queryset.filter(Q(title__icontains=query))

        if sort_by == 'desc':
            queryset = queryset.order_by('-price')  # убывание
        else:
            queryset = queryset.order_by('price')  # возрастание

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['search_query'] = self.request.GET.get('q', '')
        context['sort_order'] = self.request.GET.get('sort', 'asc')
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        subject = f"Обращение от пользователя {data['first_name']}"
        message = f"{data['first_name']} {data['last_name']} отправил обращение в поддержку.\n\n" \
                  f"Обращение: {data['problem']}\n\n" \
                  f"Почта: {data['email']}"
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class ProductByCategoryListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(id=self.kwargs['id'])
        queryset = Product.objects.all().filter(category__id=self.category.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_create.html'
    form_class = ProductCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ProductUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'products/product_update.html'
    context_object_name = 'product'
    form_class = ProductUpdateForm
    login_url = 'home'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context


class ProductDeleteView(AuthorRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('home')
    context_object_name = 'product'
    template_name = 'products/product_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'
        return context


class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        cart_items = [
            {
                'product': product,
                'quantity': cart[str(product.id)],
                'total_price': product.price * cart[str(product.id)],
            }
            for product in products
        ]
        total_cost = sum(item['total_price'] for item in cart_items)

        return render(request, 'products/cart.html', {
            'cart_items': cart_items,
            'total_cost': total_cost,
        })


class AddToCartView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        return redirect('cart')


class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
        request.session['cart'] = cart
        return redirect('cart')

