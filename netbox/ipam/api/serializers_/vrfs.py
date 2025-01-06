from ipam.models import RouteTarget, VRF
from netbox.api.fields import RelatedObjectCountField, SerializedPKRelatedField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers_.tenants import TenantSerializer

__all__ = (
    'RouteTargetSerializer',
    'VRFSerializer',
)


class RouteTargetSerializer(NetBoxModelSerializer):
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = RouteTarget
        fields = [
            'id', 'url', 'display_url', 'display', 'name', 'tenant', 'description', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'description')


class VRFSerializer(NetBoxModelSerializer):
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    import_targets = SerializedPKRelatedField(
        queryset=RouteTarget.objects.all(),
        serializer=RouteTargetSerializer,
        required=False,
        many=True
    )
    export_targets = SerializedPKRelatedField(
        queryset=RouteTarget.objects.all(),
        serializer=RouteTargetSerializer,
        required=False,
        many=True
    )

    # Related object counts
    ipaddress_count = RelatedObjectCountField('ip_addresses')
    prefix_count = RelatedObjectCountField('prefixes')

    class Meta:
        model = VRF
        fields = [
            'id', 'url', 'display_url', 'display', 'name', 'rd', 'tenant', 'enforce_unique', 'description', 'comments',
            'import_targets', 'export_targets', 'tags', 'custom_fields', 'created', 'last_updated', 'ipaddress_count',
            'prefix_count',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'rd', 'description', 'prefix_count')
