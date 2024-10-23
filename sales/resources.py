from import_export import resources

from .models import Product


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        import_id_fields = ['code']
        fields = ('code', 'name', 'brand', 'article', 'access_category', 'tranzit_price')
