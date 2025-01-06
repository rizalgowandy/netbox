import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django_tables2.utils import Accessor

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin
from vpn.models import *

__all__ = (
    'TunnelTable',
    'TunnelGroupTable',
    'TunnelTerminationTable',
)


class TunnelGroupTable(NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True
    )
    tunnel_count = columns.LinkedCountColumn(
        viewname='vpn:tunnel_list',
        url_params={'group_id': 'pk'},
        verbose_name=_('Tunnels')
    )
    tags = columns.TagColumn(
        url_name='vpn:tunnelgroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = TunnelGroup
        fields = (
            'pk', 'id', 'name', 'tunnel_count', 'description', 'slug', 'tags', 'actions', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'tunnel_count', 'description')


class TunnelTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True
    )
    group = tables.Column(
        verbose_name=_('Group'),
        linkify=True
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_('Status')
    )
    ipsec_profile = tables.Column(
        verbose_name=_('IPSec profile'),
        linkify=True
    )
    terminations_count = columns.LinkedCountColumn(
        accessor=Accessor('count_terminations'),
        viewname='vpn:tunneltermination_list',
        url_params={'tunnel_id': 'pk'},
        verbose_name=_('Terminations')
    )
    comments = columns.MarkdownColumn(
        verbose_name=_('Comments'),
    )
    tags = columns.TagColumn(
        url_name='vpn:tunnel_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Tunnel
        fields = (
            'pk', 'id', 'name', 'group', 'status', 'encapsulation', 'ipsec_profile', 'tenant', 'tenant_group',
            'tunnel_id', 'termination_count', 'description', 'comments', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'group', 'status', 'encapsulation', 'tenant', 'terminations_count')


class TunnelTerminationTable(TenancyColumnsMixin, NetBoxTable):
    tunnel = tables.Column(
        verbose_name=_('Tunnel'),
        linkify=True
    )
    role = columns.ChoiceFieldColumn(
        verbose_name=_('Role')
    )
    termination_parent = tables.Column(
        accessor='termination__parent_object',
        linkify=True,
        orderable=False,
        verbose_name=_('Host')
    )
    termination = tables.Column(
        verbose_name=_('Tunnel interface'),
        linkify=True
    )
    ip_addresses = columns.ManyToManyColumn(
        accessor=tables.A('termination__ip_addresses'),
        orderable=False,
        linkify_item=True,
        verbose_name=_('IP Addresses')
    )
    outside_ip = tables.Column(
        verbose_name=_('Outside IP'),
        linkify=True
    )
    tags = columns.TagColumn(
        url_name='vpn:tunneltermination_list'
    )

    class Meta(NetBoxTable.Meta):
        model = TunnelTermination
        fields = (
            'pk', 'id', 'tunnel', 'role', 'termination_parent', 'termination', 'ip_addresses', 'outside_ip', 'tags',
            'created', 'last_updated',
        )
        default_columns = (
            'pk', 'id', 'tunnel', 'role', 'termination_parent', 'termination', 'ip_addresses', 'outside_ip',
        )
