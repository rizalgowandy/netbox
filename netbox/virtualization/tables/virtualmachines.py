import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from dcim.tables.devices import BaseInterfaceTable
from netbox.tables import NetBoxTable, columns
from tenancy.tables import ContactsColumnMixin, TenancyColumnsMixin
from utilities.templatetags.helpers import humanize_megabytes
from virtualization.models import VirtualDisk, VirtualMachine, VMInterface

__all__ = (
    'VirtualDiskTable',
    'VirtualMachineTable',
    'VirtualMachineVirtualDiskTable',
    'VirtualMachineVMInterfaceTable',
    'VMInterfaceTable',
)

VMINTERFACE_BUTTONS = """
{% if perms.virtualization.change_vminterface %}
  <span class="dropdown">
    <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="Add">
      <span class="mdi mdi-plus-thick" aria-hidden="true"></span>
    </button>
    <ul class="dropdown-menu dropdown-menu-end">
      {% if perms.ipam.add_ipaddress %}
        <li><a class="dropdown-item" href="{% url 'ipam:ipaddress_add' %}?vminterface={{ record.pk }}&return_url={% url 'virtualization:virtualmachine_interfaces' pk=object.pk %}">IP Address</a></li>
      {% endif %}
      {% if perms.vpn.add_l2vpntermination %}
        <li><a class="dropdown-item" href="{% url 'vpn:l2vpntermination_add' %}?virtual_machine={{ object.pk }}&vminterface={{ record.pk }}&return_url={% url 'virtualization:virtualmachine_interfaces' pk=object.pk %}">L2VPN Termination</a></li>
      {% endif %}
      {% if perms.ipam.add_fhrpgroupassignment %}
        <li><a class="dropdown-item" href="{% url 'ipam:fhrpgroupassignment_add' %}?interface_type={{ record|content_type_id }}&interface_id={{ record.pk }}&return_url={% url 'virtualization:virtualmachine_interfaces' pk=object.pk %}">Assign FHRP Group</a></li>
      {% endif %}
    </ul>
  </span>
{% endif %}
{% if perms.vpn.add_tunnel and not record.tunnel_termination %}
  <a href="{% url 'vpn:tunnel_add' %}?termination1_type=virtualization.virtualmachine&termination1_parent={{ record.virtual_machine.pk }}&termination1_termination={{ record.pk }}&return_url={% url 'virtualization:virtualmachine_interfaces' pk=object.pk %}" title="Create a tunnel" class="btn btn-success btn-sm">
    <i class="mdi mdi-tunnel-outline" aria-hidden="true"></i>
  </a>
{% elif perms.vpn.delete_tunneltermination and record.tunnel_termination %}
  <a href="{% url 'vpn:tunneltermination_delete' pk=record.tunnel_termination.pk %}?return_url={% url 'virtualization:virtualmachine_interfaces' pk=object.pk %}" title="Remove tunnel" class="btn btn-danger btn-sm">
    <i class="mdi mdi-tunnel-outline" aria-hidden="true"></i>
  </a>
{% endif %}
"""


#
# Virtual machines
#

class VirtualMachineTable(TenancyColumnsMixin, ContactsColumnMixin, NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        order_by=('_name',),
        linkify=True
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_('Status'),
    )
    site = tables.Column(
        verbose_name=_('Site'),
        linkify=True
    )
    cluster = tables.Column(
        verbose_name=_('Cluster'),
        linkify=True
    )
    device = tables.Column(
        verbose_name=_('Device'),
        linkify=True
    )
    role = columns.ColoredLabelColumn(
        verbose_name=_('Role'),
    )
    platform = tables.Column(
        linkify=True,
        verbose_name=_('Platform')
    )
    comments = columns.MarkdownColumn(
        verbose_name=_('Comments'),
    )
    primary_ip4 = tables.Column(
        linkify=True,
        verbose_name=_('IPv4 Address')
    )
    primary_ip6 = tables.Column(
        linkify=True,
        verbose_name=_('IPv6 Address')
    )
    primary_ip = tables.Column(
        linkify=True,
        order_by=('primary_ip4', 'primary_ip6'),
        verbose_name=_('IP Address')
    )
    tags = columns.TagColumn(
        url_name='virtualization:virtualmachine_list'
    )
    interface_count = tables.Column(
        verbose_name=_('Interfaces')
    )
    virtual_disk_count = tables.Column(
        verbose_name=_('Virtual Disks')
    )
    config_template = tables.Column(
        verbose_name=_('Config Template'),
        linkify=True
    )
    disk = tables.Column(
        verbose_name=_('Disk'),
    )

    class Meta(NetBoxTable.Meta):
        model = VirtualMachine
        fields = (
            'pk', 'id', 'name', 'status', 'site', 'cluster', 'device', 'role', 'tenant', 'tenant_group', 'vcpus',
            'memory', 'disk', 'primary_ip4', 'primary_ip6', 'primary_ip', 'description', 'comments', 'config_template',
            'serial', 'contacts', 'tags', 'created', 'last_updated',
        )
        default_columns = (
            'pk', 'name', 'status', 'site', 'cluster', 'role', 'tenant', 'vcpus', 'memory', 'disk', 'primary_ip',
        )

    def render_disk(self, value):
        return humanize_megabytes(value)


