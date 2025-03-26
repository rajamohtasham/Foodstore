from django.apps import AppConfig

class StoreConfig(AppConfig):  # Change `StoreConfig` to your app name if different
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'  # Change this to your app's name

    def ready(self):
        import store.signals  # Import signals when the app is ready
