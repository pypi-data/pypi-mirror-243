from django.db import models

from nautobot.dcim.choices import CableTypeChoices, CableLengthUnitChoices
from nautobot.dcim.models import Cable
from nautobot.extras.models import RelationshipModel
from nautobot.utilities.fields import ColorField
from nautobot.utilities.querysets import RestrictedQuerySet
from nautobot.core.models import BaseModel


class CablePlug(BaseModel):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class CableTemplate(BaseModel, RelationshipModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    label = models.CharField(
        max_length=100,
        blank=True
    )
    type = models.CharField(
        max_length=50,
        choices=CableTypeChoices,
        blank=True
    )
    plug = models.ForeignKey(
        to=CablePlug,
        on_delete=models.CASCADE,
        related_name="cable_templates",
        blank=True,
        null=True,
    )
    color = ColorField(
        blank=True
    )
    length = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )
    length_unit = models.CharField(
        max_length=50,
        choices=CableLengthUnitChoices,
        blank=True,
    )
    cable = models.OneToOneField(
        Cable,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    owner = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="cable_templates",
        blank=True,
        null=True,
    )

    supplier = models.ForeignKey(
        to="dcim.Manufacturer",
        on_delete=models.PROTECT,
        related_name="cable_templates",
        null=True,
        blank=True,
    )

    storage_rack = models.ForeignKey(
        to="dcim.Rack",
        on_delete=models.PROTECT,
        related_name="cable_templates",
        blank=True,
        null=True,
    )

    procurement_ident = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Procurement Identifier"
    )

    objects = RestrictedQuerySet.as_manager()

    import_csv_headers = [
        'name', 'owner', 'type', 'plug', 'label', 'color', 'length', 'length_unit', "storage_rack", "supplier",
        "procurement_ident"
    ]

    csv_headers = [
        *import_csv_headers,
        "in_use"
    ]

    def __str__(self):
        return self.name

    def to_csv(self):
        return (
            self.name,
            self.owner.name if self.owner else None,
            self.get_type_display() if self.type else None,
            self.plug.name if self.plug else None,
            self.label,
            self.color,
            self.length,
            self.length_unit,
            self.storage_rack.name if self.storage_rack else None,
            self.supplier.name if self.supplier else None,
            self.procurement_ident,
            self.cable is not None,
        )


class MeasurementLog(BaseModel):
    link = models.URLField(
        blank=True,
        null=True
    )
    cable = models.OneToOneField(
        Cable,
        on_delete=models.CASCADE,
    )
