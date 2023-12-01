from amsdal_framework.contrib.app_config import AppConfig as AppConfig

class AuthAppConfig(AppConfig):
    def on_ready(self) -> None: ...
