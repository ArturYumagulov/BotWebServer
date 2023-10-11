from django.apps import AppConfig


class CensusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'census'
    verbose_name = "Сенсус торговой точки"
    verbose_name_plural = "Сенсусы торговых точек"
