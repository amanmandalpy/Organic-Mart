"""Abstract persistence primitives shared by domain models."""

import uuid

from django.db import models


class UUIDTimeStampedModel(models.Model):
    """Give domain records opaque identifiers and UTC audit timestamps."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
