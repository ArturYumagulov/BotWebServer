# from dash import html, dash_table, dcc
# from django_plotly_dash import DjangoDash
# from dash.dependencies import Input, Output
# import pandas as pd
# import asyncio
# from parse.services import Parsers
# from sales.models import Product, Brand
#
# # Инициализация приложения Dash
# app = DjangoDash('DataTableExample')
#
#
# # Получаем данные из базы данных
# def get_products_data(selected_brands=None):
#     queryset = Product.objects.filter(brand__partkom_code__isnull=False).values("article", "tranzit_price",
#                                                                                 "partkom_price", "brand__name")
#
#     if selected_brands:
#         queryset = queryset.filter(brand__pk__in=selected_brands)
#
#     articles_dict = {}
#
#     for product in queryset:
#         articles_dict[product['article']] = {
#             'Бренд': product['brand__name'],
#             '3.Спец': product['tranzit_price'],
#             'partkom': product['partkom_price']
#         }
#
#     return pd.DataFrame.from_dict(
#         articles_dict,
#         orient='index',
#         columns=['Бренд', '3.Спец', 'partkom']
#     ).reset_index()
#
#
# def get_brands():
#     queryset = Product.objects.filter(brand__partkom_code__isnull=False).values_list("brand__pk", flat=True)
#     brands = Brand.objects.filter(pk__in=queryset).values("pk", "name")
#     return [{'label': brand['name'], 'value': brand['pk']} for brand in brands]
#
#
# df = get_products_data()
#
# # Layout приложения Dash с таблицей
# app.layout = html.Div(
#     style={'height': '100vh'},
#     children=[
#         dcc.Dropdown(
#             id='brand-filter',
#             options=get_brands(),
#             placeholder="Выберите бренд",
#             multi=True,  # Позволяет выбрать несколько значений
#             style={'width': '50%', 'margin-bottom': '20px'}
#         ),
#         dash_table.DataTable(
#             id='parse-table',
#             columns=[{"name": i, "id": i} for i in df.columns],  # Заголовки колонок
#             data=df.to_dict('records'),  # Данные таблицы
#             style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '180px'},
#             style_header={
#                 'backgroundColor': '#ced4da',
#                 'fontWeight': 'bold',
#                 'textAlign': 'center',
#             },
#             page_size=20,  # Количество строк на одной странице
#             sort_action="native",  # Включение сортировки
#             filter_action="native",  # Включение фильтрации
#             row_selectable='multi',  # Возможность выбирать несколько строк
#         ),
#         html.Button(
#             'Обновить данные',  # Текст кнопки
#             id='update-button',
#             n_clicks=0,  # Счетчик кликов
#             style={  # Стили для кнопки
#                 'background-color': '#4CAF50',  # Цвет фона
#                 'color': 'white',  # Цвет текста
#                 'padding': '10px 20px',  # Отступы внутри кнопки
#                 'text-align': 'center',  # Выравнивание текста
#                 'text-decoration': 'none',  # Без подчеркивания
#                 'display': 'inline-block',  # Inline-блок
#                 'font-size': '16px',  # Размер текста
#                 'margin': '10px 2px',  # Внешние отступы
#                 'border': 'none',  # Без границ
#                 'border-radius': '5px',  # Скругленные углы
#                 'cursor': 'pointer',  # Курсор "рука" при наведении
#                 'opacity': 0,
#             }
#         ),
#     ]
# )
#
#
# # Callback для фильтрации и обновления таблицы
# @app.callback(
#     Output('parse-table', 'data'),  # Обновляемые данные таблицы
#     [Input('update-button', 'n_clicks'),  # Срабатывание при клике на кнопку
#      Input('brand-filter', 'value')]  # Входные данные для фильтрации по брендам
# )
# def update_table(n_clicks, selected_brands):
#     # Получаем отфильтрованные данные по брендам
#     df = get_products_data(selected_brands)
#
#     # Преобразуем DataFrame в список словарей для таблицы
#     return df.to_dict('records')
