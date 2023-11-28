from ..models import (
    SecretCreating,
    SecretDeleting,
    SecretDetail,
    SecretReading,
    SecretSummary,
)
from .base import ModelClient


class Secret(
    ModelClient[
        SecretCreating,
        SecretReading,
        SecretCreating,
        SecretDeleting,
        SecretSummary,
        SecretDetail,
    ]
):
    Creating = SecretCreating
    Reading = SecretReading
    Deleting = SecretDeleting
    Summary = SecretSummary
    Detail = SecretDetail
