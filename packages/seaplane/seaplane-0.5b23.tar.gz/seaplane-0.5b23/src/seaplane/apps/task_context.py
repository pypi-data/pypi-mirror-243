from typing import Any, Optional

import json

from seaplane_framework.flow import processor

from seaplane.logs import log
from seaplane.object import object_store


class TaskContext:
    """TaskContext is what a Task receives."""

    def __init__(self, body: bytes, meta: dict[str, Any]):
        self.body = body
        # For now let's not imply that customers should touch this
        self._meta = meta
        self._object_data: Optional[bytes] = None

    def emit(self, message: bytes, batch_id: int = 1) -> None:
        """Queues message to send once the task completes.
        batch_id: The index with which to refer to this member of the batch."""
        new_meta = self._meta.copy()
        new_meta["_seaplane_batch_hierarchy"] += f".{batch_id}"
        output_msg = processor._Msg(message, new_meta)
        processor.write(output_msg)

    @property
    def object_data(self) -> bytes:
        """
        Attempts to interpret the body of the context
        as an object store event, and to syncronously load
        the associated object and return it.

        May throw exceptions if the message isn't an object store
        notification, if the object store is unavailable, or if
        the object store would otherwise throw an exception (for example,
        if the notification was for a deleted object.)
        """
        if self._object_data is not None:
            return self._object_data

        try:
            msg = json.loads(self.body)
            bucket = msg["Bucket"]
            obj = msg["Object"]
        except (json.JSONDecodeError, KeyError):
            log.error(
                "it doesn't look like this message was from the object store."
                " Make sure your tasks are configured to listen to object store messages"
                " when using context.object_data"
            )
            raise

        self._object_data = object_store.download(bucket, obj)

        return self._object_data
