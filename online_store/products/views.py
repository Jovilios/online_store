from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView


from online_store.products.forms import AddProductForm, EditProductForm, DeleteProductForm
from online_store.products.models import Product
from online_store.user_messages.forms import MessageForm


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/products_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = self.paginator_class(Product.objects.all(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['categories'] = Product.CATEGORY_CHOICES
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["related_products"] = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
        context["product_publisher"] = product.user_profile
        context["message_form"] = MessageForm(initial={'product_id': product.id})
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = product.user_profile.user

            # Option that you cannot write to yourself

            # if message.sender == message.recipient:
            #     return render(request, "web/error_page.html",
            #                   {"error_message": "You cannot write to yourself."})

            message.subject = f"Regarding product: {product.name}"
            message.save()
            return redirect('product_detail', pk=product.pk)
        else:
            context = self.get_context_data()
            context['message_form'] = form
            return self.render_to_response(context)


@login_required
def add_product(request):
    user_profile = request.user.userprofile

    if not user_profile.is_complete():
        messages.error(request, "Please complete your profile before adding a product.")
        return redirect("profile_edit", pk=user_profile.pk)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user_profile = user_profile
            product.save()

            photos = request.FILES.getlist("photos")
            for photo in photos:
                product.photos.create(image=photo)

            return redirect("index")
    else:
        form = AddProductForm()

    context = {
        "form": form,
        "user_profile": user_profile,
    }

    return render(request, "products/product_add.html", context)


@login_required
def edit_product(request, pk):
    user_profile = request.user.userprofile
    product = Product.objects.get(pk=pk)

    if user_profile.user_id != product.user_profile_id:
        return render(request, "web/error_page.html",
                      {"error_message": "You do not have permission to edit this product."})

    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            return redirect("product_detail", pk=product.pk)
    else:
        form = EditProductForm(instance=product)

    context = {
        "form": form,
        "product": product,
        "user_profile": user_profile
    }

    return render(request, "products/product_edit.html", context)


def delete_product(request, pk):
    user_profile = request.user.userprofile
    product = Product.objects.get(pk=pk)

    if user_profile.user_id != product.user_profile_id:
        return render(request, "web/error_page.html",
                      {"error_message": "You do not have permission to edit this product."})

    if request.method == "POST":
        form = DeleteProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = DeleteProductForm(instance=product)

    context = {
        "form": form,
        "product": product
    }

    return render(request, "products/product_delete.html", context)