#
# VM components
#

class VMInterfaceTable(BaseInterfaceTable):
    virtual_machine = tables.Column(
        verbose_name=_('Virtual Machine'),
        linkify=True
    )
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True
    )
    vrf = tables.Column(
        verbose_name=_('VRF'),
        linkify=True
    )
    tags = columns.TagColumn(
        url_name='virtualization:vminterface_list'
    )

    class Meta(NetBoxTable.Meta):
        model = VMInterface
        fields = (
            'pk', 'id', 'name', 'virtual_machine', 'enabled', 'mac_address', 'mtu', 'mode', 'description', 'tags',
            'vrf', 'l2vpn', 'tunnel', 'ip_addresses', 'fhrp_groups', 'untagged_vlan', 'tagged_vlans', 'created',
            'last_updated',
        )
        default_columns = ('pk', 'name', 'virtual_machine', 'enabled', 'description')


class VirtualMachineVMInterfaceTable(VMInterfaceTable):
    parent = tables.Column(
        verbose_name=_('Parent'),
        linkify=True
    )
    bridge = tables.Column(
        verbose_name=_('Bridge'),
        linkify=True
    )
    actions = columns.ActionsColumn(
        actions=('edit', 'delete'),
        extra_buttons=VMINTERFACE_BUTTONS
    )

    class Meta(NetBoxTable.Meta):
        model = VMInterface
        fields = (
            'pk', 'id', 'name', 'enabled', 'parent', 'bridge', 'mac_address', 'mtu', 'mode', 'description', 'tags',
            'vrf', 'l2vpn', 'tunnel', 'ip_addresses', 'fhrp_groups', 'untagged_vlan', 'tagged_vlans', 'actions',
        )
        default_columns = ('pk', 'name', 'enabled', 'mac_address', 'mtu', 'mode', 'description', 'ip_addresses')
        row_attrs = {
            'data-name': lambda record: record.name,
            'data-virtual': lambda record: "true",
            'data-enabled': lambda record: "true" if record.enabled else "false",
        }


class VirtualDiskTable(NetBoxTable):
    virtual_machine = tables.Column(
        verbose_name=_('Virtual Machine'),
        linkify=True
    )
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True
    )
    size = tables.Column(
        verbose_name=_('Size')
    )
    tags = columns.TagColumn(
        url_name='virtualization:virtualdisk_list'
    )

    class Meta(NetBoxTable.Meta):
        model = VirtualDisk
        fields = (
            'pk', 'id', 'virtual_machine', 'name', 'size', 'description', 'tags',
        )
        default_columns = ('pk', 'name', 'virtual_machine', 'size', 'description')
        row_attrs = {
            'data-name': lambda record: record.name,
        }

    def render_size(self, value):
        return humanize_megabytes(value)


class VirtualMachineVirtualDiskTable(VirtualDiskTable):
    actions = columns.ActionsColumn(
        actions=('edit', 'delete'),
    )

    class Meta(VirtualDiskTable.Meta):
        fields = (
            'pk', 'id', 'name', 'size', 'description', 'tags', 'actions',
        )
        default_columns = ('pk', 'name', 'size', 'description')
