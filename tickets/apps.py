from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'
    verbose_name = 'Sistema de Tickets'
    
    def ready(self):
        # Importar signals para que se registren
        import tickets.models.user_profile  # noqa
