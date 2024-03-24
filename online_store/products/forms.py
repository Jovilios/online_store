from django import forms

from online_store.products.models import Product, ProductImage


class BaseProductForm(forms.ModelForm):
    photos = forms.ImageField(widget=forms.ClearableFileInput(), )

    class Meta:
        model = Product
        fields = ["name", "category", "description", "price", "date_published", "photos"]
        # widgets = {'photos': forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),}
        # photo = forms.ImageField(widget=forms.ClearableFileInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Product Name"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Product Description"})
        self.fields["category"].widget.attrs.update({"class": "form-control", "placeholder": "Category"})
        self.fields["price"].widget.attrs.update({"class": "form-control", "placeholder": "Price"})
        self.fields["date_published"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Date Published", "readonly": "readonly"})
        self.fields["photos"].widget.attrs.update({"class": "form-control", "placeholder": "Select Image"})

    # def save(self, commit=True):
    #     product = super().save(commit=commit)
    #     if commit:
    #         for image in self.cleaned_data.get('photos', []):
    #             ProductImage.objects.create(product=product, image=image)
    #     return product


class AddProductForm(BaseProductForm):
    pass


class EditProductForm(BaseProductForm):
    pass


class DeleteProductForm(BaseProductForm):
    pass
