from amsdal_framework.contrib.app_config import AppConfig as AppConfig
from amsdal_framework.contrib.frontend_configs.constants import ON_RESPONSE_EVENT as ON_RESPONSE_EVENT
from amsdal_framework.contrib.frontend_configs.lifecycle.consumer import ProcessResponseConsumer as ProcessResponseConsumer

class FronendConfigAppConfig(AppConfig):
    def on_ready(self) -> None: ...
