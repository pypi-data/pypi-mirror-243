import functools
import logging
import msgpack
import pydantic

from typing import Dict, Any, List, Optional, Tuple

from . import errors


logger = logging.getLogger(__name__)


class BaseModel(pydantic.BaseModel):
    @classmethod
    def model_validate_msgpack(cls, obj: bytes):
        return cls.model_validate(msgpack.loads(obj))

    def model_dump_msgpack(self, **kwargs) -> bytes:
        kwargs.setdefault("exclude_defaults", True)
        return msgpack.dumps(self.model_dump(**kwargs))


class AbstractOptions(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", frozen=True)

    def __init__(self, *args: "AbstractOptions", **kwargs: Dict[str, Any]):
        if args:
            merged = {}
            self_class = type(self)
            for options in args:
                if not isinstance(options, self_class):
                    raise TypeError(
                        f"Positional arguments must be {self_class} instances"
                    )

                merged.update(options.model_dump(exclude_unset=True))
            merged.update(**kwargs)

            kwargs = merged

        return super().__init__(**kwargs)

    def update(self, *args: "AbstractOptions", **kwargs: Dict[str, Any]):
        if not args and not kwargs:
            return self

        return self.__class__(self, *args, **kwargs)


class Request(BaseModel):
    method_name: str
    arguments: Dict[str, Any] = {}
    context: Optional[Any] = None
    timings: List[Tuple[str, float]] = []


class ResponseError(BaseModel):
    type: str
    message: Optional[str] = None


class Response(BaseModel):
    result: Optional[Any] = None
    error: Optional[ResponseError] = None
    context: Optional[Any] = None
    timings: List[Tuple[str, float]] = []

    @classmethod
    def wrap_errors(cls, func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            try:
                response = await func(*args, **kwargs)
                if not isinstance(response, cls):
                    raise TypeError(f"Incorrect response type, got: {type(response)}")

            except errors.RpcError as error:
                response = cls(
                    error={"type": type(error).__name__, "message": error.args[0]}
                )

            except Exception as error:
                logger.exception("Unhandled error")
                response = cls(error={"type": "UnhandledError", "message": repr(error)})

            return response

        return inner
