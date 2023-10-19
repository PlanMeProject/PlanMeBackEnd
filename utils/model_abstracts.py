"""Abstract model classes for generate unique id for each model."""
import uuid
from django.db import models


class Model(models.Model):
    """Abstract model class."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        """Meta definition for Model."""
        abstract = True
