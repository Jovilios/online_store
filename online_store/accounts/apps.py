from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_store.accounts'

    def ready(self) -> None:
        import online_store.accounts.signals
