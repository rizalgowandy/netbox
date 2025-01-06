import strawberry_django

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin
from wireless import filtersets, models

__all__ = (
    'WirelessLANGroupFilter',
    'WirelessLANFilter',
    'WirelessLinkFilter',
)


@strawberry_django.filter(models.WirelessLANGroup, lookups=True)
@autotype_decorator(filtersets.WirelessLANGroupFilterSet)
class WirelessLANGroupFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.WirelessLAN, lookups=True)
@autotype_decorator(filtersets.WirelessLANFilterSet)
class WirelessLANFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.WirelessLink, lookups=True)
@autotype_decorator(filtersets.WirelessLinkFilterSet)
class WirelessLinkFilter(BaseFilterMixin):
    pass
