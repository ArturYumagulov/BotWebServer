import io
from django.core.files import File
from xlsxwriter.workbook import Workbook
from .models import ReportDownloadFile


def generate_excel_file_report_1(user, data, volumes_list, column_list, elements):
    output = io.BytesIO()  # Create an in -memory output file
    workbook = Workbook(output, {
        'in_memory': True
    })  # Create a workbook in memory
    worksheet = workbook.add_worksheet()  # Add a worksheet to the workbook

    columns_list = []
    for head in range(len(column_list)):
        if head < 9:
            columns_list.append(column_list[head]['name'])
        elif head == 9:
            for vol, dt in enumerate(volumes_list):
                columns_list.append(volumes_list[vol]['name'])
        elif head > 9:
            columns_list.append(column_list[head]['name'])

    for column in range(len(columns_list)):
        worksheet.write(0, column, columns_list[column])

    for row, data_item in enumerate(data):
        for col in range(len(columns_list) - len(volumes_list) + 1):
            if col < 8:
                worksheet.write(row + 1, col, data_item[column_list[col]['id']])
            elif col == 8:
                if data_item[column_list[col]['id']] is not None:
                    if len(data_item[column_list[col]['id']]) > 0:
                        context = ''
                        for i in data_item[column_list[col]['id']]:
                            context += i + ', '
                        worksheet.write(row + 1, col, context)
                    else:
                        worksheet.write(row + 1, col, "")
                else:
                    worksheet.write(row + 1, col, "")
            elif col == 9:
                for vol in range(len(data_item[column_list[col]['id']])):
                    worksheet.write(row + 1, col + vol, data_item[column_list[col]['id']][vol]['value'])
            elif col > 9:
                worksheet.write(row + 1, len(volumes_list) + col - 1, data_item[column_list[col]['id']])

    workbook.close()  # Close the workbook

    output.seek(0)  # Rewind the buffer

    new_report = ReportDownloadFile()
    new_report.user = user
    new_report.elements = elements
    new_report.file.save(f'report_1_{user.username}.xlsx', File(output), save=True)

    output.close()  # Close the in -memory output file

    return new_report.file.url
