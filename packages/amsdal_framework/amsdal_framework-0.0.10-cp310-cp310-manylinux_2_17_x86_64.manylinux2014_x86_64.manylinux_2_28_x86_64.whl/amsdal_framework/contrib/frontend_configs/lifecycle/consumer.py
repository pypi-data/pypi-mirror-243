import logging
from typing import Any

from amsdal_data.transactions.decorators import transaction
from amsdal_utils.lifecycle.consumer import LifecycleConsumer
from amsdal_utils.models.enums import Versions

logger = logging.getLogger(__name__)


class ProcessResponseConsumer(LifecycleConsumer):
    @transaction
    def on_event(
        self,
        request: Any,
        response: dict[str, Any],
    ) -> None:
        from models.contrib.frontend_model_config import FrontendModelConfig  # type: ignore[import-not-found]

        if hasattr(request, 'query_params') and 'class_name' in request.query_params:
            class_name = request.query_params['class_name']
            config = (
                FrontendModelConfig.objects.all()
                .first(
                    class_name=class_name,
                    _metadata__is_deleted=False,
                    _address__object_version=Versions.LATEST,
                )
                .execute()
            )
            response['control'] = config.control.model_dump() if config and config.control else {}
