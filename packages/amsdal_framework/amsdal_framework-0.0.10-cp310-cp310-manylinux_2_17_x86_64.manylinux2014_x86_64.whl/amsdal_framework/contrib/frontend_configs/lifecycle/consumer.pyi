from _typeshed import Incomplete
from amsdal_utils.lifecycle.consumer import LifecycleConsumer
from typing import Any

logger: Incomplete

class ProcessResponseConsumer(LifecycleConsumer):
    def on_event(self, request: Any, response: dict[str, Any]) -> None: ...
