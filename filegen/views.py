import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse

from analytics.services import ReportDataOnMongoDB
from filegen.services import generate_excel_file_report_1

User = get_user_model()


def gen_excel_report_1(request):
    if request.method == "POST":
        depart = json.loads(request.body).get('depart')
        filters = json.loads(request.body).get('filters')
        volumes_list = json.loads(request.body).get('volumes_list')
        column_list = json.loads(request.body).get('column_list')
        user = User.objects.get(pk=request.user.pk)
        elements = {'depart': depart}
        if len(filters) > 0:

            for filter_item in filters:
                category = filter_item.split('_')[0]
                category_item = filter_item.split('_')[1]
                elements[category] = category_item

            data = ReportDataOnMongoDB().find_document(
                elements=elements,
                multiple=True,
                limit=100,
                skip=0,
            )
            url = generate_excel_file_report_1(
                user=user,
                data=data,
                volumes_list=volumes_list,
                column_list=column_list,
                elements=elements,
            )

        else:
            data = ReportDataOnMongoDB().find_document(
                elements=elements,
                summary=True
            )
            url = generate_excel_file_report_1(
                user=user,
                data=data,
                volumes_list=volumes_list,
                column_list=column_list,
                elements=elements,
            )

        return JsonResponse({'data': True, 'body': url}, safe=False)
    return JsonResponse({'detail': 'GET method'})

