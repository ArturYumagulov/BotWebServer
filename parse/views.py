# from django.http import HttpResponse
# from django.shortcuts import render
# from django.utils import timezone
#
# from core.tasks import update_price
# from sales.models import Brand, Product
#
#
# # Create your views here.
#
#
# def parse(request):
#     brands = Brand.objects.filter(partkom_code__isnull=False).distinct().values("pk", "name")
#     context = {
#         "brands": brands,
#         'update': Product.objects.filter(edit_date__lte=timezone.now()).first()
#     }
#     return render(request, 'parse/parse.html', context=context)
#
#
# def update_price(request):
#     update_price()
#     return HttpResponse('OK')
#
