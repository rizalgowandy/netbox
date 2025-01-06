from copy import deepcopy
from functools import cached_property

import django_tables2 as tables
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ManyToOneRel
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_tables2.data import TableQuerysetData

from core.models import ObjectType
from extras.choices import *
from extras.models import CustomField, CustomLink
from netbox.constants import EMPTY_TABLE_TEXT
from netbox.registry import registry
from netbox.tables import columns
from utilities.paginator import EnhancedPaginator, get_paginate_count
from utilities.html import highlight
from utilities.string import title
from utilities.views import get_viewname
from .template_code import *

__all__ = (
    'BaseTable',
    'NetBoxTable',
    'SearchTable',
)


class BaseTable(tables.Table):
    """
    Base table class for NetBox objects. Adds support for:

        * User configuration (column preferences)
        * Automatic prefetching of related objects
        * BS5 styling

    :param user: Personalize table display for the given user (optional). Has no effect if AnonymousUser is passed.
    """
    exempt_columns = ()

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        # Set default empty_text if none was provided
        if self.empty_text is None:
            self.empty_text = _("No {model_name} found").format(model_name=self._meta.model._meta.verbose_name_plural)

        # Determine the table columns to display by checking the following:
        #   1. User's configuration for the table
        #   2. Meta.default_columns
        #   3. Meta.fields
        selected_columns = None
        if user is not None and not isinstance(user, AnonymousUser):
            selected_columns = user.config.get(f"tables.{self.name}.columns")
        if not selected_columns:
            selected_columns = getattr(self.Meta, 'default_columns', self.Meta.fields)

        # Hide non-selected columns which are not exempt
        for column in self.columns:
            if column.name not in [*selected_columns, *self.exempt_columns]:
                self.columns.hide(column.name)

        # Rearrange the sequence to list selected columns first, followed by all remaining columns
        # TODO: There's probably a more clever way to accomplish this
        self.sequence = [
            *[c for c in selected_columns if c in self.columns.names()],
            *[c for c in self.columns.names() if c not in selected_columns]
        ]

        # PK column should always come first
        if 'pk' in self.sequence:
            self.sequence.remove('pk')
            self.sequence.insert(0, 'pk')

        # Actions column should always come last
        if 'actions' in self.sequence:
            self.sequence.remove('actions')
            self.sequence.append('actions')

        # Dynamically update the table's QuerySet to ensure related fields are pre-fetched
        if isinstance(self.data, TableQuerysetData):

            prefetch_fields = []
            for column in self.columns:
                if column.visible:
                    model = getattr(self.Meta, 'model')
                    accessor = column.accessor
                    prefetch_path = []
                    for field_name in accessor.split(accessor.SEPARATOR):
                        try:
                            field = model._meta.get_field(field_name)
                        except FieldDoesNotExist:
                            break
                        if isinstance(field, (RelatedField, ManyToOneRel)):
                            # Follow ForeignKeys to the related model
                            prefetch_path.append(field_name)
                            model = field.remote_field.model
                        elif isinstance(field, GenericForeignKey):
                            # Can't prefetch beyond a GenericForeignKey
                            prefetch_path.append(field_name)
                            break
                    if prefetch_path:
                        prefetch_fields.append('__'.join(prefetch_path))
            self.data.data = self.data.data.prefetch_related(*prefetch_fields)

    def _get_columns(self, visible=True):
        columns = []
        for name, column in self.columns.items():
            if column.visible == visible and name not in self.exempt_columns:
                columns.append((name, column.verbose_name))
        return columns

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def available_columns(self):
        return sorted(self._get_columns(visible=False))

    @property
    def selected_columns(self):
        return self._get_columns(visible=True)

    @property
    def objects_count(self):
        """
        Return the total number of real objects represented by the Table. This is useful when dealing with
        prefixes/IP addresses/etc., where some table rows may represent available address space.
        """
        if not hasattr(self, '_objects_count'):
            self._objects_count = sum(1 for obj in self.data if hasattr(obj, 'pk'))
        return self._objects_count

    def configure(self, request):
        """
        Configure the table for a specific request context. This performs pagination and records
        the user's preferred ordering logic.
        """
        # Save ordering preference
        if request.user.is_authenticated:
            if self.prefixed_order_by_field in request.GET:
                if request.GET[self.prefixed_order_by_field]:
                    # If an ordering has been specified as a query parameter, save it as the
                    # user's preferred ordering for this table.
                    ordering = request.GET.getlist(self.prefixed_order_by_field)
                    request.user.config.set(f'tables.{self.name}.ordering', ordering, commit=True)
                else:
                    # If the ordering has been set to none (empty), clear any existing preference.
                    request.user.config.clear(f'tables.{self.name}.ordering', commit=True)
            elif ordering := request.user.config.get(f'tables.{self.name}.ordering'):
                # If no ordering has been specified, set the preferred ordering (if any).
                self.order_by = ordering

        # Paginate the table results
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        tables.RequestConfig(request, paginate).configure(self)


