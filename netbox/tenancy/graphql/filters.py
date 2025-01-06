import strawberry_django

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin
from tenancy import filtersets, models

__all__ = (
    'TenantFilter',
    'TenantGroupFilter',
    'ContactFilter',
    'ContactRoleFilter',
    'ContactGroupFilter',
    'ContactAssignmentFilter',
)


@strawberry_django.filter(models.Tenant, lookups=True)
@autotype_decorator(filtersets.TenantFilterSet)
class TenantFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.TenantGroup, lookups=True)
@autotype_decorator(filtersets.TenantGroupFilterSet)
class TenantGroupFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.Contact, lookups=True)
@autotype_decorator(filtersets.ContactFilterSet)
class ContactFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.ContactRole, lookups=True)
@autotype_decorator(filtersets.ContactRoleFilterSet)
class ContactRoleFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.ContactGroup, lookups=True)
@autotype_decorator(filtersets.ContactGroupFilterSet)
class ContactGroupFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.ContactAssignment, lookups=True)
@autotype_decorator(filtersets.ContactAssignmentFilterSet)
class ContactAssignmentFilter(BaseFilterMixin):
    pass
