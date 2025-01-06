from rest_framework.routers import APIRootView

from circuits import filtersets
from circuits.models import *
from dcim.api.views import PassThroughPortMixin
from netbox.api.viewsets import NetBoxModelViewSet
from . import serializers


class CircuitsRootView(APIRootView):
    """
    Circuits API root view
    """
    def get_view_name(self):
        return 'Circuits'


#
# Providers
#

class ProviderViewSet(NetBoxModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    filterset_class = filtersets.ProviderFilterSet


#
#  Circuit Types
#

class CircuitTypeViewSet(NetBoxModelViewSet):
    queryset = CircuitType.objects.all()
    serializer_class = serializers.CircuitTypeSerializer
    filterset_class = filtersets.CircuitTypeFilterSet


#
# Circuits
#

class CircuitViewSet(NetBoxModelViewSet):
    queryset = Circuit.objects.all()
    serializer_class = serializers.CircuitSerializer
    filterset_class = filtersets.CircuitFilterSet


#
# Circuit Terminations
#

class CircuitTerminationViewSet(PassThroughPortMixin, NetBoxModelViewSet):
    queryset = CircuitTermination.objects.all()
    serializer_class = serializers.CircuitTerminationSerializer
    filterset_class = filtersets.CircuitTerminationFilterSet


#
# Circuit Groups
#

class CircuitGroupViewSet(NetBoxModelViewSet):
    queryset = CircuitGroup.objects.all()
    serializer_class = serializers.CircuitGroupSerializer
    filterset_class = filtersets.CircuitGroupFilterSet


#
# Circuit Group Assignments
#

class CircuitGroupAssignmentViewSet(NetBoxModelViewSet):
    queryset = CircuitGroupAssignment.objects.all()
    serializer_class = serializers.CircuitGroupAssignmentSerializer
    filterset_class = filtersets.CircuitGroupAssignmentFilterSet


#
# Provider accounts
#

class ProviderAccountViewSet(NetBoxModelViewSet):
    queryset = ProviderAccount.objects.all()
    serializer_class = serializers.ProviderAccountSerializer
    filterset_class = filtersets.ProviderAccountFilterSet


#
# Provider networks
#

class ProviderNetworkViewSet(NetBoxModelViewSet):
    queryset = ProviderNetwork.objects.all()
    serializer_class = serializers.ProviderNetworkSerializer
    filterset_class = filtersets.ProviderNetworkFilterSet
