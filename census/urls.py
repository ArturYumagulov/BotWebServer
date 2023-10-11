from django.urls import path

from . import views

urlpatterns = [
    path('f/<int:pk>', views.census, name='census'),
    path('load/', views.load_data, name='census_load'),
    path('partner-search/', views.get_partners, name='partners'),
    path('point-names/', views.get_point_names, name='point_names'),
    path('point-category/', views.get_point_category, name='point_category'),
    path('sto-types/', views.get_sto_type, name='sto_types'),
    path('point-vectors', views.get_point_vector, name='point_vectors'),
    path('access-category', views.get_accessories_category, name='access_category'),
    path('access-category/<str:category_id>', views.get_accessories_category_item),
    path('cars-list/', views.get_cars, name='cars_list'),
    path('oil-list/', views.get_oils, name='oil_list'),
    path('filter-list/', views.get_filters, name='filter_list'),
    path('controls/', views.get_control_data, name='controls_list'),
    path('providers/', views.get_providers, name='providers'),
]
