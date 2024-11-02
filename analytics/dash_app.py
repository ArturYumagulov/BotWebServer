from dash import html, dash_table, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import pandas as pd
import asyncio
from urllib.parse import urlencode, quote

from census.models import Census
from parse.services import Parsers
from sales.models import Product, Brand, OrderItem
from collections import UserDict
from tasks.models import Task

# Инициализация приложения Dash
app = DjangoDash('TaskDataDashboard')

queryset = Task.objects.filter(base__group__name="Сенсус")


def get_filters(data, pk_name, name):
    result = {}
    for department in data:
        dept_id = department[pk_name]
        if dept_id not in result:
            result[dept_id] = {'label': department[name], 'value': dept_id}
    return list(result.values())


def get_tasks(data, selected_departments=None):
    if selected_departments:
        data = data.filter(worker__department__pk=selected_departments)

    articles_dict = {}

    for task in data:
        potential_count = Census.objects.filter(worker=task.worker, edited=True, working__isnull=True).count()

        worker = quote(task.worker.name, safe="")
        author = quote(task.author.name, safe="")
        department = task.worker.department.name
        census = Census.objects.filter(worker=task.worker)

        url = f"/analytics/?worker={worker}&author={author}&depart={department}"

        if potential_count > 0:
            potential_count = f'<p style="text-align: center; text-decoration: none;"><a href="{url}" target="_blank" title="Перейти">{potential_count}</a></p>'
        else:
            potential_count = f'<p style="text-align: center;">{potential_count}</p>'

        articles_dict[task.worker.name] = {
            'department': task.worker.department.name,
            'author': task.author.name,
            'tasks': data.filter(worker=task.worker, author__name=task.author.name).count(),
            'ready': data.filter(worker=task.worker, author__name=task.author.name, status="Выполнено").count(),
            'potential': potential_count,
            'active': census.filter(working__isnull=False).count(),
            'contract': census.filter(working__contract__isnull=False).count(),
            'amount': sum(OrderItem.objects.filter(order__partner__in=census.values_list('working_id', flat=True)).values_list('total', flat=True))
        }
    return pd.DataFrame.from_dict(
        articles_dict,
        orient='index',
        columns=['department', 'author', 'tasks', 'ready', 'active', 'potential', 'contract', 'amount']
    ).reset_index()


df = get_tasks(queryset)

department_filters = get_filters(queryset.values('worker__department__name', 'worker__department').distinct(),
                                 'worker__department', 'worker__department__name')

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

app.layout = html.Div(
    style={'height': '100%', 'width': '100%'},
    children=[
        html.H2(children='Общее выполнение задач Сенсуса', style={'textAlign': 'center'}),
        html.Div(
            className='filters-block',
            style={'display': 'flex', 'width': '100%', 'justify-content': 'start', 'margin-bottom': '15px'},
            children=[dcc.Dropdown(
                id='department-dropdown',
                options=department_filters,
                placeholder="Подразделение",
                style={'width': '200px', 'margin-right': '15px'},
            ),
            ]),
        dash_table.DataTable(
            id='task-table',
            columns=[
                {"name": "Исполнитель", "id": "index"},
                {"name": "Подразделение", "id": "department"},
                {"name": "Автор", "id": "author"},
                {"name": "Количество", "id": "tasks"},
                {"name": "Действующие торговые точки", "id": "active"},
                {"name": "Потенциальные торговые точки", "id": "potential", "presentation": "markdown"},
                {"name": "Договор", "id": "contract"},
                {"name": "Сумма отгрузки", "id": "amount"},
                     ],
            data=df.to_dict('records'),
            style_cell={'textAlign': 'center', 'minWidth': '100px', 'width': '100px', 'maxWidth': '180px'},
            style_header={
                'backgroundColor': '#ced4da',
                'fontWeight': 'bold',
                'textAlign': 'center',
            },
            page_size=20,  # Количество строк на одной странице
            sort_action="native",  # Включение сортировки
            filter_action="native",  # Включение фильтрации
            row_selectable='multi',  # Возможность выбирать несколько строк
            markdown_options={"html": True},
            style_data_conditional=[
                {
                    'if': {'column_id': 'potential'},
                    'textDecoration': 'none',
                    'color': 'black',
                    'width': 'auto'
                }
            ],
        ),
    ])


@app.callback(
    Output('task-table', 'data'),
    [
        # Input('update-button', 'n_clicks'),
    Input('department-dropdown', 'value')]
)
def update_table(selected_departments):
    # Получаем отфильтрованные данные по брендам
    df = get_tasks(queryset, selected_departments)

    # Преобразуем DataFrame в список словарей для таблицы
    return df.to_dict('records')
