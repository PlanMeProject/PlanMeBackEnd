"""Abstract model classes for generate unique id for each model."""
import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Model(TimeStampedModel):
    """Abstract model class for generate unique id for each model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Meta definition for Model."""
        abstract = True
