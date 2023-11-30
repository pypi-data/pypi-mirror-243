from typing import Any, Callable, Dict, List, Optional, Tuple

from seaplane.logs import log

"""
Tasks are weird use / mention hybrids: in a deployment
context, they are a map of Seaplane carrier flows and
the connections between them. In an execution context
on the Seaplane platform, they're containers for executable
code that get the results of endpoints or tasks as input and can
emit good things to their downstream flows and endpoints.
"""


class TaskEvent:
    def __init__(self, id: str, input: Any) -> None:
        self.id = id
        self.status = "in_progress"
        self.input = input
        self.output: Optional[Any] = None
        self.error: Optional[Any] = None

    def set_output(self, output: Any) -> None:
        self.output = output
        self.status = "completed"

    def set_error(self, error: Any) -> None:
        self.error = error
        self.status = "error"


class Task:
    def __init__(
        self,
        func: Callable[[Any], Any],
        id: str,
        type: Optional[str] = None,
        model: Optional[str] = None,
        index_name: Optional[str] = None,
        replicas: Optional[int] = 1,
    ) -> None:
        self.func = func
        self.id = id
        self.args: Optional[Tuple[Any, ...]] = None
        self.kwargs: Optional[Dict[str, Any]] = None
        self.type = type
        self.model = model
        self.sources: List[str] = []
        self.name = func.__name__
        self.index_name = index_name
        self.replicas = replicas

    def process(self, *args: Any, **kwargs: Any) -> Any:
        self.args = args
        self.kwargs = kwargs

        log.info(f"Task '{self.id}' processing...")
        return self.func(*self.args, **self.kwargs)

    def called_from(self, sources: List[str]) -> None:
        self.sources = sources

    def print(self) -> None:
        log.info(f"id: {self.id}, replicas: {self.replicas}")
