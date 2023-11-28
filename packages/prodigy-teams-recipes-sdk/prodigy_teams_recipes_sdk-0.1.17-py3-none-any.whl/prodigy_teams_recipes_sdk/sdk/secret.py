from ..types import Secret
from .decorator import teams_type

teams_type(
    "secret",
    title="Secret",
    description="Select an existing secret",
    exclude={"id", "name", "path", "broker_id"},
)(Secret)


__all__ = ["Secret"]