class NetBoxTable(BaseTable):
    """
    Table class for most NetBox objects. Adds support for custom field & custom link columns. Includes
    default columns for:

        * PK (row selection)
        * ID
        * Actions
    """
    pk = columns.ToggleColumn(
        visible=False
    )
    id = tables.Column(
        linkify=True,
        verbose_name=_('ID')
    )
    actions = columns.ActionsColumn()

    exempt_columns = ('pk', 'actions')
    embedded = False

    class Meta(BaseTable.Meta):
        pass

    def __init__(self, *args, extra_columns=None, **kwargs):
        if extra_columns is None:
            extra_columns = []

        if registered_columns := registry['tables'].get(self.__class__):
            extra_columns.extend([
                # Create a copy to avoid modifying the original Column
                (name, deepcopy(column)) for name, column in registered_columns.items()
            ])

        # Add custom field & custom link columns
        object_type = ObjectType.objects.get_for_model(self._meta.model)
        custom_fields = CustomField.objects.filter(
            object_types=object_type
        ).exclude(ui_visible=CustomFieldUIVisibleChoices.HIDDEN)
        extra_columns.extend([
            (f'cf_{cf.name}', columns.CustomFieldColumn(cf)) for cf in custom_fields
        ])
        custom_links = CustomLink.objects.filter(object_types=object_type, enabled=True)
        extra_columns.extend([
            (f'cl_{cl.name}', columns.CustomLinkColumn(cl)) for cl in custom_links
        ])

        super().__init__(*args, extra_columns=extra_columns, **kwargs)

    @cached_property
    def htmx_url(self):
        """
        Return the base HTML request URL for embedded tables.
        """
        if self.embedded:
            viewname = get_viewname(self._meta.model, action='list')
            try:
                return reverse(viewname)
            except NoReverseMatch:
                pass
        return ''


class SearchTable(tables.Table):
    object_type = columns.ContentTypeColumn(
        verbose_name=_('Type'),
        order_by="object___meta__verbose_name",
    )
    object = tables.Column(
        verbose_name=_('Object'),
        linkify=True,
        order_by=('name', )
    )
    field = tables.Column(
        verbose_name=_('Field'),
    )
    value = tables.Column(
        verbose_name=_('Value'),
    )
    attrs = columns.TemplateColumn(
        template_code=SEARCH_RESULT_ATTRS,
        verbose_name=_('Attributes')
    )

    trim_length = 30

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        empty_text = _(EMPTY_TABLE_TEXT)

    def __init__(self, data, highlight=None, **kwargs):
        self.highlight = highlight
        super().__init__(data, **kwargs)

    def render_field(self, value, record):
        try:
            model_field = record.object._meta.get_field(value)
            return title(model_field.verbose_name)
        except FieldDoesNotExist:
            return value

    def render_value(self, value):
        if not self.highlight:
            return value

        value = highlight(value, self.highlight, trim_pre=self.trim_length, trim_post=self.trim_length)

        return mark_safe(value)
