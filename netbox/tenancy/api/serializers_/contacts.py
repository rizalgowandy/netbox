from django.contrib.auth.models import ContentType
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.fields import ChoiceField, ContentTypeField
from netbox.api.serializers import NestedGroupModelSerializer, NetBoxModelSerializer
from tenancy.choices import ContactPriorityChoices
from tenancy.models import ContactAssignment, Contact, ContactGroup, ContactRole
from utilities.api import get_serializer_for_model
from .nested import NestedContactGroupSerializer

__all__ = (
    'ContactAssignmentSerializer',
    'ContactGroupSerializer',
    'ContactRoleSerializer',
    'ContactSerializer',
)


class ContactGroupSerializer(NestedGroupModelSerializer):
    parent = NestedContactGroupSerializer(required=False, allow_null=True, default=None)
    contact_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = ContactGroup
        fields = [
            'id', 'url', 'display_url', 'display', 'name', 'slug', 'parent', 'description', 'tags', 'custom_fields',
            'created', 'last_updated', 'contact_count', '_depth',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'slug', 'description', 'contact_count', '_depth')


class ContactRoleSerializer(NetBoxModelSerializer):

    class Meta:
        model = ContactRole
        fields = [
            'id', 'url', 'display_url', 'display', 'name', 'slug', 'description', 'tags', 'custom_fields',
            'created', 'last_updated',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'slug', 'description')


class ContactSerializer(NetBoxModelSerializer):
    group = ContactGroupSerializer(nested=True, required=False, allow_null=True, default=None)

    class Meta:
        model = Contact
        fields = [
            'id', 'url', 'display_url', 'display', 'group', 'name', 'title', 'phone', 'email', 'address', 'link',
            'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'description')


class ContactAssignmentSerializer(NetBoxModelSerializer):
    object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)
    contact = ContactSerializer(nested=True)
    role = ContactRoleSerializer(nested=True, required=False, allow_null=True)
    priority = ChoiceField(choices=ContactPriorityChoices, allow_blank=True, required=False, default=lambda: '')

    class Meta:
        model = ContactAssignment
        fields = [
            'id', 'url', 'display', 'object_type', 'object_id', 'object', 'contact', 'role', 'priority',
            'tags', 'custom_fields', 'created', 'last_updated',
        ]
        brief_fields = ('id', 'url', 'display', 'contact', 'role', 'priority')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_object(self, instance):
        serializer = get_serializer_for_model(instance.object_type.model_class())
        context = {'request': self.context['request']}
        return serializer(instance.object, nested=True, context=context).data
